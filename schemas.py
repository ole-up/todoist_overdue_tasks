from dataclasses import dataclass
from typing import TypedDict, List


@dataclass
class FormattedTask:
    content: str
    priority: int
    due_date: str
    url: str


@dataclass
class ProjectTasks:
    project_name: str
    tasks: List[FormattedTask]


@dataclass
class AssigneeTasks:
    assignee_name: str
    projects: List[ProjectTasks]
