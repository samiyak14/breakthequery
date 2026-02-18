from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from database import execute_query, execute_select
from fastapi.middleware.cors import CORSMiddleware

# ----------- Request Model -----------
class QuestionDataRequest(BaseModel):
    name: str
    pc_number: int
    question_number: int
    timestamp: Optional[datetime] = None
    time_taken: float
    correct: bool  # NEW field to track correctness

# ----------- FastAPI App -----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- Endpoints -----------

@app.post("/log")
async def log_data(entry: QuestionDataRequest):
    """Logs a player's answer along with correctness and time taken."""
    if not entry.timestamp:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        time = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    correct_val = 1 if entry.correct else 0  # convert boolean to integer

    query = f"""
    INSERT INTO QuizData (Name, PCNumber, QuestionNumber, SubmissionTime, TimeTaken, Correct)
    VALUES ('{entry.name}', {entry.pc_number}, {entry.question_number}, '{time}', {entry.time_taken}, {correct_val});
    """
    return execute_query(query)

@app.get("/results")
async def get_results():
    """Fetches all quiz results from the database."""
    query = "SELECT * FROM QuizData;"
    result = execute_select(query)
    return result

@app.get("/leaderboard")
async def leaderboard():
    """
    Returns the leaderboard:
    - Sorted by total correct answers descending
    - Then by total time ascending (faster wins)
    """
    query = """
    SELECT Name, PCNumber, SUM(Correct) as TotalCorrect, SUM(TimeTaken) as TotalTime
    FROM QuizData
    GROUP BY Name, PCNumber
    ORDER BY TotalCorrect DESC, TotalTime ASC;
    """
    result = execute_select(query)
    return result
