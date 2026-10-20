from mcp.server.fastmcp import FastMCP
import json
import datetime
from pathlib import Path

mcp = FastMCP("CampusConnect-AI")
DATA_FILE = Path("student_data.json")

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"assignments": [], "timetable": [], "notes": [], "reminders": []}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

@mcp.tool()
def add_assignment(subject: str, title: str, due_date: str, description: str = "") -> str:
    data = load_data()
    assignment = {
        "id": len(data["assignments"]) + 1,
        "subject": subject,
        "title": title,
        "due_date": due_date,
        "description": description,
        "created_at": datetime.datetime.now().isoformat()
    }
    data["assignments"].append(assignment)
    save_data(data)
    return f"Added: {title} for {subject}, due {due_date}"

@mcp.tool()
def list_assignments(subject: str = "") -> str:
    data = load_data()
    assignments = data["assignments"]
    if not assignments:
        return "No assignments"
    result = "Assignments:\n"
    for a in assignments:
        result += f"- {a['subject']}: {a['title']} (Due: {a['due_date']})\n"
    return result

@mcp.tool()
def add_timetable(day: str, time: str, subject: str, location: str = "") -> str:
    data = load_data()
    data["timetable"].append({"day": day, "time": time, "subject": subject, "location": location})
    save_data(data)
    return f"Added {subject} on {day} at {time}"

@mcp.tool()
def get_today_schedule() -> str:
    data = load_data()
    today = datetime.datetime.now().strftime("%A")
    classes = [c for c in data["timetable"] if c["day"].lower() == today.lower()]
    if not classes:
        return f"No classes for {today}"
    result = f"{today}:\n"
    for c in classes:
        result += f"- {c['time']}: {c['subject']}\n"
    return result

@mcp.tool()
def student_dashboard() -> str:
    data = load_data()
    return f"Dashboard - Assignments: {len(data['assignments'])}, Notes: {len(data['notes'])}"

if __name__ == "__main__":
    mcp.run()
