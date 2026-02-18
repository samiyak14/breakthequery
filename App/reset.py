import os
import json
import requests
from database import execute_query  # matches your main.py
from pathlib import Path

# ----------- Paths -----------
APP_PATH = Path(__file__).parent
BACKUP_FILE = APP_PATH / "backup_log.json"
IP_FILE = APP_PATH / ".." / "ipaddress.txt"

# Read server IP
with open(IP_FILE, 'r') as f:
    server_ip = f.read().strip()

PORT = "8000"
URL_LOCAL = "http://127.0.0.1:8000/log"
URL_SERVER = f"http://{server_ip}:{PORT}/log"

# ----------- Clear local backup -----------
if BACKUP_FILE.exists():
    BACKUP_FILE.unlink()
    print(f"Deleted local backup file: {BACKUP_FILE}")
else:
    print("No local backup file found.")

# ----------- Clear server logs -----------
for url in [URL_LOCAL, URL_SERVER]:
    try:
        resp = requests.delete(url, timeout=3)  # assumes your server supports DELETE
        if resp.status_code == 200:
            print(f"Successfully cleared logs at {url}")
        else:
            print(f"Server responded with status {resp.status_code} for {url}")
    except Exception as e:
        print(f"Could not connect to {url}: {e}")

# ----------- Clear database table -----------
try:
    query = "DELETE FROM QuizData;"
    execute_query(query)
    print("Cleared all entries from QuizData table in the database.")
except Exception as e:
    print(f"Error clearing database table: {e}")

print("Reset complete.")
