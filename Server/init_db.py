import sqlite3

db_path = r"C:\Users\saami\OneDrive\Desktop\SEM6\Techventure2026\breakthequery\App\database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add Correct column if it doesn't exist
cursor.execute("""
ALTER TABLE QuizData 
ADD COLUMN Correct INTEGER DEFAULT 0;
""")

conn.commit()
conn.close()
