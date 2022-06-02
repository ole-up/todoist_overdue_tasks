from dataclasses import dataclass


@dataclass
class FormattedTask:
    content: str
    priority: int
    due_date: str
    url: str
