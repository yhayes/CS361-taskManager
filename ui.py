"""
Handles all user interface operations like display and input.
Designed for command-line interface with inclusive prompts.
"""


def display_main_menu():
    """
    Display the main menu with all available options.
    """
    print("\n" + "=" * 19)
    print("TASK MANAGER")
    print("=" * 19)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Task")
    print("4. Exit")
    print()


def get_user_choice():
    """
    Get and return the user's menu choice.
    """
    return input("Enter choice: ")


def get_task_title():
    """
    Prompt for and return task title.
    """
    return input("Enter task title: ")


def get_task_description():
    """
    Prompt for and return task description.
    """
    return input("Enter task description: ")


def display_add_task_header():
    """
    Display the header for Add Task screen.
    """
    print("\nADD TASK")
    print("-" * 9)


def display_success_message(message):
    """
    Display a success message with checkmark.
    """
    print(f"\n✓ {message}")


def display_error_message(message):
    """
    Display an error message with X symbol.
    """
    print(f"\n✗ Error: {message}")


def display_view_tasks_header():
    """
    Display the header for View Tasks screen.
    """
    print("\nYOUR TASKS")
    print("-" * 10)


def display_tasks(tasks):
    """
    Display all tasks in a numbered list format.
    """
    if not tasks:
        print("No tasks found")
    else:
        for i, task in enumerate(tasks, 1):
            print(f"\n{i}. {task['title']}")
            print(f"   Description: {task['description']}")


def display_delete_task_header():
    """
    Display the header for Delete Task screen.
    """
    print("\nDELETE TASK")
    print("-" * 11)


def get_task_number_to_delete():
    """
    Prompt for task number to delete.
    """
    return input("\nEnter task number to delete: ")


def get_delete_confirmation(task_title):
    """
    Ask user to confirm deletion with warning about permanence.
    """
    print(f"\nAre you sure you want to delete this task?")
    print(f'"{task_title}"')
    print("This action cannot be undone.")
    print()
    return input("Enter 'yes' to confirm or 'no' to cancel: ").lower()


def wait_for_return_to_menu():
    """
    Wait for user to press any key before returning to main menu.

    Not sure yet if we want this
    """
    input("\nPress any key to return to main menu...")

def display_exit_message():
    """
    Display goodbye message when user exits.
    """
    print("\nThank you for using Task Manager. Goodbye!")