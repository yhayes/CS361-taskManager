"""
This is where all the core task management business logic lives.
Handles add, view, and delete operations with validation.
"""

from storage import load_tasks, save_tasks
from ui import (
    display_add_task_header,
    get_task_title,
    get_task_description,
    display_success_message,
    display_error_message,
    wait_for_return_to_menu,
    display_view_tasks_header,
    display_tasks,
    display_delete_task_header,
    get_task_number_to_delete,
    get_delete_confirmation
)


def add_task():
    """
    Add a new task to the task list.
    Prompts user for title and description, validates input,
    and saves to storage.
    """
    display_add_task_header()

    # Get task title
    title = get_task_title()

    # Validate title is not empty
    if not title or title.strip() == "":
        display_error_message("Task title cannot be empty")
        wait_for_return_to_menu()
        return

    # Get task description
    description = get_task_description()

    # Create task dictionary
    task = {
        "title": title,
        "description": description
    }

    # Load existing tasks
    tasks = load_tasks()

    # Add new task
    tasks.append(task)

    # Save tasks
    if save_tasks(tasks):
        display_success_message("Task added successfully!")
    else:
        display_error_message("Failed to save task")

    wait_for_return_to_menu()


def view_tasks():
    """
    Display all tasks that we have.
    Shows numbered list with titles and descriptions, or a message if no tasks exist.
    """
    display_view_tasks_header()

    # Load all tasks
    tasks = load_tasks()

    # Display tasks
    display_tasks(tasks)

    wait_for_return_to_menu()


def delete_task():
    """
    Delete a task from the task list.
    Shows tasks, prompts for task number, confirms deletion, and removes task.
    """
    display_delete_task_header()

    # Load all tasks
    tasks = load_tasks()

    # Check if there are any tasks
    if not tasks:
        display_error_message("No tasks available to delete")
        wait_for_return_to_menu()
        return

    # Display tasks
    display_tasks(tasks)

    # Get task number to delete
    task_num_str = get_task_number_to_delete()

    # Validate input is a number
    try:
        task_num = int(task_num_str)
    except ValueError:
        display_error_message("Invalid task number")
        wait_for_return_to_menu()
        return

    # Validate task number is in range
    if task_num < 1 or task_num > len(tasks):
        display_error_message("Invalid task number")
        wait_for_return_to_menu()
        return

    # Get the task to delete (adjust for 0-based indexing)
    task_to_delete = tasks[task_num - 1]

    # Confirm deletion
    confirmation = get_delete_confirmation(task_to_delete['title'])

    if confirmation == 'yes':
        # Delete the task
        tasks.pop(task_num - 1)

        # Save updated task list
        if save_tasks(tasks):
            display_success_message("Task deleted successfully!")
        else:
            display_error_message("Failed to delete task")
    else:
        print("\nDeletion cancelled.")

    wait_for_return_to_menu()
