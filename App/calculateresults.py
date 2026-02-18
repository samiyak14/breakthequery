import json
from pathlib import Path
from collections import defaultdict

# ----------- Paths -----------
APP_PATH = Path(__file__).parent
BACKUP_FILE = APP_PATH / "backup_log.json"

if not BACKUP_FILE.exists():
    print("No local backup file found.")
    exit()

# ----------- Load local backup -----------
with open(BACKUP_FILE, "r") as f:
    logs = json.load(f)

# ----------- Aggregate results -----------
# Structure: {player_name: {"pc_number": X, "correct": Y, "time": Z}}
results = defaultdict(lambda: {"pc_number": 0, "correct": 0, "time": 0})

for entry in logs:
    name = entry.get("name", "Unknown")
    pc = entry.get("pc_number", 0)
    correct = 1 if entry.get("correct", False) else 0
    time_taken = entry.get("time_taken", 0)

    results[name]["pc_number"] = pc
    results[name]["correct"] += correct
    results[name]["time"] += time_taken

# ----------- Calculate leaderboard -----------
# Sort by most correct, then least time
leaderboard = sorted(
    results.items(),
    key=lambda x: (-x[1]["correct"], x[1]["time"])
)

# ----------- Display results -----------
print("📊 Local Leaderboard:")
print(f"{'Rank':<5} {'Name':<20} {'PC No.':<7} {'Correct':<8} {'Time Taken (s)':<15}")
for idx, (name, data) in enumerate(leaderboard, start=1):
    print(f"{idx:<5} {name:<20} {data['pc_number']:<7} {data['correct']:<8} {data['time']:<15.2f}")
