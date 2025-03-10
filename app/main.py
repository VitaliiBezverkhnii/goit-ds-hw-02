from operations import get_all_users
from seed import insert_data_to_db
from create_db import create_db
from create_data import generate_fake_data, prepare_data


if __name__ == "__main__":
    create_db()
    users_fake, emails_fake, tasks_fake = generate_fake_data(3, 3)
    users, statuses, tasks = prepare_data(users_fake, emails_fake, tasks_fake)
    insert_data_to_db(users, statuses, tasks)

    all_users = get_all_users()
    print(all_users)