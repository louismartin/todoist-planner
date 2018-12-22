from collections import namedtuple, OrderedDict
import math
from pathlib import Path
import re
import sys

from todoist.api import TodoistAPI


__file__ = '/Users/louismartin/dev/todoist-planner/Untitled.ipynb'
REPO_DIR = Path(__file__).resolve().parent
token_filepath = REPO_DIR / 'token'
Attribute = namedtuple('Attribute', ['parse_regex', 'str_format', 'ask_text'])
attributes = OrderedDict({
        'importance': Attribute(r'<i(\d)>', '<i{}>', 'How important is this task? (1-4): '),
        'urgency': Attribute(r'<u(\d)>', '<u{}>', 'How urgent is this task? (1-4): '),
        'duration': Attribute(r'<(\d+)m>', '<{}m>', 'How long will this task take? (minutes): '),
})


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
    for task in api.items.all():
        if task['project_id'] != project_id:
            continue
        if task['checked']:
            continue
        tasks.append(task)
    return tasks


def get_labels(api):
    return {label['name']: label['id'] for label in api.labels.all()}


def parse_attribute(task, parse_regex):
    match = re.search(parse_regex, task['content'])
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
    return (importance_weight * importance + urgency_weight * urgency) / (importance_weight + urgency_weight)


def compute_todoist_priority(importance, urgency):
    priority = math.ceil(compute_priority(importance, urgency))
    # Note: Keep in mind that very urgent is the priority 1 on clients. So, p1 will return 4 in the API.
    return (4 - priority) + 1


def reverse_dictionary(dic):
    return {v: k for k, v in dic.items()}


def is_labeled(task):
    attribute_values = {attr_name: parse_attribute(task, attribute.parse_regex)
                        for attr_name, attribute in attributes.items()}
    if None in attribute_values.values():
        return False
    # TODO: this should be done somewhere else
    # Set to matching priority
    task.update(priority=compute_todoist_priority(attribute_values['importance'], attribute_values['urgency']))
    return True


def label_task(task):
    stripped_content = re.sub(r'<.+>', '', task['content']).strip()
    print(f'"{stripped_content}"')
    attribute_values = {}
    for attr_name, attribute in attributes.items():
        current_value = parse_attribute(task, attribute.parse_regex)
        ask_text = attribute.ask_text
        if current_value is not None:
            # TODO: Remove this value if user inputs something
            ask_text += str(current_value)
        value = input(ask_text)
        # TODO: Better way to handle this case
        if value == '':   # User just validated current value
            value = current_value
        elif value == 'n':  # next
            return
        elif value == 'd':  # delete
            task.delete()
            return
        elif value == 'e':  # edit
            task.update(content=input('New task content: \n'))
            label_task(task)
            # TODO: Maybe we should keep the tasks current attribute values
            # attributes)
            return
        elif value == 'c':  # complete
            task.complete()
            return
        attribute_values[attr_name] = int(value)
    attributes_str = ' '.join([attributes[attr_name].str_format.format(value)
                               for attr_name, value in attribute_values.items()])
    task.update(content=f'{stripped_content} {attributes_str}',
                priority=compute_todoist_priority(attribute_values['importance'], attribute_values['urgency']))


def label_tasks(tasks, api):
    unlabeled_tasks = [task for task in tasks if not is_labeled(task)]
    if not unlabeled_tasks:
        print('No unlabeled tasks.')
        return
    print('~' * 50)
    print(f'There are {len(unlabeled_tasks)} unlabeled tasks:\n')
    for i, task in enumerate(unlabeled_tasks):
        sys.stdout.write(f'{i+1}.')
        label_task(task)
        api.commit()
        print('\n')
    print('~' * 50)


def sort_tasks(tasks):
    importance = parse_attribute(task, attributes['importance'].parse_regex)
    urgency = parse_attribute(task, attributes['urgency'].parse_regex)
    duration = parse_attribute(task, attributes['duration'].parse_regex)
    return sorted(tasks, key=lambda task: (compute_priority(importance, urgency), -duration))


def filter_tasks(tasks, api):
    def have_elements_in_common(list1, list2):
        return len(set(list1)) + len(set(list2)) != len(set(list1 + list2))

    # TODO: Specific to my needs, a better solution would be to create a new label @no-planner and apply it to skipped
    # tasks during labelling
    labels = get_labels(api)
    excluded_label_names = ['onhold', 'medecin', 'orsay', 'albert']
    excluded_label_ids = [labels[label_name] for label_name in excluded_label_names]
    return [task for task in tasks if not have_elements_in_common(task['labels'], excluded_label_ids)]


if __name__ == '__main__':
    print('Welcome to Todoist planner!')
    api = TodoistAPI(read_token())
    api.reset_state()
    api.sync()
    project_name = input('What project would you like to work on? ')
    project_id = get_project_id_by_name(project_name, api)
    tasks = get_active_tasks(project_id, api)
    tasks = filter_tasks(tasks, api)
    label_tasks(tasks, api)
    sorted_tasks = sort_tasks(tasks)
    time_remaining = int(input('How long do you have? (minutes): '))
    selected_tasks = []
    for task in sorted_tasks:
        # TODO: Ask to split tasks that are too long
        duration = parse_attribute(task, attributes['duration'].parse_regex)
        if duration <= time_remaining:
            print(f'Selected: "{task["content"]}" ({duration}m)')
            selected_tasks.append(task)
            time_remaining -= duration
