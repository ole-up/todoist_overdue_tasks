from pathlib import Path, WindowsPath
from typing import Protocol, List

from jinja2 import Environment, FileSystemLoader

from schemas import AssigneeTasks


class TasksStorage(Protocol):
    """Interface for any storage saving tasks"""

    def save(self, tasks) -> None:
        raise NotImplementedError


class HTMLFileTasksStorage(TasksStorage):
    """Store tasks in HTML file"""

    def __init__(self, file: Path | WindowsPath):
        self._file = file

    def save(self, tasks: List[AssigneeTasks]) -> None:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report.html')
        output_from_parsed_template = template.render(assignees_tasks_list=tasks)
        with open(self._file, "w", encoding='utf-8') as f:
            f.write(output_from_parsed_template)
        

def save_tasks(tasks, storage: TasksStorage):
    """Saves weather in the storage"""
    storage.save(tasks)
