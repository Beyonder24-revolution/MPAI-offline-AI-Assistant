import sqlite3
import hashlib
import os

DB_PATH = os.path.join("data", "auth.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_password(password: str) -> str:
    hashed = _hash_password(password)

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)

    cur.execute("DELETE FROM user")
    cur.execute(
        "INSERT INTO user (password_hash) VALUES (?)",
        (hashed,)
    )

    conn.commit()
    conn.close()
    return hashed


def authenticate(password: str) -> bool:
    hashed = _hash_password(password)

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("SELECT password_hash FROM user LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return row[0] == hashed


def change_password(old_password: str, new_password: str) -> bool:
    if not authenticate(old_password):
        return False

    new_hash = _hash_password(new_password)

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE user SET password_hash = ?", (new_hash,))
    conn.commit()
    conn.close()

    return True
