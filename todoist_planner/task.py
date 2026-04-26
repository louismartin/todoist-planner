import re

from todoist_planner.utils import ask_question


class Attribute(property):
    '''Custom property method that parses the task content to get an attribute'''

    def __init__(self, str_format, prepend=False, callback=True):
        attr_regex = str_format.format(r'(\d*?)')  # Attibutes have to be integers (for now)

        def set_attribute(task, value):
            if value is None:
                task.content = re.sub(f'{attr_regex}', '', task.content).strip()
            else:
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


class Task:
    """Wrapper around Todoist Task object with attribute parsing."""

    max_attribute_value = 5
    modified_tasks = {}  # Track modified tasks for batch processing

    def __init__(self, todoist_task, api):
        self._todoist_task = todoist_task
        self._api = api
        self.id = todoist_task.id
        self.project_id = todoist_task.project_id
        self.content = todoist_task.content
        self.labels = todoist_task.labels  # List of label names (strings)
        self.parent_id = todoist_task.parent_id
        self._is_deleted = False
        self._is_completed = False

        self.attribute_names = ['importance', 'urgency', 'fun', 'duration']
        for attr_name, attribute in zip(self.attribute_names, [Attribute('<i{}>'),
                                                               Attribute('<u{}>'),
                                                               Attribute('<f{}>'),
                                                               Attribute('<{}m>')]):
            # We set custom properties as static class variables (that's how properties work in python)
            setattr(self.__class__, attr_name, attribute)
        setattr(self.__class__, 'priority', Attribute('<p{}>', prepend=True, callback=False))

    def _register_task_as_modified(self):
        Task.modified_tasks[self.id] = self

    def attribute_set_callback(self):
        if self.get_priority() is not None:
            # Convert the priority to be between 0 and 9 included
            self.priority = f'{round(self.get_priority() * 100) - 1:02d}'
        else:
            self.priority = None
        self._register_task_as_modified()

    @property
    def stripped_content(self):
        return re.sub(r'<.+?>', '', self.content).strip()

    @stripped_content.setter
    def stripped_content(self, value):
        self.content = re.sub(re.escape(self.stripped_content), value, self.content)
        self._register_task_as_modified()

    def clear_attributes(self):
        for attr_name in self.attribute_names:
            setattr(self, attr_name, None)

    def get_priority(self):
        if None in [self.importance, self.urgency, self.fun, self.duration]:
            return None
        importance_weight = 1.5
        urgency_weight = 1
        fun_weight = 0.5
        duration_weight = 0.5
        weighted_sum = (importance_weight * (self.importance / self.max_attribute_value)
                        + urgency_weight * (self.urgency / self.max_attribute_value)
                        + fun_weight * (self.fun / self.max_attribute_value)
                        + duration_weight * min(self.duration / 300, 1) ** (1/2))
        priority = weighted_sum / (importance_weight + urgency_weight + fun_weight + duration_weight)
        assert priority <= 1
        return priority

    def get_todoist_priority(self):
        if self.get_priority() is None:
            return 1
        # Note: Keep in mind that very urgent is the priority 1 on clients. So, p1 will return 4 in the API.
        return 4 - int(self.get_priority() * 4)

    def is_labeled(self):
        return (None not in [getattr(self, attr_name) for attr_name in self.attribute_names])

    def save(self, api):
        """Save changes to the task via API."""
        if self._is_deleted or self._is_completed:
            return
        api.update_task(
            task_id=self.id,
            content=self.content,
            priority=self.get_todoist_priority(),
        )

    def complete(self, api):
        """Mark task as completed."""
        api.complete_task(task_id=self.id)
        self._is_completed = True
        # Remove from modified tasks since it's completed
        Task.modified_tasks.pop(self.id, None)

    def delete(self, api):
        """Delete the task."""
        api.delete_task(task_id=self.id)
        self._is_deleted = True
        # Remove from modified tasks since it's deleted
        Task.modified_tasks.pop(self.id, None)

    def add_subtask(self, content, api):
        """Add a subtask under this task."""
        api.add_task(
            content=content,
            project_id=self.project_id,
            parent_id=self.id,
        )

    def split(self, api):
        i = 0
        while True:
            content = input(f'\tSubtask {i+1} content: ')
            self.add_subtask(content, api)
            i += 1
            if ask_question('Would you like to add another subtask?', possible_answers=['y', 'n']) == 'n':
                break
