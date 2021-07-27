import json
import os
import datetime
import requests


def create_user_tasks(user):

    try:
        name = user["username"]
        tasks = get_tasks_by_user_id(user["id"], todos_json_list)
    except KeyError:
        return

    now_time = datetime.datetime.now()
    filename = f'tasks/{user["username"]}.txt'

    if os.path.exists(filename):
        file = open(filename)
        s = file.readline()
        file_creation_time = ''
        index = 0
        for char in s:
            if char == '>':
                index += 2
                file_creation_time = s[index: len(s)-1]
                file_creation_time = f'{file_creation_time[6:10]}-{file_creation_time[3:5]}-{file_creation_time[0:2]}T{file_creation_time[11:16]}'
            else:
                index += 1
        new_filename = f'tasks/{user["username"]}_{file_creation_time}.txt'
        file.close()
        os.rename(filename, new_filename)

    completed_tasks = ''
    failed_tasks = ''

    for task in tasks[0]:
        if len(task) > 50:
            task = task[0:50] + '...'
        completed_tasks += task + '\n'

    for task in tasks[1]:
        if len(task) > 50:
            task = task[0:50] + '...'
        failed_tasks += task + '\n'

    if completed_tasks == '':
        completed_tasks = 'Нет задач'
    if failed_tasks == '':
        failed_tasks = 'Нет задач'

    with open(filename, 'w') as file:
        file.write(f'''{user["name"]} <{user["email"]}> {now_time.strftime("%d.%m.%Y %H:%M")}
{user["company"]["name"]}\n
Завершённые задачи:
{completed_tasks}\n
Оставшиеся задачи:
{failed_tasks}''')


def get_tasks_by_user_id(id, todos):
    completed_tasks = []
    failed_tasks = []
    try:
        for task in todos:
            if task["userId"] == id:
                if task['completed']:
                    completed_tasks.append(task['title'])
                else:
                    failed_tasks.append(task['title'])
    except KeyError:
        pass
    return completed_tasks, failed_tasks


users_link = 'https://json.medrating.org/users'
todos_link = 'https://json.medrating.org/todos'

request_users = requests.get(users_link)
request_todos = requests.get(todos_link)

request_users_dumps = json.dumps(request_users.json())
request_todos_dumps = json.dumps(request_todos.json())

users_json_list = json.loads(request_users_dumps)
todos_json_list = json.loads(request_todos_dumps)

try:
    os.mkdir('tasks')
except FileExistsError:
    pass

for user in users_json_list:
    create_user_tasks(user)
