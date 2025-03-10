import sqlite3

def create_db():
    with open("app/db/user_tasks.sql", "r") as f:
        sql = f.read()

    with sqlite3.connect("app/db/user_tasks.db") as db_conn:
        cur = db_conn.cursor()
        cur.executescript(sql)