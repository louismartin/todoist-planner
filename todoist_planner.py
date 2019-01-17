from datetime import datetime, timedelta
import math
from pathlib import Path
import re
import sys
import time

from tqdm import tqdm

from todoist.api import TodoistAPI
from todoist.models import Item


REPO_DIR = Path(__file__).resolve().parent
TOKEN_FILEPATH = REPO_DIR / 'token'
MODIFIED_TASKS = {}  # Track modified tasks for batch processing (server limits requests


def register_task_as_modified(task):
    global MODIFIED_TASKS  # Not necessary but more explicit
    MODIFIED_TASKS[task['id']] = task


class Attribute(property):
    '''Custom property method that parses the task content to get an attribute'''

    def __init__(self, str_format, prepend=False, callback=True):
        attr_regex = str_format.format(r'(\d*?)')  # Attibutes have to be integers (for now)

        def set_attribute(task, value):
            value = int(value)
            if re.search(attr_regex, task.content) is None:
                if prepend:
                    task.content = str_format.format('') + ' ' + task.content
                else:
                    task.content += ' ' + str_format.format('')
            task.content = re.sub(attr_regex, str_format.format(value), task.content)
            if callback:
                task.attribute_set_callback()

        def get_attribute(task):
            match = re.search(attr_regex, task.content)
            if match is None:
                return None
            return int(match.groups()[0])

        # https://docs.python.org/3/library/functions.html#property
        super().__init__(get_attribute, set_attribute)


class Task(Item):

    max_attribute_value = 8

    def __init__(self, item):
        super().__init__(item.data, item.api)
        self.content = self['content']  # We will work on content as an attribute instead of an element of a dict
        self.attribute_names = ['importance', 'urgency', 'duration']
        for attr_name, attribute in zip(self.attribute_names, [Attribute('<i{}>'),
                                                               Attribute('<u{}>'),
                                                               Attribute('<{}m>')]):
            # We set custom properties as static class variables (that's how properties work in python)
            setattr(self.__class__, attr_name, attribute)
        setattr(self.__class__, 'priority', Attribute('<p{}>', prepend=True, callback=False))

    def attribute_set_callback(self):
        if self.get_priority() is not None:
            # Convert the priority to be between 0 and 9 included
            self.priority = f'{round(self.get_priority() * 100) - 1:02d}'
        register_task_as_modified(self)

    @property
    def stripped_content(self):
        return re.sub(r'<.+?>', '', self.content).strip()

    @stripped_content.setter
    def stripped_content(self, value):
        self.content = re.sub(self.stripped_content, value, self.content)

    def get_priority(self):
        if None in [self.importance, self.urgency]:
            return None
        importance_weight = 1.5
        urgency_weight = 1
        duration_weight = 0.5
        weighted_sum = (importance_weight * (self.importance / self.max_attribute_value)
                        + urgency_weight * (self.urgency / self.max_attribute_value)
                        + duration_weight * min(self.duration / 300, 1))
        priority = weighted_sum / (importance_weight + urgency_weight + duration_weight)
        assert priority <= 1
        return priority

    def get_todoist_priority(self):
        if self.get_priority() is None:
            return
        # Note: Keep in mind that very urgent is the priority 1 on clients. So, p1 will return 4 in the API.
        return (4 - math.ceil(self.get_priority() * 4)) + 1

    def is_labeled(self):
        return (None not in [getattr(self, attr_name) for attr_name in self.attribute_names])

    def update_attributes(self):
        self.update(content=self.content, priority=self.get_todoist_priority())

    def label(self):
        print(f'"{self.stripped_content}"')
        ask_texts = {
            'importance': f'How important is this task? (1-{self.max_attribute_value}): ',
            'urgency': f'How urgent is this task? (1-{self.max_attribute_value}): ',
            'duration': 'How long will this task take? (minutes): ',
        }
        for attr_name in self.attribute_names:
            current_value = getattr(self, attr_name)
            ask_text = ask_texts[attr_name]
            if current_value is not None:
                # TODO: Remove this value if user inputs something
                ask_text += str(current_value)
            new_value = input(ask_text)
            # TODO: Better way to handle this cases
            if new_value == '':   # User just validated current value
                new_value = current_value
            elif new_value == 'n':  # next
                return
            elif new_value == 'd':  # delete
                self.delete()
                return
            elif new_value == 'e':  # edit
                self.stripped_content = input('New task content: \n')
                self.label()
                return
            elif new_value == 'c':  # complete
                self.complete()
                return
            setattr(self, attr_name, new_value)

    def add_subtask(self, content, api):
        # This will add a command to api.queue which will be committed in the next commit()
        api.items.add(content,
                      project_id=self['project_id'],
                      item_order=self['item_order'],
                      indent=self['indent'] + 1)


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
                yield batch
                batch = []
        if len(batch) > 0:
            yield batch

    # Create one command for each modified task
    global MODIFIED_TASKS
    for task in list(MODIFIED_TASKS.values()):
        task.update_attributes()
    MODIFIED_TASKS = {}
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
    return sorted(tasks, key=lambda task: (task.get_priority(), -task.duration))


def filter_tasks(tasks, api):
    def have_elements_in_common(list1, list2):
        return len(set(list1)) + len(set(list2)) != len(set(list1 + list2))

    # TODO: Specific to my needs, a better solution would be to create a new label @no-planner and apply it to skipped
    # tasks during labelling
    labels = get_labels(api)
    excluded_label_names = ['onhold', 'medecin', 'orsay', 'albert']
    excluded_label_ids = [labels[label_name] for label_name in excluded_label_names]
    return [task for task in tasks if not have_elements_in_common(task['labels'], excluded_label_ids)]


def seconds_to_human_readable(seconds, display_seconds=True):
    d = datetime(1, 1, 1) + timedelta(seconds=int(seconds))
    human_readable = ''
    if display_seconds:
        human_readable = f'{d.second}s'
    if seconds >= 60:
        human_readable = f'{d.minute}m {human_readable}'
    if seconds >= 3600:
        human_readable = f'{d.hour}h {human_readable}'
    if seconds >= 86400:
        human_readable = f'{d.day-1}d {human_readable}'
    return human_readable.strip()


def start_timer(minutes):
    start_time = time.time()
    elapsed = 0
    while elapsed < (minutes * 60):
        elapsed = time.time() - start_time
        sys.stdout.write(f'\rElapsed: {seconds_to_human_readable(elapsed)}')
        time.sleep(1)


if __name__ == '__main__':
    print('Welcome to Todoist planner!')
    project_name = get_project_name()
    api = get_api()
    project_id = get_project_id_by_name(project_name, api)
    tasks = get_active_tasks(project_id, api)
    tasks = filter_tasks(tasks, api)
    label_tasks(tasks, api)
    # Reload active tasks (tasks may have been completed or deleted)
    # TODO: find a better way to handle this case
    tasks = get_active_tasks(project_id, api)
    tasks = filter_tasks(tasks, api)
    sorted_tasks = sort_tasks(tasks)
    time_available = int(input('How long do you have? (minutes): '))
    time_remaining = time_available
    selected_tasks = []
    for task in sorted_tasks:
        # TODO: Ask to split tasks that are too long
        if task.duration <= time_remaining:
            print(f'Selected: "{task["content"]}" ({task.duration}m)')
            selected_tasks.append(task)
            time_remaining -= task.duration
    start_timer(time_available)
