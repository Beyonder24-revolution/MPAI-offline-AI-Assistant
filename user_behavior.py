# core/user_behavior.py
import sqlite3
import os

DB_PATH = os.path.join("data", "memory.db")

def save_behavior(key, value):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS behavior (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cur.execute(
        "INSERT OR REPLACE INTO behavior (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()
    conn.close()


def get_behavior(key):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT value FROM behavior WHERE key = ?",
        (key,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
