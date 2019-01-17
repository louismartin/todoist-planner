from todoist_planner import get_project_name, get_api, commit, get_active_tasks, filter_tasks, get_project_id_by_name


def migrate_task(task):
    for attr_name in task.attribute_names:
        # Set each attribute to itself to call the getters and setters as if it was just labelled
        value = getattr(task, attr_name)
        if value is not None:
            setattr(task, attr_name, value)


if __name__ == '__main__':
    project_name = get_project_name()
    api = get_api()
    project_id = get_project_id_by_name(project_name, api)
    tasks = get_active_tasks(project_id, api)
    tasks = filter_tasks(tasks, api)
    print('Migrating...')
    for task in tasks:
        initial_content = task.content
        migrate_task(task)
        print(f'{initial_content} -> {task.content}')
    answer = input('Commit changes? (y-n)')
    if answer == 'y':
        commit(api)
    else:
        print('Exiting without committing.')
