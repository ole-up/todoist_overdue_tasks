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
    project_id: int
    tasks: List[FormattedTask]


@dataclass
class AssigneeTasks(TypedDict):
    assignee_id: int
    projects: List[ProjectTasks]
