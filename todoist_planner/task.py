import re

from todoist.models import Item


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

    max_attribute_value = 5
    modified_tasks = {}  # Track modified tasks for batch processing (server limits requests)

    def __init__(self, item):
        super().__init__(item.data, item.api)
        self.content = self['content']  # We will work on content as an attribute instead of an element of a dict
        self.attribute_names = ['importance', 'urgency', 'fun', 'duration']
        for attr_name, attribute in zip(self.attribute_names, [Attribute('<i{}>'),
                                                               Attribute('<u{}>'),
                                                               Attribute('<f{}>'),
                                                               Attribute('<{}m>')]):
            # We set custom properties as static class variables (that's how properties work in python)
            setattr(self.__class__, attr_name, attribute)
        setattr(self.__class__, 'priority', Attribute('<p{}>', prepend=True, callback=False))

    def _register_task_as_modified(self):
        Task.modified_tasks[self['id']] = self

    def attribute_set_callback(self):
        if self.get_priority() is not None:
            # Convert the priority to be between 0 and 9 included
            self.priority = f'{round(self.get_priority() * 100) - 1:02d}'
        self._register_task_as_modified()

    @property
    def stripped_content(self):
        return re.sub(r'<.+?>', '', self.content).strip()

    @stripped_content.setter
    def stripped_content(self, value):
        self.content = re.sub(self.stripped_content, value, self.content)

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
            return None
        # Note: Keep in mind that very urgent is the priority 1 on clients. So, p1 will return 4 in the API.
        return 4 - int(self.get_priority() * 4)

    def is_labeled(self):
        return (None not in [getattr(self, attr_name) for attr_name in self.attribute_names])

    def add_changes_to_queue(self):
        self.update(
            content=self.content,
            priority=self.get_todoist_priority(),
            date_string=None,  # Remove due date
        )

    def label(self):
        print(f'"{self.stripped_content}"')
        ask_texts = {
            'importance': f'How important is this task? (1-{self.max_attribute_value}): ',
            'urgency': f'How urgent is this task? (1-{self.max_attribute_value}): ',
            'fun': f'How fun is this task? (1-{self.max_attribute_value}): ',
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
