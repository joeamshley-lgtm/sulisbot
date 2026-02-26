import sqlite3

conn = sqlite3.connect("linguamaster.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    xp INTEGER,
    level TEXT,
    correct INTEGER,
    wrong INTEGER
)
""")
conn.commit()


def calculate_level(xp):
    if xp < 10:
        return "Beginner"
    elif xp < 30:
        return "Intermediate"
    elif xp < 60:
        return "Scholar"
    else:
        return "Professor"


def add_xp(user, amount=5):
    cursor.execute("SELECT xp FROM users WHERE user_id=?", (user.id,))
    result = cursor.fetchone()

    if result:
        xp = result[0] + amount
        level = calculate_level(xp)
        cursor.execute("""
        UPDATE users SET xp=?, level=?, correct=correct+1
        WHERE user_id=?
        """, (xp, level, user.id))
    else:
        level = calculate_level(amount)
        cursor.execute("""
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
        """, (user.id, user.username, amount, level, 1, 0))

    conn.commit()


def get_profile(user_id):
    cursor.execute("""
    SELECT xp, level, correct, wrong
    FROM users WHERE user_id=?
    """, (user_id,))
    return cursor.fetchone()