#!/usr/bin/env python3
"""Interactive task labeling via WhatsApp voice messages."""

import argparse
import json
import time
from datetime import datetime, timezone

import anthropic
from twilio.rest import Client

from todoist_planner.config import load_config, Config
from todoist_planner.core import get_api, filter_tasks
from todoist_planner.task import Task


def get_tasks_to_label(todoist_api, query: str) -> list[Task]:
    """Fetch tasks matching the filter query, excluding already reviewed tasks."""
    tasks = []
    for batch in todoist_api.filter_tasks(query=query):
        for t in batch:
            # Skip tasks already reviewed
            if "reviewed" in t.labels:
                continue
            task = Task(t, todoist_api)
            tasks.append(task)
    return tasks


def mark_as_reviewed(task: Task, todoist_api) -> None:
    """Add @reviewed label to a task."""
    labels = list(task.labels)
    if "reviewed" not in labels:
        labels.append("reviewed")
        todoist_api.update_task(task_id=task.id, labels=labels)


def send_whatsapp(message: str, config: Config) -> str:
    """Send a WhatsApp message."""
    client = Client(config.twilio.account_sid, config.twilio.auth_token)
    msg = client.messages.create(
        body=message,
        from_=config.twilio.from_number,
        to=config.twilio.to_number,
    )
    return msg.sid


def get_latest_reply(config: Config, after_timestamp: datetime) -> str | None:
    """Poll for the latest incoming WhatsApp message after a given timestamp."""
    client = Client(config.twilio.account_sid, config.twilio.auth_token)

    # Fetch messages sent TO our Twilio number (i.e., from the user)
    messages = client.messages.list(
        to=config.twilio.from_number,
        from_=config.twilio.to_number,
        limit=5,
    )

    for msg in messages:
        # Check if message is newer than our timestamp
        if msg.date_sent and msg.date_sent > after_timestamp:
            return msg.body

    return None


def wait_for_reply(config: Config, timeout: int = 300, poll_interval: int = 5) -> str | None:
    """Wait for a WhatsApp reply within timeout seconds."""
    start_time = datetime.now(timezone.utc)
    deadline = time.time() + timeout

    while time.time() < deadline:
        reply = get_latest_reply(config, start_time)
        if reply:
            return reply
        time.sleep(poll_interval)

    return None


def get_someday_maybe_section_id(project_id: str, todoist_api) -> str | None:
    """Get the Someday Maybe section ID for a given project."""
    for batch in todoist_api.get_sections(project_id=project_id):
        for section in batch:
            if section.name.lower() == "someday maybe":
                return section.id
    return None


def parse_reply_with_claude(task_content: str, user_reply: str, config: Config) -> dict:
    """Use Claude to parse the user's voice reply and extract structured info."""
    client = anthropic.Anthropic(api_key=config.anthropic.api_key)

    prompt = f"""Tu es un assistant qui aide à organiser des tâches Todoist. L'utilisateur a une tâche et a donné une description vocale.

IMPORTANT: La réponse de l'utilisateur a été transcrite par un algorithme de speech-to-text imparfait. Il peut y avoir des erreurs de transcription. Essaie d'intuiter les mots mal transcrits en fonction du contexte.

Tâche: "{task_content}"

Réponse de l'utilisateur (transcription vocale): "{user_reply}"

Analyse cette réponse et extrais:
1. Une description reformulée et claire à ajouter à la tâche (en français). Cette description sera ajoutée au champ "description" de la tâche Todoist.
2. Si mentionné: importance (1-5), urgence (1-5), niveau de fun (1-5), durée estimée (en minutes)
3. L'action à effectuer:
   - "update": mettre à jour la tâche avec la description
   - "skip": passer à la tâche suivante sans rien faire
   - "delete": supprimer la tâche
   - "complete": marquer la tâche comme terminée
   - "someday_maybe": déplacer la tâche vers la section "Someday Maybe" du projet actuel (l'utilisateur peut dire "someday maybe", "un jour peut-être", "plus tard", etc.)

Réponds en JSON avec ce format:
{{
    "description": "description reformulée à ajouter au champ description",
    "importance": null ou 1-5,
    "urgency": null ou 1-5,
    "fun": null ou 1-5,
    "duration": null ou nombre de minutes,
    "action": "update" ou "skip" ou "delete" ou "complete" ou "someday_maybe"
}}

Réponds uniquement avec le JSON, sans markdown ni commentaires."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response.content[0].text)
    except json.JSONDecodeError:
        return {"description": user_reply, "action": "update"}


def update_task_with_info(task: Task, info: dict, todoist_api) -> str:
    """Update the task based on parsed info."""
    action = info.get("action", "update")

    if action == "skip":
        return "skipped"
    elif action == "delete":
        task.delete(todoist_api)
        return "deleted"
    elif action == "complete":
        task.complete(todoist_api)
        return "completed"
    elif action == "someday_maybe":
        # Move task to Someday Maybe section
        section_id = get_someday_maybe_section_id(task.project_id, todoist_api)
        if section_id:
            todoist_api.move_task(task_id=task.id, section_id=section_id)
            return "moved to Someday Maybe"
        else:
            return "skipped (no Someday Maybe section found)"
    else:
        # Build description with user's notes and attributes
        parts = []

        # Add user's description
        description = info.get("description", "")
        if description:
            parts.append(description)

        # Add attributes as text in description
        attrs = []
        if info.get("importance"):
            attrs.append(f"importance: {info['importance']}/5")
        if info.get("urgency"):
            attrs.append(f"urgence: {info['urgency']}/5")
        if info.get("fun"):
            attrs.append(f"fun: {info['fun']}/5")
        if info.get("duration"):
            attrs.append(f"durée: {info['duration']}min")

        if attrs:
            parts.append(" | ".join(attrs))

        # Build final description wrapped in tags
        new_content = "\n".join(parts) if parts else ""

        if new_content:
            wrapped_content = f"<todoist-planner>\n{new_content}\n</todoist-planner>"
            existing_desc = task._todoist_task.description or ""
            if existing_desc:
                final_desc = f"{existing_desc}\n\n{wrapped_content}"
            else:
                final_desc = wrapped_content

            todoist_api.update_task(task_id=task.id, description=final_desc)

        return "updated"


def run_labeling_session(config: Config, query: str, dry_run: bool = False):
    """Run an interactive WhatsApp labeling session."""
    if not config.anthropic:
        print("Error: Anthropic API key required for parsing replies")
        return

    todoist_api = get_api()
    tasks = get_tasks_to_label(todoist_api, query)
    tasks = filter_tasks(tasks, todoist_api)
    unlabeled = [t for t in tasks if not t.is_labeled()]

    print(f"Found {len(unlabeled)} unlabeled tasks")

    if not unlabeled:
        print("Pas de tâches à labelliser!")
        return

    # Send intro message
    intro = f"Salut! {len(unlabeled)} tâches à traiter. Réponds à l'oral. Tu peux dire 'skip', 'supprimer', 'terminer', ou 'someday maybe'. C'est parti!"
    if not dry_run:
        send_whatsapp(intro, config)
        time.sleep(2)
    else:
        print(f"[DRY RUN] Would send: {intro}")

    for i, task in enumerate(unlabeled, 1):
        # Send task
        msg = f"[{i}/{len(unlabeled)}] {task.stripped_content}"

        if dry_run:
            print(f"\n[DRY RUN] Would send: {msg}")
            continue

        send_whatsapp(msg, config)
        print(f"\nSent task {i}: {task.stripped_content[:50]}...")

        # Wait for reply
        print("Waiting for reply...")
        reply = wait_for_reply(config, timeout=300)

        if not reply:
            print("No reply received, skipping...")
            continue

        print(f"Received: {reply}")

        # Parse with Claude
        info = parse_reply_with_claude(task.stripped_content, reply, config)
        print(f"Parsed: {info}")

        # Update task
        result = update_task_with_info(task, info, todoist_api)
        print(f"Result: {result}")

        # Mark as reviewed (except for skipped tasks)
        if result != "skipped":
            mark_as_reviewed(task, todoist_api)

    # Done
    print("Terminé!")


def main():
    parser = argparse.ArgumentParser(description="Label tasks via WhatsApp voice messages")
    parser.add_argument(
        "--query",
        type=str,
        default="(overdue | Today) & (#Personal | #GluGlu | #Inbox)",
        help="Todoist filter query",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without sending messages",
    )
    args = parser.parse_args()

    config = load_config()
    run_labeling_session(config, args.query, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
