import sqlite3


def insert_data_to_db(users, statuses, tasks):
    
    with sqlite3.connect('app/db/user_tasks.db') as con:
        cur = con.cursor()

        query_insert_users = "INSERT INTO users(fullname, email) VALUES (?, ?)"
        cur.executemany(query_insert_users, users)

        query_insert_statuses = "INSERT INTO statuses(name) VALUES (?)"
        cur.executemany(query_insert_statuses, statuses)

        query_insert_tasks = "INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)"
        cur.executemany(query_insert_tasks, tasks)

