"""Manage tasks through the graphical dashboard using the group's modules."""

# Check that the entered deadline is a valid calendar date.
from datetime import date

from dashboard_display_module import display_dashboard
from priority_queue_engine import priority_queue_engine
from reactive_task_list import ReactiveTaskList
from task_manager import manage_tasks

if __name__ == "__main__":
    # 1. Initialize the reactive list (auto-loads on startup)
    my_tasks = ReactiveTaskList("my_tasks.json")

    # 3. Calculate priority and sort (via priority_queue_engine)
    my_tasks = priority_queue_engine(my_tasks)

    # Process button actions.
    def change_task(command, data):
        """Validate task input and call the group's management and ranking functions."""
        # Assign a new ID when adding.
        if command == "ADD":
            data["id"] = max((task["id"] for task in my_tasks), default=0) + 1

        # Validate the form before changing or saving task data.
        if command != "DELETE":
            for field in ("name", "deadline_date", "duration", "difficulty"):
                value = data[field].strip()
                error = ""
                if field == "name":
                    if not value:
                        error = "Enter a task name."
                elif field == "deadline_date":
                    if len(value) != 10 or value[4] != "-" or value[7] != "-":
                        error = "Use YYYY-MM-DD for the deadline."
                    else:
                        try:
                            date.fromisoformat(value)
                        except ValueError:
                            error = "Enter a valid calendar date."
                elif field == "duration":
                    if not value.replace(".", "", 1).isdecimal():
                        error = "Enter a numeric duration, such as 2 or 1.5."
                    else:
                        value = float(value)
                        if not 0 < value <= 100:
                            error = "Duration must be greater than 0 and at most 100 hours."
                elif field == "difficulty":
                    if not value.isdecimal() or not 1 <= int(value) <= 5:
                        error = "Difficulty must be a whole number from 1 to 5."
                    else:
                        value = int(value)
                if error:
                    return False, error, field
                data[field] = value

        # Update, rank and save the task list.
        manage_tasks(my_tasks, command, data)
        priority_queue_engine(my_tasks)
        messages = {"ADD": "Task added.", "EDIT": "Task updated.", "DELETE": "Task deleted."}
        return True, messages[command] + " Schedule updated.", None

    # 4. Display dashboard (via dashboard_display_module)
    # Pass the task-operation callback to the dashboard buttons.
    display_dashboard(my_tasks, on_action=change_task)
