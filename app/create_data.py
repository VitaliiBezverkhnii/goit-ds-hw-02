from random import choice, randint
from faker import Faker

def generate_fake_data(number_users: int, number_tasks: int) -> tuple:
    fake_users = []
    fake_emails = []
    fake_tasks = []

    fake_data = Faker()

    for _ in range(number_users):
        fake_users.append(fake_data.name())
        fake_emails.append(fake_data.email())

    for _ in range(number_tasks):
        fake_tasks.append(fake_data.job())

    return fake_users, fake_emails, fake_tasks


def prepare_data(users, emails, tasks) -> tuple:
    for_users = []
    fake_statuses = [('new',), ('in progress',), ('completed',)]
    for_tasks = []
    
    for i, user in enumerate(users):
        for_users.append((user, emails[i]))

    for task in tasks:
        id_status = randint(1, len(fake_statuses[:-1]))
        id_user = randint(1, len(users[:-1]))
        status = fake_statuses[id_status][0]
        user = for_users[id_user][0]
        description = f"Title: {task}, Status: {status}, User: {user}"
        for_tasks.append((task, description, id_status, id_user))

    return for_users, fake_statuses, for_tasks

