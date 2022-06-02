from pathlib import Path, WindowsPath
from typing import Protocol

import config
import html_template
from todoist_api_service import get_project_name


class TasksStorage(Protocol):
    """Interface for any storage saving tasks"""

    def save(self, tasks) -> None:
        raise NotImplementedError


class HTMLFileTasksStorage(TasksStorage):
    """Store tasks in HTML file"""

    def __init__(self, file: Path | WindowsPath):
        self._file = file

    def save(self, tasks) -> None:
        with open(self._file, 'w') as f:
            f.write(html_template.BODY_START)
            for assignee, projects in tasks.items():
                if projects:
                    f.write(f'<h2 style="color: #008000">Исполнитель: {config.ASSIGNEES[assignee]}</h2>')
                    for project_id, tasks in projects.items():
                        f.write(f'<h3 style="color: #DC143C">Проект: {get_project_name(project_id)}</h3>')
                        f.write(html_template.TABLE_HEADER)
                        for task in tasks:
                            f.write(
                                f'<tr><td style="text-align: left; width: 300px">{task.content}</td><td style="text-align: center; width: 100px">{task.due_date}</td><td style="text-align: center; width: 100px">{task.priority}</td><td style="width: 300px;"><a href="{task.url}">{task.url}</a></td></tr>')
                        f.write(html_template.TABEL_END_TAG)
                    f.write('<br><hr><br>')
            f.write(html_template.BODY_END)


def save_tasks(tasks, storage: TasksStorage):
    """Saves weather in the storage"""
    storage.save(tasks)
