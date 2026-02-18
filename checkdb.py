import sqlite3
import os

# Absolute path to database.db in your project
db_path = os.path.abspath(r"C:\Users\saami\OneDrive\Desktop\SEM6\Techventure2026\breakthequery\App\database.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()
