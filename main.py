"""
This is the entry point for the Task Manager application.
Displays main menu and routes user choices to appropriate functions.
"""

from ui import display_main_menu, get_user_choice, display_exit_message
from task_manager import add_task, view_tasks, delete_task


def main():

    while True:
        display_main_menu()
        choice = get_user_choice()

        if choice == '1':
            # Add Task
            add_task()
        elif choice == '2':
            # View Tasks
            view_tasks()
        elif choice == '3':
            # Delete Task
            delete_task()
        elif choice == '4':
            # Exit
            display_exit_message()
            break
        else:
            # Invalid choice
            print("\n✗ Error: Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
