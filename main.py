from todoist_planner.utils import (get_project_name, get_api, get_project_id_by_name, get_active_tasks, filter_tasks,
                                   label_tasks, sort_tasks, start_timer)


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
