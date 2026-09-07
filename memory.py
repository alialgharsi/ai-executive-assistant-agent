import json
import os

MEMORY_FILE = "tasks.json"


def save_tasks(tasks):
    with open(MEMORY_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def load_tasks():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    return [
        "Study Python for 1 hour",
        "Update GitHub project",
        "Practice machine learning"
    ]