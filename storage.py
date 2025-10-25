"""
Handles all file I/O operations for task persistence.
Tasks are stored in JSON format.
"""

import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    """
    Load tasks from the JSON file.
    """
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
            return tasks
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or unreadable, return empty list
        return []


def save_tasks(tasks):
    """
    Save tasks to the JSON file.
    """
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
        return True
    except IOError:
        return False
