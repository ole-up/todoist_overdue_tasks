from datetime import datetime
from typing import List

from todoist_api_python.models import Task

import config
import todoist_api_service
from exceptions import FormattingError
from schemas import FormattedTask, ProjectTasks, AssigneeTasks


def get_formatted_tasks(tasks: List[Task]) -> List[AssigneeTasks]:
    """Returns overdue tasks grouped by assignee and projects and sorted by priority """
    try:
        overdue_tasks = _get_overdue_tasks(tasks)
        tasks_with_assignee = _get_tasks_with_assignee(overdue_tasks)
        grouped_tasks = _grouping_tasks(tasks_with_assignee)
        sorted_tasks = _sorting_tasks(grouped_tasks)
        return sorted_tasks
    except Exception:
        raise FormattingError


def _get_overdue_tasks(tasks: List[Task], date_of_overdue: datetime = datetime.now()) -> List[Task]:
    """Returns overdue tasks"""
    return list(filter(lambda x: x.due and datetime.strptime(x.due.date, '%Y-%m-%d').date() < date_of_overdue.date(), tasks))


def _get_tasks_with_assignee(tasks: List[Task], exclude_assignee=True) -> List[Task]:
    """Returns task with assignee"""
    if exclude_assignee:
        return list(filter(lambda x: x.assignee and x.assignee not in config.EXCLUDE_ASSIGNEES, tasks))
    else:
        return list(filter(lambda x: x.assignee, tasks))


def _grouping_tasks(tasks: List[Task]) -> List[AssigneeTasks]:
    """Returns tasks grouped by assignee and project"""
    assignees_tasks = []
    for task in tasks:
        # форматируем задачу
        formatted_task = _fortmating_Task(task)
        # добавляем отформатированную задачу в список
        assignees_tasks = _add_task_in_assignees_tasks(formatted_task=formatted_task,
                                                       assignee_id=task.assignee,
                                                       project_id=task.project_id,
                                                       assignees_tasks=assignees_tasks)
    return assignees_tasks


def _add_task_in_assignees_tasks(formatted_task: FormattedTask, assignee_id, project_id,
                                 assignees_tasks: List[AssigneeTasks]) -> List[AssigneeTasks]:
    """Adds task in assignee's tasks list"""
    assignees_tasks_keys = _get_assignee_list(assignees_tasks)
    if assignee_id:
        assignee_name = _get_assignee_name(assignee_id)
        if assignee_name not in assignees_tasks_keys:
            project_tasks = ProjectTasks(project_name=todoist_api_service.get_project_name(project_id),
                                         tasks=[formatted_task])
            assignee_tasks = AssigneeTasks(assignee_name=assignee_name,
                                           projects=[project_tasks])
            assignees_tasks.append(assignee_tasks)
            return assignees_tasks
        else:
            return _add_task_in_project(formatted_task=formatted_task,
                                        assignee_id=assignee_id,
                                        project_id=project_id,
                                        assignees_tasks=assignees_tasks)


def _add_task_in_project(formatted_task: FormattedTask, assignee_id, project_id,
                         assignees_tasks: List[AssigneeTasks]) -> List[AssigneeTasks]:
    """Adds task in project's tasks list"""
    assignee_name = _get_assignee_name(assignee_id)
    project_name = todoist_api_service.get_project_name(project_id)
    for assignee_tasks in assignees_tasks:
        if assignee_tasks.assignee_name == assignee_name:
            for project in assignee_tasks.projects:
                if project.project_name == project_name:
                    project.tasks.append(formatted_task)
                    break
                else:
                    project.tasks.append(formatted_task)
            break
    return assignees_tasks


def _get_assignee_name(assignee_id: int) -> str:
    return config.ASSIGNEES[
        assignee_id] if assignee_id in config.ASSIGNEES.keys() else f'Неизвестный ответственный {assignee_id}'


def _fortmating_Task(task: Task) -> FormattedTask:
    """Formates Task"""
    return FormattedTask(content=task.content,
                         priority=task.priority,
                         due_date=task.due.date,
                         url=task.url)


def _get_assignee_list(assignees_tasks_list: List[AssigneeTasks]) -> List[str]:
    """Returns list of assignee_id from assignee's tasks list"""
    return [assignee.assignee_name for assignee in assignees_tasks_list]


def _sort_key(formatted_task: FormattedTask):
    """Returns key for sorted function"""
    return formatted_task.priority


def _sorting_tasks(assignees_tasks_list: List[AssigneeTasks]) -> List[AssigneeTasks]:
    """Sort tasks by priority"""
    for assignee in assignees_tasks_list:
        if assignee.projects:
            for project in assignee.projects:
                sorted_tasks = sorted(project.tasks, key=_sort_key, reverse=True)
                project.tasks = sorted_tasks
    return assignees_tasks_list


if __name__ == "__main__":
    from pprint import pprint

    from tasks import tasks

    overdue_tasks = _get_overdue_tasks(tasks)
    print("Просроченные задачи:")
    pprint(overdue_tasks)
    print(100 * '*')
    print("Задачи с назначенным исполнителем:")
    tasks_with_assignee = _get_tasks_with_assignee(overdue_tasks)
    pprint(tasks_with_assignee)
    print(100 * '*')
    print("Сгруппированные задачи:")
    grouped_task = _grouping_tasks(tasks_with_assignee)
    pprint(grouped_task)
