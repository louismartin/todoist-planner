from datetime import datetime, timedelta
import math
from pathlib import Path
import re
import sys
import time

from todoist.api import TodoistAPI
from todoist.models import Item


REPO_DIR = Path(__file__).resolve().parent
token_filepath = REPO_DIR / 'token'


class Attribute(property):
    '''Custom property method that parses the task content to get an attribute'''

    def __init__(self, str_format):
        attr_regex = str_format.format(r'(\d*)')  # Attibutes have to be integers (for now)

        def set_attribute(task, value):
            value = int(value)
            if re.search(attr_regex, task['content']) is None:
                task['content'] += ' ' + str_format.format('')
            task['content'] = re.sub(attr_regex, str_format.format(value), task['content'])

        def get_attribute(task):
            match = re.search(attr_regex, task['content'])
            if match is None:
                return None
            return int(match.groups()[0])

        # https://docs.python.org/3/library/functions.html#property
        super().__init__(get_attribute, set_attribute)


class Task(Item):

    def __init__(self, item):
        super().__init__(item.data, item.api)
        self.attributes = ['importance', 'urgency', 'duration']
        for attr_name, attribute in zip(self.attributes, [Attribute('<i{}>'),
                                                          Attribute('<u{}>'),
                                                          Attribute('<{}m>')]):
            # We set custom properties as static class variables (that's how properties work in python)
            setattr(self.__class__, attr_name, attribute)

    @property
    def stripped_content(self):
        return re.sub(r'<.+>', '', self['content']).strip()

    @stripped_content.setter
    def stripped_content(self, value):
        self['content'] = re.sub(self.stripped_content, value, self['content'])

    @property
    def priority(self):
        if None in [self.importance, self.urgency]:
            return None
        importance_weight = 1.5
        urgency_weight = 1
        return (importance_weight * self.importance + urgency_weight * self.urgency) / (importance_weight + urgency_weight)  # noqa: E501

    @property
    def todoist_priority(self):
        if self.priority is None:
            return
        max_priority = 8
        # Note: Keep in mind that very urgent is the priority 1 on clients. So, p1 will return 4 in the API.
        return (4 - math.ceil(self.priority / max_priority * 4)) + 1

    def is_labeled(self):
        return (None not in [getattr(self, attr_name) for attr_name in self.attributes])

    def update_attributes(self):
        self.update(content=self['content'], priority=self.todoist_priority)

    def label(self):
        print(f'"{self.stripped_content}"')
        ask_texts = {
            'importance': 'How important is this task? (1-8): ',
            'urgency': 'How urgent is this task? (1-8): ',
            'duration': 'How long will this task take? (minutes): ',
        }
        for attr_name in self.attributes:
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
        self.update_attributes()


def ask_for_token():
    text = 'Please copy your todoist API token.'
    text += '\nYou can find it in "Todoist Settings -> Integrations -> API token":'
    text += '\nhttps://en.todoist.com/prefs/integrations\n'
    token = input(text)
    with token_filepath.open('w') as f:
        f.write(token + '\n')


def read_token():
    if not token_filepath.exists():
        ask_for_token()
    with token_filepath.open('r') as f:
        token = f.read().rstrip('\n')
    if token == '':
        ask_for_token()
    return token


def get_project_id_by_name(name, api):
    for project in api.projects.all():
        if project['name'].lower() == name.lower():
            return project['id']


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
        api.commit()
        print('\n')
    print('~' * 50)


def sort_tasks(tasks):
    return sorted(tasks, key=lambda task: (task.priority, -task.duration))


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
    api = TodoistAPI(read_token())
    project_name = input('What project would you like to work on? ')
    api.reset_state()
    api.sync()
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
