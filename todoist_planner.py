import math
from pathlib import Path
import re

from todoist.api import TodoistAPI


__file__ = '/Users/louismartin/dev/todoist-planner/Untitled.ipynb'
REPO_DIR = Path(__file__).resolve().parent
token_filepath = REPO_DIR / 'token'


def ask_for_token():
    text = 'Please copy your todoist API token.'
    text += '\nYou can find it in "Todoist Settings -> Integrations -> API token":'
    token = input(text)
    with token_filepath.open('w') as f:
        f.write(token + '\n')


def read_token():
    if not token_filepath.exists():
        ask_for_token()
    with token_filepath.open('r') as f:
        return f.read().rstrip('\n')


def get_project_id_by_name(name, api):
    for project in api.projects.all():
        if project['name'].lower() == name.lower():
            return project['id']


def get_active_tasks(project_id, api):
    tasks = []
    for task in api.items.all():
        if task['project_id'] != project_id:
            continue
        if task['checked']:
            continue
        tasks.append(task)
    return tasks


def get_labels(api):
    return {label['name']: label['id'] for label in api.labels.all()}


def _deprecated_get_importance_ids(api):
    labels = get_labels(api)
    names_to_level = {'i1': 1, 'i2': 2, 'i3': 3, 'i4': 4}
    names_to_id = {name: labels[name] for name in names_to_level.keys()}
    return {importance: names_to_id[name]
            for name, importance in names_to_level.items()}


def _deprecated_get_urgency_ids(api):
    labels = get_labels(api)
    names_to_level = {'u1': 1, 'u2': 2, 'u3': 3, 'u4': 4}
    names_to_id = {name: labels[name] for name in names_to_level.keys()}
    return {importance: names_to_id[name]
            for name, importance in names_to_level.items()}


def _deprecated_get_importance(task, api):
    ids_to_level = reverse_dictionary(_deprecated_get_importance_ids(api))
    for label_id in task['labels']:
        if label_id in ids_to_level:
            return ids_to_level[label_id]
    return None


def _deprecated_get_urgency(task, api):
    ids_to_level = reverse_dictionary(_deprecated_get_urgency_ids(api))
    for label_id in task['labels']:
        if label_id in ids_to_level:
            return ids_to_level[label_id]
    return None


def _deprecated_parse_duration(title):
    match = re.search(r'<(\d*)h(\d+)m?>', title)
    if match is None:
        return None
    h, m = match.groups()
    return int(h), int(m)


def get_importance(task):
    match = re.search(r'<i(\d)>', task['content'])
    if match is None:
        return None
    return int(match.groups()[0])


def get_urgency(task):
    match = re.search(r'<u(\d)>', task['content'])
    if match is None:
        return None
    return int(match.groups()[0])


def get_duration(task):
    match = re.search(r'<(\d+)m>', task['content'])
    if match is None:
        return None
    return int(match.groups()[0])


def get_notes(task, api):
    # TODO: we go through all the notes at everycall, maybe we should do it once and store in notes_by_task_id dict
    notes = []
    for note in api.notes.all():
        if note['item_id'] == task['id']:
            notes.append(note)
    return notes


def compute_priority(importance, urgency):
    importance_weight = 1.5
    urgency_weight = 1
    return math.ceil((importance_weight * importance + urgency_weight * urgency) / (importance_weight + urgency_weight))


def reverse_dictionary(dic):
    return {v: k for k, v in dic.items()}


def get_priority(task):
    # Note: Keep in mind that very urgent is the priority 1 on clients. So, p1 will return 4 in the API.
    return (4 - task['priority']) + 1


def is_labeled(task):
    importance = get_importance(task)
    urgency = get_urgency(task)
    duration = get_duration(task)
    if importance is None or urgency is None or duration is None:
        return False
    priority = compute_priority(importance, urgency)
    actual_priority = get_priority(task)
    if priority != actual_priority:
        print(f'Warning: actual_priority != computed_priority for task "{task["content"]}"')
        return False
    return True


def label_task(task):
    stripped_content = re.sub(r'<.+>', '', task['content']).strip()
    print(f'"{stripped_content}"')
    importance = int(input('How important is this task? (1-4):'))
    urgency = int(input('How urgent is this task? (1-4):'))
    duration = int(input('How long will it take? (minutes)'))
    priority = compute_priority(importance, urgency)
    # TODO: Store this information in a note?
    task.update(content=f'{stripped_content} <i{importance}> <u{urgency}> <{duration}m>',
                priority=(4 - priority) + 1)


def label_tasks(tasks):
    unlabeled_tasks = [task for task in tasks if not is_labeled(task)]
    if not unlabeled_tasks:
        print('No unlabeled tasks.')
        return
    print('~' * 50)
    print(f'There are {len(unlabeled_tasks)} unlabeled tasks:')
    for i, task in enumerate(unlabeled_tasks):
        print(f'{i}.')
        label_task(task)
        print('\n')
    print('~' * 50)


def sort_tasks(tasks):
    return sorted(tasks, key=lambda task: (get_priority(task), -get_duration(task)))


if __name__ == '__main__':
    api = TodoistAPI(read_token())
    api.reset_state()
    api.sync()
    project_name = input('What project would you like to work on?\n')
    project_id = get_project_id_by_name(project_name, api)
    tasks = get_active_tasks(project_id, api)
    label_tasks(tasks)
    api.commit()
    sorted_tasks = sort_tasks(tasks)
    time_remaining = int(input('How long do you have? (minutes)'))
    selected_tasks = []
    for task in sorted_tasks:
        # TODO: Ask to split tasks that are too long
        duration = get_duration(task)
        if duration < time_remaining:
            print(f'Selected: "{task["content"]}" ({duration}m)')
            selected_tasks.append(task)
            time_remaining -= duration
