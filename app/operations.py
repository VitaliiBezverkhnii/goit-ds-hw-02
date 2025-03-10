import sqlite3

def get_all_users():
    results = []
    query = "SELECT * FROM users"

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    return results


def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = ?"

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute(query, (user_id,))
        con.commit()

    print(f"Користувач з ID {user_id} видалений.")

def get_user_tasks(user_id: int):
    results = []
    query = "SELECT * FROM tasks WHERE user_id = ?"

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
    return results

def get_tasks_by_status(status: str):
    results = []
    query_status_new = "SELECT id FROM statuses WHERE name = ?"
    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()

        cursor.execute(query_status_new, (status,))
        result = cursor.fetchone()
        if result:
            status_id = result[0]
            query_tasks = "SELECT * FROM tasks WHERE status_id = ?"
            cursor.execute(query_tasks, (status_id,))
            results = cursor.fetchall()
    return results

def update_status_task(id_task: int, status: str) -> bool:
    is_updated = False
    
    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        query_status_id = "SELECT id FROM statuses WHERE name = ?"
        cursor.execute(query_status_id, (status,))
        result = cursor.fetchone()
        
        if not result:
            return is_updated
        
        status_id = result[0]
        query_update_task = "UPDATE tasks SET status_id = ? WHERE id = ?"
        cursor.execute(query_update_task, (status_id, id_task))
        if cursor.rowcount > 0:
            is_updated = True
    
    return is_updated

def get_users_without_task():
    results = []
    query = """
        SELECT * FROM users 
        LEFT JOIN tasks ON users.id = tasks.user_id 
        WHERE tasks.id IS NULL
    """
    
    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        
        cursor.execute(query)
        results = cursor.fetchall()
    
    return results

def add_user_task(title, description, status, user_id: int):
    is_insert = False
        
    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()

        query_status_id = "SELECT id FROM statuses WHERE name = ?"
        cursor.execute(query_status_id, (status,))
        result = cursor.fetchone()

        if not result:
            return is_insert
        
        id_status = result[0]

        query_insert_tasks = "INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)"
        cursor.execute(query_insert_tasks, (title, description, id_status, user_id))
        con.commit()
        if cursor.rowcount > 0:
            is_insert = True
    return is_insert

def get_tasks_not_completed():
    results = []
    completed_status = "completed"

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        query_status = "SELECT id FROM statuses WHERE name = ?"
        cursor.execute(query_status, (completed_status,))
        result = cursor.fetchone()
        if result:
            query_tasks = "SELECT * FROM tasks WHERE status_id != ?"
            cursor.execute(query_tasks, (result[0],))
            results = cursor.fetchall()
    return results

def delete_task(task_id: int) -> bool:
    is_deleted = False
    query = "DELETE FROM tasks WHERE id = ?"

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute(query, (task_id,))
        con.commit()
        if cursor.rowcount > 0:
            is_deleted = True
    return is_deleted


def get_user_by_email(email: str):
    query = "SELECT * from users WHERE email = ?"
    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute(query, (email,))
        return cursor.fetchone()


def update_user_name(name: str, user_id: str):
    is_updated = False
    query = "UPDATE users SET fullname = ? WHERE id = ?"
    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute(query, (name, user_id,))
        if cursor.rowcount > 0:
            is_updated = True
    return is_updated

def get_task_count_by_all_status():
    results = []
    query = """
        SELECT statuses.name, COUNT(tasks.id) AS task_count
        FROM statuses
        LEFT JOIN tasks ON statuses.id = tasks.status_id
        GROUP BY statuses.id
    """

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

    return results



def get_user_tasks_by_email_domain(email_domain: str):
    results = []
    query = """
        SELECT *
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE ?
    """

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        email_domain = f"%@{email_domain}"
        cursor.execute(query, (email_domain,))
        results = cursor.fetchall()

    return results


def get_tasks_without_description():
    results = []
    query = "SELECT * FROM tasks WHERE description IS NULL OR description = ''"

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()

        cursor.execute(query)
        results = cursor.fetchall()

    return results

def get_users_and_tasks_in_progress():
    results = []
    query = """
        SELECT users.fullname, tasks.title, tasks.description
        FROM tasks
        INNER JOIN users ON tasks.user_id = users.id
        INNER JOIN statuses ON tasks.status_id = statuses.id
        WHERE statuses.name = 'in progress'
    """

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

    return results

def get_users_and_task_counts():
    results = []
    query = """
        SELECT users.fullname, COUNT(tasks.id) AS task_count
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.id
    """

    with sqlite3.connect('app/db/user_tasks.db') as con:
        cursor = con.cursor()

        cursor.execute(query)
        results = cursor.fetchall()

    return results