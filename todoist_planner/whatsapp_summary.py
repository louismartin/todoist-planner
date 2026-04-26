"""WhatsApp daily summary functionality."""

from datetime import datetime
from typing import Optional

from twilio.rest import Client

from todoist_planner.config import Config, TwilioConfig, ScheduleConfig
from todoist_planner.core import get_api, get_project_id_by_name, get_active_tasks, filter_tasks
from todoist_planner.task import Task


def is_workday() -> bool:
    """Check if today is a workday (Monday-Friday)."""
    return datetime.now().weekday() < 5


def get_projects_for_today(schedule: ScheduleConfig) -> list[str]:
    """Get the list of projects to include based on day of week."""
    if is_workday():
        return schedule.weekday_projects
    return schedule.weekend_projects


def get_top_tasks(config: Config) -> list[Task]:
    """Get the top priority tasks for today.

    Args:
        config: Application configuration.

    Returns:
        List of top priority tasks, sorted by priority descending.
    """
    api = get_api()
    projects = get_projects_for_today(config.schedule)
    all_tasks = []

    for project_name in projects:
        try:
            project_id = get_project_id_by_name(project_name, api)
            tasks = get_active_tasks(project_id, api)
            tasks = filter_tasks(tasks, api)
            all_tasks.extend(tasks)
        except NameError:
            # Project not found, skip it
            continue

    # Filter to labeled tasks only
    labeled_tasks = [task for task in all_tasks if task.is_labeled()]

    # Sort by priority descending (highest priority first)
    labeled_tasks.sort(key=lambda t: t.get_priority() or 0, reverse=True)

    # Return top N tasks
    return labeled_tasks[:config.schedule.num_tasks]


def format_duration(minutes: Optional[int]) -> str:
    """Format duration in a human-readable way."""
    if minutes is None:
        return "?"
    if minutes < 60:
        return f"{minutes}min"
    hours = minutes // 60
    remaining_mins = minutes % 60
    if remaining_mins == 0:
        return f"{hours}h"
    return f"{hours}h{remaining_mins}min"


def compose_message(tasks: list[Task], config: Config) -> str:
    """Compose the WhatsApp message with today's top tasks.

    Args:
        tasks: List of top priority tasks.
        config: Application configuration.

    Returns:
        Formatted message string.
    """
    day_type = "Workday" if is_workday() else "Weekend"

    if not tasks:
        return (
            f"Good morning! ({day_type})\n\n"
            "No prioritized tasks found for today. "
            "Consider labeling some tasks to get personalized recommendations."
        )

    lines = [f"Good morning! Here are your top {len(tasks)} tasks for today ({day_type}):"]
    lines.append("")

    for i, task in enumerate(tasks, 1):
        priority_pct = round((task.get_priority() or 0) * 100)
        duration_str = format_duration(task.duration)

        lines.append(f"{i}. {task.stripped_content}")
        lines.append(f"   Priority: {priority_pct}% | Duration: ~{duration_str}")
        lines.append("")

    lines.append("Focus on these before anything else. You've got this!")

    return "\n".join(lines)


def send_whatsapp(message: str, twilio_config: TwilioConfig) -> str:
    """Send a WhatsApp message via Twilio.

    Args:
        message: The message text to send.
        twilio_config: Twilio API configuration.

    Returns:
        Message SID on success.
    """
    client = Client(twilio_config.account_sid, twilio_config.auth_token)
    msg = client.messages.create(
        body=message,
        from_=twilio_config.from_number,
        to=twilio_config.to_number,
    )
    return msg.sid


def send_daily_summary(config: Config, dry_run: bool = False) -> tuple[str, Optional[str]]:
    """Generate and send the daily task summary.

    Args:
        config: Application configuration.
        dry_run: If True, only generate message without sending.

    Returns:
        Tuple of (message, message_sid or None if dry_run).
    """
    tasks = get_top_tasks(config)
    message = compose_message(tasks, config)

    if dry_run:
        return message, None

    message_sid = send_whatsapp(message, config.twilio)
    return message, message_sid


def send_test_message(config: Config) -> str:
    """Send a test message to verify Twilio configuration.

    Args:
        config: Application configuration.

    Returns:
        Message SID.
    """
    test_message = (
        "Test message from todoist-planner!\n\n"
        "Your WhatsApp integration is working correctly. "
        "You will receive daily task summaries at this number."
    )
    return send_whatsapp(test_message, config.twilio)
