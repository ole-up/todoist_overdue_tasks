from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task

import config

api = TodoistAPI(config.API_TOKEN)


def get_tasks() -> list[Task]:
    """Returns tasks list"""
    try:
        tasks = api.get_tasks()
        return tasks
    except Exception as error:
        print(error)


def get_project_name(project_id):
    """Returns project name by id"""
    try:
        project = api.get_project(project_id)
        return project.name
    except Exception as error:
        print(f'Название проекта не получено. Ошибка: {error}')
        return project_id


if __name__ == "__main__":
    print(get_tasks())
