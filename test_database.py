from src.database import Database

db = Database()

db.save_task(
    "Research AI trends",
    "AI Report"
)

print(
    db.get_tasks()
)
