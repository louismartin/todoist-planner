from todoist.api import TodoistAPI

from todoist_planner import read_token, commit, get_active_tasks, filter_tasks, get_project_id_by_name


def migrate_task(task):
    for attr_name in task.attribute_names:
        # Set each attribute to itself to call the getters and setters as if it was just labelled
        value = getattr(task, attr_name)
        if value is not None:
            setattr(task, attr_name, value)


if __name__ == '__main__':
    print('Welcome to Todoist planner!')
    api = TodoistAPI(read_token())
    project_name = input('What project would you like to migrate? ')
    api.reset_state()
    api.sync()
    project_id = get_project_id_by_name(project_name, api)
    tasks = get_active_tasks(project_id, api)
    tasks = filter_tasks(tasks, api)
    print('Migrating...')
    for task in tasks:
        initial_content = task.content
        migrate_task(task)
        print(f'{initial_content} -> {task.content}')
    commit(api)
