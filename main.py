import os
import time
import requests
from datetime import datetime

USERS_URL = 'https://json.medrocket.ru/users'
TASKS_URL = 'https://json.medrocket.ru/todos'


def get_users():
    response = requests.get(USERS_URL)
    return response.json()


def get_tasks(user):
    params = {'userId': user['id']}
    response = requests.get(TASKS_URL, params=params)
    return response.json()


def generate_report(user):
    tasks = get_tasks(user)
    num_tasks = len(tasks)

    completed = [t for t in tasks if t['completed']]
    pending = [t for t in tasks if not t['completed']]

    company = user['company']['name']
    name = f"{user['name']} <{user['email']}>"

    now = datetime.now().strftime('%d.%m.%Y %H:%M')

    report = f"""
# Отчёт для {company}.
{name} {now} 
Всего задач: {num_tasks}

## Актуальные задачи ({len(pending)}):
"""

    for task in pending:
        title = task['title'][:46] + '...' if len(task['title']) > 46 else task['title']
        report += f"- {title}\n"

    report += "\n"

    report += f"""
## Завершённые задачи ({len(completed)}):
"""

    for task in completed:
        title = task['title'][:46] + '...' if len(task['title']) > 46 else task['title']
        report += f"- {title}\n"

    return report


def save_report(user, report):
    filename = f"{user['username']}.txt"

    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'w') as f:
         f.write(report)


def main():
    users = get_users()

    if not os.path.exists('tasks'):
        os.mkdir('tasks')

    os.chdir('tasks')

    for user in users:
        report = generate_report(user)
        save_report(user, report)


if __name__ == '__main__':
    main()