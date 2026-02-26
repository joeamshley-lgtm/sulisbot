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


import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS group_settings (
    chat_id INTEGER PRIMARY KEY,
    ai_enabled INTEGER DEFAULT 1,
    games_enabled INTEGER DEFAULT 1,
    translate_enabled INTEGER DEFAULT 1,
    mode TEXT DEFAULT 'academic'
)
""")
conn.commit()


def initialize_group_settings(chat_id):
    cursor.execute(
        "INSERT OR IGNORE INTO group_settings (chat_id) VALUES (?)",
        (chat_id,)
    )
    conn.commit()


def get_group_settings(chat_id):
    cursor.execute(
        "SELECT ai_enabled, games_enabled, translate_enabled, mode FROM group_settings WHERE chat_id=?",
        (chat_id,)
    )
    row = cursor.fetchone()

    return {
        "ai_enabled": bool(row[0]),
        "games_enabled": bool(row[1]),
        "translate_enabled": bool(row[2]),
        "mode": row[3],
    }


def update_group_setting(chat_id, column, value):
    cursor.execute(
        f"UPDATE group_settings SET {column}=? WHERE chat_id=?",
        (value, chat_id)
    )
    conn.commit()
