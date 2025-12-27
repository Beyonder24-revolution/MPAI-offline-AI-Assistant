from core.response_engine import smart_fallback, confirm_save
from core.document_reader import read_pdf
from core.image_reader import read_image
from core.auth import authenticate
from core.session import SessionManager
from core.ai_engine import OfflineAI
from core.memory import list_memory, forget_memory
import sqlite3
import time
import os

# -------------------------------
# SETUP
# -------------------------------
DB_PATH = os.path.join("data", "memory.db")
os.makedirs("data", exist_ok=True)

# Create memory table with created_at if not exists
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    key TEXT PRIMARY KEY,
    value TEXT,
    created_at TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS emergency_log (
    id INTEGER PRIMARY KEY,
    used_at TEXT
)
""")
conn.commit()
conn.close()

# Initialize session and AI
session = SessionManager(timeout_seconds=60, emergency_password="EMERGENCY123")
ai = OfflineAI(allow_save=True)

print("\n🔒 MPAI is locked")

# -------------------------------
# INITIAL UNLOCK
# -------------------------------
while session.locked:
    pwd = input("Enter password to unlock (or emergency): ").strip()
    unlocked = session.unlock(pwd, authenticate)

    if unlocked and pwd == session.emergency_password:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO emergency_log (used_at) VALUES (?)",
            (time.strftime("%Y-%m-%d %H:%M:%S"),)
        )
        conn.commit()
        conn.close()

print("\n✅ MPAI unlocked. You can start chatting.")
print("Type: exit       → quit")
print("Type: teach      → teach MPAI something")
print("Type: list       → show all saved memories")
print("Type: forget     → delete a saved memory")
print("Type: read pdf   → read a PDF file")
print("Type: read image → read an image\n")

# -------------------------------
# MAIN INTERACTION LOOP
# -------------------------------
while True:
    session.activity()

    # 🔒 AUTO-LOCK HANDLING
    if session.locked:
        print("\n🔒 Session locked. Unlock required.")
        while session.locked:
            pwd = input("Enter password to unlock (or emergency): ").strip()
            unlocked = session.unlock(pwd, authenticate)

            if unlocked and pwd == session.emergency_password:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO emergency_log (used_at) VALUES (?)",
                    (time.strftime("%Y-%m-%d %H:%M:%S"),)
                )
                conn.commit()
                conn.close()

        print("✅ Unlocked. Continue chatting.\n")
        continue

    user_input = input("You: ").strip()
    if not user_input:
        continue

    cmd = user_input.lower()

    # -------------------------------
    # COMMAND HANDLER
    # -------------------------------
    if cmd == "exit":
        print("👋 Goodbye")
        session.stop()
        break

    elif cmd == "teach":
        key = input("Teach question/key: ").strip()
        value = input("Teach answer/value: ").strip()

        if not key or not value:
            print("⚠️ Key and value cannot be empty\n")
            continue

        confirm = input("Save this memory? (y/n): ").lower()
        if confirm == "y":
            ai.teach(key, value)
            print("🧠", confirm_save(), "\n")
        else:
            print("❌ Memory not saved\n")
        continue

    elif cmd == "list":
        list_memory()
        continue

    elif cmd == "forget":
        key = input("Enter key to forget: ").strip()
        if key:
            forget_memory(key)
        else:
            print("⚠️ Key cannot be empty\n")
        continue

    elif cmd.startswith("read pdf"):
        path = input("Enter PDF file path: ").strip()
        read_pdf(path)
        print("✅ PDF processed and saved in memory\n")
        continue

    elif cmd.startswith("read image"):
        path = input("Enter image file path: ").strip()
        read_image(path)
        print("✅ Image processed and saved in memory\n")
        continue

    # -------------------------------
    # NORMAL QUESTION + SMART FALLBACK
    # -------------------------------
    answer = ai.ask(user_input)

    if answer in smart_fallback().__class__([answer]):
        teach_confirm = input(f"MPAI: {answer} Can I remember your answer? (y/n): ").lower()
        if teach_confirm == "y":
            user_answer = input("You (answer to remember): ").strip()
            if user_answer:
                ai.teach(user_input, user_answer)
                print("🧠 Learned automatically\n")
            else:
                print("❌ No answer provided, memory skipped\n")
    else:
        print("MPAI:", answer, "\n")
