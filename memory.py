import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "memory.db")
os.makedirs("data", exist_ok=True)

# Initialize memory table
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    key TEXT PRIMARY KEY,
    value TEXT,
    created_at TEXT
)
""")
conn.commit()
conn.close()
from core.app_mode import is_demo

def save_memory(key, value, allow_save=True):
    if is_demo():
        return  # ❌ No saving in demo mode

    if not allow_save:
        return

    # existing DB save logic continues here
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO memory (key, value, created_at)
        VALUES (?, ?, ?)
    """, (key, value, timestamp))
    conn.commit()
    conn.close()
    print(f"[Memory] Saved '{key}' at {timestamp}")

def list_memory():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT key, created_at FROM memory")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("🧠 No memories saved yet\n")
        return
    print("\n🧠 Saved Memories:")
    for key, created_at in rows:
        print(f"- {key}  (saved on {created_at})")
    print()

def forget_memory(key):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM memory WHERE key=?", (key,))
    conn.commit()
    conn.close()
    print(f"[Memory] '{key}' deleted if it existed")

def search_memory(query, exact=False):
    query = query.lower()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if exact:
        cur.execute("SELECT rowid, key, value, created_at FROM memory WHERE key=?", (query,))
    else:
        cur.execute("SELECT rowid, key, value, created_at FROM memory WHERE key LIKE ?", (f"%{query}%",))
    results = cur.fetchall()
    conn.close()
    return results

def load_memory(key):
    results = search_memory(key, exact=True)
    if results:
        return results[0][2]  # return value
    return None
def get_all_memory():
    import sqlite3
    import os

    DB_PATH = os.path.join("data", "memory.db")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM memory")
    rows = cur.fetchall()

    conn.close()
    return rows
