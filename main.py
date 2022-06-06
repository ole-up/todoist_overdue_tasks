from pathlib import Path

import config
from email_sender import send_email
from exceptions import ApiServiceError, FormattingError, EmailError, SaverError
from saver import save_tasks, HTMLFileTasksStorage
from tasks_formater import get_formatted_tasks
from todoist_api_service import get_tasks


def main():
    try:
        tasks = get_tasks()
    except ApiServiceError:
        print('Не удалось получить задачи')
        exit(1)
    try:
        formatted_tasks = get_formatted_tasks(tasks)
    except FormattingError:
        print('Не удалось обработать список задач')
        exit(1)
    try:
        save_tasks(formatted_tasks, HTMLFileTasksStorage(Path.cwd() / 'tasks.html'))
    except SaverError:
        print('Не удалось сохранить задачи в файл')
        exit(1)
    try:
        send_email("tasks.html", config.SENDER_EMAIL, config.RECEIVER_EMAIL, config.SUBJECT, config.SMTP_SERVER,
                   config.SMTP_PORT, config.SENDER_PASSWORD)
    except EmailError:
        print(f'Не удалось отправить отчет на электронную почту {config.RECEIVER_EMAIL}')
        exit(1)


if __name__ == "__main__":
    main()
