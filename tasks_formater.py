from datetime import datetime
from typing import List

from todoist_api_python.models import Task, Due

from schemas import FormattedTask


def get_formatted_tasks(tasks: List[Task]):
    """Returns overdue tasks grouped by assignee and projects and sorted by priority """
    overdue_tasks = _get_overdue_tasks(tasks)
    grouping_tasks = _grouping_tasks(overdue_tasks)
    return _sorting_tasks(grouping_tasks)


def _get_overdue_tasks(tasks: List[Task], date_of_overdue: datetime = datetime.today()) -> List[Task]:
    """Returns overdue tasks"""
    return list(filter(lambda x: x.due and datetime.strptime(x.due.date, '%Y-%m-%d') < date_of_overdue, tasks))


def _grouping_tasks(tasks: List[Task]):
    """Returns tasks grouped by assignee and project"""
    assignees_tasks_dict = {}
    for task in tasks:
        formatted_task = FormattedTask(content=task.content,
                                       priority=task.priority,
                                       due_date=task.due.date,
                                       url=task.url)
        # проверяем наличие назначенного ответственного
        if task.assignee:
            # проверяем есть ли уже такой ответственный в словаре
            if task.assignee not in assignees_tasks_dict.keys():
                # если нет, добавляем проект и задачу в словарь
                assignees_tasks_dict.update({task.assignee: {task.project_id: [formatted_task]}})
            else:
                # если есть, берем список проектов и проверяем есть ли такой проект у ответственного
                projects = assignees_tasks_dict.pop(task.assignee)
                if task.project_id in projects.keys():
                    project_tasks = projects.pop(task.project_id)
                    project_tasks.append(formatted_task)
                    projects.update({task.project_id: project_tasks})
                    assignees_tasks_dict.update({task.assignee: projects})
                # если проекта нет, добавляем его и задачу
                else:
                    projects.update({task.project_id: [formatted_task]})

    return assignees_tasks_dict


def _sort_key(formatted_task: FormattedTask):
    """Returns key for sorted function"""
    return formatted_task.priority

def _sorting_tasks(tasks_dict):
    """Sort tasks by priority"""
    for assignee, projects in tasks_dict.items():
        if projects:
            for project_id, tasks in projects.items():
                sorted_tasks = sorted(tasks, key=_sort_key, reverse=True)
                projects.update({project_id: sorted_tasks})
    return tasks_dict
