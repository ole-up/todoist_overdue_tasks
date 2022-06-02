from pathlib import Path

import config
from email_sender import send_email
from saver import save_tasks, HTMLFileTasksStorage
from tasks_formater import get_formatted_tasks
from todoist_api_service import get_tasks


def main():
    tasks = get_tasks()
    formatted_tasks = get_formatted_tasks(tasks)
    save_tasks(formatted_tasks, HTMLFileTasksStorage(Path.cwd() / 'tasks.html'))
    send_email("tasks.html", config.SENDER_EMAIL, config.RECEIVER_EMAIL, config.SUBJECT, config.SMTP_SERVER,
                 config.SMTP_PORT, config.SENDER_PASSWORD)


if __name__ == "__main__":
    main()
