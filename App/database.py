import sqlite3 as sq3
import json
import os
import sys

db_name = 'database.db'
questions_name = 'questions.json'

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(__file__)

DATABASE = os.path.join(application_path, db_name)
QUESTIONS = os.path.abspath(os.path.join(application_path, '..', questions_name))  # root folder

def execute_select(query):
    with sq3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            connection.commit()
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

def get_questions():
    with open(QUESTIONS, 'r') as f:
        return json.load(f)['questions']

def check_query(question, query):
    model_answer = execute_select(question['answer_key'])['response']
    answer = execute_select(query)

    if answer['status'] != 'success':
        return {"executed": False, "match": False, "response": f"Error: {answer['response']}"}

    user_answer = answer['response']
    if set(user_answer) == set(model_answer):
        return {"executed": True, "match": True, "response": "Well done, correct answer!"}
    else:
        return {"executed": True, "match": False, "response": "Query is correct in syntax but output is not correct."}
