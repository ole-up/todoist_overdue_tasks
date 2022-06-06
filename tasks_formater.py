from datetime import datetime
from typing import List

from todoist_api_python.models import Task

from schemas import FormattedTask, ProjectTasks, AssigneeTasks


def get_formatted_tasks(tasks: List[Task]) -> List[AssigneeTasks]:
    """Returns overdue tasks grouped by assignee and projects and sorted by priority """
    overdue_tasks = _get_overdue_tasks(tasks)
    grouping_tasks = _grouping_tasks(overdue_tasks)
    return _sorting_tasks(grouping_tasks)


def _get_overdue_tasks(tasks: List[Task], date_of_overdue: datetime = datetime.today()) -> List[Task]:
    """Returns overdue tasks"""
    return list(filter(lambda x: x.due and datetime.strptime(x.due.date, '%Y-%m-%d') < date_of_overdue, tasks))


def _grouping_tasks(tasks: List[Task]) -> List[AssigneeTasks]:
    """Returns tasks grouped by assignee and project"""
    assignees_tasks = []
    for task in tasks:
        # форматируем задачу
        formatted_task = _fortmating_Task(task)
        # добавляем отформатированную задачу в список
        _add_task_in_assignees_tasks(formatted_task=formatted_task,
                                     assignee_id=task.assignee,
                                     project_id=task.project_id,
                                     assignees_tasks=assignees_tasks)
    return assignees_tasks


def _add_task_in_assignees_tasks(formatted_task: FormattedTask, assignee_id, project_id,
                                 assignees_tasks: List[AssigneeTasks]) -> List[AssigneeTasks]:
    """Adds task in assignee's tasks list"""
    assignees_tasks_keys = _get_assignee_list(assignees_tasks)
    if assignee_id and assignee_id not in assignees_tasks_keys:
        project_tasks = ProjectTasks(project_id=project_id,
                                     tasks=[formatted_task])
        assignee_tasks = AssigneeTasks(assignee_id=assignee_id,
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
    for assignee_tasks in assignees_tasks:
        if assignee_tasks.assignee_id == assignee_id:
            for project in assignee_tasks.projects:
                if project.project_id == project_id:
                    project.tasks.append(formatted_task)
                    break
                else:
                    project.tasks.append(formatted_task)
            break
    return assignees_tasks


def _fortmating_Task(task: Task) -> FormattedTask:
    """Formates Task"""
    return FormattedTask(content=task.content,
                         priority=task.priority,
                         due_date=task.due.date,
                         url=task.url)


def _get_assignee_list(assignees_tasks_list: List[AssigneeTasks]):
    """Returns list of assignee_id from assignee's tasks list"""
    return [assignee.assignee_id for assignee in assignees_tasks_list]


def _sort_key(formatted_task: FormattedTask):
    """Returns key for sorted function"""
    return formatted_task.priority


def _sorting_tasks(assignees_tasks_list: List[AssigneeTasks]):
    """Sort tasks by priority"""
    for assignee in assignees_tasks_list:
        if assignee.projects:
            for project in assignee.projects:
                sorted_tasks = sorted(project.tasks, key=_sort_key, reverse=True)
                project.tasks = sorted_tasks
    return assignees_tasks_list
