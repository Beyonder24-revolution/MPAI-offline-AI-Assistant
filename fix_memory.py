import sqlite3
import os

DB_PATH = os.path.join("data", "memory.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if 'created_at' column exists
cur.execute("PRAGMA table_info(memory)")
columns = [col[1] for col in cur.fetchall()]
print("Current columns in 'memory' table:", columns)

# Add 'created_at' if missing
if 'created_at' not in columns:
    cur.execute("ALTER TABLE memory ADD COLUMN created_at TEXT")
    print("✅ 'created_at' column added successfully")
else:
    print("✅ 'created_at' column already exists")

conn.commit()
conn.close()
