import sqlite3 as sq3
import os
import sys

db_path = r"C:\Users\saami\OneDrive\Desktop\SEM6\Techventure2026\breakthequery\App\database.db"  # path to your app database


DATABASE = db_path

def execute_select(query):
    with sq3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return {"status": "success", "response": rows}
        except Exception as e:
            return {"status": "error", "response": str(e)}

def execute_query(query):
    with sq3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            return {"status": "success", "response": "done"}
        except Exception as e:
            return {"status": "error", "response": str(e)}
