"""
This is where all the core task management business logic lives.
Handles add, view, and delete operations with validation.
"""

import zmq
import json

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


def format_text_via_service(text, format_type="sentence"):
    """
    Format text using the Text Formatter microservice.

    Args:
        text: The text to format
        format_type: Type of formatting ("sentence", "upper", "lower", "title")

    Returns:
        Formatted text, or original text if service unavailable
    """
    try:
        # Create ZeroMQ context and socket
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        # Set timeout to avoid hanging if service is down
        socket.setsockopt(zmq.RCVTIMEO, 2000)  # 2 second timeout

        # Prepare request
        request = {
            "text": text,
            "format_type": format_type
        }

        # Send request
        socket.send_string(json.dumps(request))

        # Receive response
        response_json = socket.recv_string()
        response = json.loads(response_json)

        # Clean up
        socket.close()
        context.term()

        # Return formatted text or handle error
        if response.get("error"):
            print(f"\n[Warning] Text Formatter error: {response['error']}")
            return text  # Return original text if error

        return response.get("formatted_text", text)

    except zmq.error.Again:
        # Timeout - service not running
        print("\n[Warning] Text Formatter service not responding. Using original text.")
        return text
    except Exception as e:
        # Any other error
        print(f"\n[Warning] Could not connect to Text Formatter: {str(e)}")
        return text


def validate_text_via_service(text, min_length=1, max_length=100):
    """
    Validate text using the Text Validator microservice.

    Args:
        text: The text to validate
        min_length: Minimum required length (default: 1)
        max_length: Maximum allowed length (default: 100)

    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    try:
        # Create ZeroMQ context and socket
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5556")

        # Set timeout to avoid hanging if service is down
        socket.setsockopt(zmq.RCVTIMEO, 2000)  # 2 second timeout

        # Prepare request
        request = {
            "text": text,
            "min_length": min_length,
            "max_length": max_length
        }

        # Send request
        socket.send_string(json.dumps(request))

        # Receive response
        response_json = socket.recv_string()
        response = json.loads(response_json)

        # Clean up
        socket.close()
        context.term()

        # Return validation result
        is_valid = response.get("valid", False)
        error_message = response.get("error", None)

        return is_valid, error_message

    except zmq.error.Again:
        # Timeout - service not running, do basic validation
        print("\n[Warning] Text Validator service not responding. Using basic validation.")
        if not text or text.strip() == "":
            return False, "Text cannot be empty"
        return True, None
    except Exception as e:
        # Any other error - do basic validation
        print(f"\n[Warning] Could not connect to Text Validator: {str(e)}")
        if not text or text.strip() == "":
            return False, "Text cannot be empty"
        return True, None


def add_task():
    """
    Add a new task to the task list.
    Prompts user for title and description, validates input,
    and saves to storage.
    """
    display_add_task_header()

    # Get task title
    title = get_task_title()

    # Validate title using Text Validator microservice
    is_valid, error_message = validate_text_via_service(title, min_length=1, max_length=100)
    if not is_valid:
        display_error_message(error_message)
        wait_for_return_to_menu()
        return

    # Format title using Text Formatter microservice
    # Use "title" format to capitalize first letter of each word
    title = format_text_via_service(title, "title")

    # Get task description
    description = get_task_description()

    # Validate description using Text Validator microservice
    # Description is optional, so min_length=0
    is_valid, error_message = validate_text_via_service(description, min_length=0, max_length=500)
    if not is_valid:
        display_error_message(error_message)
        wait_for_return_to_menu()
        return

    # Format description using Text Formatter microservice
    # Use "sentence" format for proper sentence capitalization
    description = format_text_via_service(description, "sentence")

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