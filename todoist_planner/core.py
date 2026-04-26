from pathlib import Path
import sys

from tqdm import tqdm
from todoist_api_python.api import TodoistAPI

from todoist_planner.task import Task
from todoist_planner.utils import ask_question


REPO_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILEPATH = REPO_DIR / 'token'


def ask_for_token():
    text = 'Please copy your todoist API token.'
    text += '\nYou can find it in "Todoist Settings -> Integrations -> API token":'
    text += '\nhttps://en.todoist.com/prefs/integrations\n'
    token = input(text)
    with TOKEN_FILEPATH.open('w') as f:
        f.write(token + '\n')


def read_token():
    if not TOKEN_FILEPATH.exists():
        ask_for_token()
    with TOKEN_FILEPATH.open('r') as f:
        token = f.read().rstrip('\n')
    if token == '':
        ask_for_token()
    return token


def get_project_name():
    if len(sys.argv) == 2:
        return sys.argv[1]
    return input('What project would you like to work on? ')


def get_api():
    return TodoistAPI(read_token())


def commit(api):
    """Commit all modified tasks to the API."""
    pbar = tqdm(total=len(Task.modified_tasks), desc='Committing')
    for task in list(Task.modified_tasks.values()):
        task.save(api)
        pbar.update(1)
    Task.modified_tasks = {}
    pbar.close()


def get_project_id_by_name(name, api):
    for batch in api.get_projects():
        for project in batch:
            if project.name.lower() == name.lower():
                return project.id
    raise NameError(f'Project {name} cannot be found.')


def get_active_tasks(project_id, api):
    tasks = []
    for batch in api.get_tasks(project_id=project_id):
        for item in batch:
            if item.is_completed:
                continue
            tasks.append(Task(item, api))
    return tasks


def get_labels(api):
    labels = {}
    for batch in api.get_labels():
        for label in batch:
            labels[label.name] = label.id
    return labels


def get_notes(task, api):
    """Get comments/notes for a task."""
    notes = []
    for batch in api.get_comments(task_id=task.id):
        for comment in batch:
            notes.append(comment)
    return notes


def reverse_dictionary(dic):
    return {v: k for k, v in dic.items()}


def label_task(task, api):
    def resolve_command(cmd):
        cmd_resolved = True
        if cmd in ['next', 'n']:
            pass
        elif cmd in ['delete', 'd']:
            task.delete(api)
        elif cmd in ['edit', 'e']:
            task.stripped_content = input('New task content: \n')
            label_task(task, api)
        elif cmd in ['complete', 'c']:
            task.complete(api)
        elif cmd in ['clear', 'cl']:
            task.clear_attributes()
        elif cmd in ['split', 's']:
            task.split(api)
        elif cmd in ['commit']:
            commit(api)
            label_task(task, api)
        else:
            cmd_resolved = False
        return cmd_resolved

    print(f'"{task.stripped_content}"')
    ask_texts = {
        'importance': f'How important is this task? (1-{task.max_attribute_value}): ',
        'urgency': f'How urgent is this task? (1-{task.max_attribute_value}): ',
        'fun': f'How fun is this task? (1-{task.max_attribute_value}): ',
        'duration': 'How long will this task take? (minutes): ',
    }
    for attr_name in task.attribute_names:
        if getattr(task, attr_name) is not None:
            continue
        ask_text = ask_texts[attr_name]
        new_value = input(ask_text)
        cmd_resolved = resolve_command(new_value)
        if cmd_resolved:
            return
        setattr(task, attr_name, new_value)


def label_tasks(unlabeled_tasks, api):
    if not unlabeled_tasks:
        print('No unlabeled tasks.')
        return
    print('~' * 50)
    print(f'There are {len(unlabeled_tasks)} unlabeled tasks:\n')
    for i, task in enumerate(unlabeled_tasks):
        sys.stdout.write(f'{i+1}.')
        label_task(task, api)
        print('\n')
    commit(api)
    print('~' * 50)


def sort_tasks(tasks):
    return sorted(tasks, key=lambda task: task.get_priority() or 0)


def filter_tasks(tasks, api):
    """Filter out tasks with excluded labels."""
    excluded_label_names = ['onhold', 'medecin', 'orsay', 'albert']
    excluded_label_names_lower = [name.lower() for name in excluded_label_names]

    def has_excluded_label(task):
        task_labels = [label.lower() for label in task.labels]
        return any(excluded in task_labels for excluded in excluded_label_names_lower)

    return [task for task in tasks if not has_excluded_label(task)]
