from pathlib import Path
import sys
import time

from tqdm import tqdm
from todoist.api import TodoistAPI

from todoist_planner.task import Task


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
    api = TodoistAPI(read_token())
    api.reset_state()
    api.sync()
    return api


def commit(api):
    def sync_commands_with_retry(commands, api):
        def is_valid(response):
            if type(response) == str:
                print(f'Response is a string ({response}), not valid.')
                return False
            if response.get('error_tag', None) == 'LIMITS_REACHED':
                # Todoist API does not accept more than 50 requests per minute
                print(f'Limits reached.')
                return False
            assert all(v == 'ok' for _, v in response['sync_status'].items()), response
            return True

        response = api.sync(commands)
        sleep_time = 5
        while not is_valid(response):
            print(f'Retrying in {sleep_time} seconds.')
            time.sleep(sleep_time)
            sleep_time *= 2
            response = api.sync(commands)

    def batch_commands(commands):
        batch = []
        while len(commands) > 0:
            batch.append(commands.pop())
            if len(batch) == 100:
                # Todoist's API does not accept more than 100 commands at once
                yield batch
                batch = []
        if len(batch) > 0:
            yield batch

    # Create one command for each modified task
    for task in list(Task.modified_tasks.values()):
        task.add_changes_to_queue()
    Task.modified_tasks = {}
    # Group commands by batches of 100
    pbar = tqdm(total=len(api.queue), desc='Committing')
    for batch in batch_commands(api.queue):
        sync_commands_with_retry(batch, api)
        pbar.update(len(batch))
    assert len(api.queue) == 0


def get_project_id_by_name(name, api):
    for project in api.projects.all():
        if project['name'].lower() == name.lower():
            return project['id']
    raise NameError(f'Project {name} cannot be found.')


def get_active_tasks(project_id, api):
    tasks = []
    for item in api.items.all():
        if item['project_id'] != project_id:
            continue
        if item['checked']:
            continue
        tasks.append(Task(item))
    return tasks


def get_labels(api):
    return {label['name']: label['id'] for label in api.labels.all()}


def get_notes(task, api):
    # TODO: we go through all the notes at everycall, maybe we should do it once and store in notes_by_task_id dict
    notes = []
    for note in api.notes.all():
        if note['item_id'] == task['id']:
            notes.append(note)
    return notes


def reverse_dictionary(dic):
    return {v: k for k, v in dic.items()}


def label_tasks(tasks, api):
    unlabeled_tasks = [task for task in tasks if not task.is_labeled()]
    if not unlabeled_tasks:
        print('No unlabeled tasks.')
        return
    print('~' * 50)
    print(f'There are {len(unlabeled_tasks)} unlabeled tasks:\n')
    for i, task in enumerate(unlabeled_tasks):
        sys.stdout.write(f'{i+1}.')
        task.label()
        print('\n')
    commit(api)
    print('~' * 50)


def sort_tasks(tasks):
    return sorted(tasks, key=lambda task: task.get_priority())


def filter_tasks(tasks, api):
    def have_elements_in_common(list1, list2):
        return len(set(list1)) + len(set(list2)) != len(set(list1 + list2))

    # TODO: Specific to my needs, a better solution would be to create a new label @no-planner and apply it to skipped
    # tasks during labelling
    labels = get_labels(api)
    excluded_label_names = ['onhold', 'medecin', 'orsay', 'albert']
    excluded_label_ids = [labels[label_name] for label_name in excluded_label_names]
    return [task for task in tasks if not have_elements_in_common(task['labels'], excluded_label_ids)]
