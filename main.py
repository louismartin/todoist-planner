from todoist_planner.utils import (get_project_name, get_api, get_project_id_by_name, get_active_tasks, filter_tasks,
                                   label_tasks, sort_tasks, ask_question, commit)


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
    print('Tasks:')
    for task in sort_tasks(tasks):
        print('\n' + task.content + '\n')
        answer = ask_question('Type c to complete, n for next', possible_answers=['c', 'n'])
        if answer == 'c':
            task.complete()
            commit(api)
        print('\n')
