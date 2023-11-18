import sqlite3 as sql


async def sql_connector():
    con = sql.connect("youtube.db")
    cur = con.cursor()

    return con, cur


async def create_tables():
    con, cur = await sql_connector()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY
    )""")


async def add_user(user_id: int):
    con, cur = await sql_connector()
    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    if not user:
        cur.execute("INSERT INTO users VALUES (?)", (user_id,))
        con.commit()

async def total_user():
    con, cur = await sql_connector()
    total_user = cur.execute("SELECT * FROM users").fetchall()

    return len(total_user)

async def get_all_users_id():
    con, cur = await sql_connector()
    users = cur.execute("SELECT * FROM users").fetchall()

    return users
