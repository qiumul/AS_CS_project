"""Manage tasks in the terminal and display the schedule in the dashboard."""

# Import date to check calendar dates.
from datetime import date

from dashboard_display_module import display_dashboard
from priority_queue_engine import priority_queue_engine
from reactive_task_list import ReactiveTaskList
from task_manager import manage_tasks


if __name__ == "__main__":

    # Load previously saved tasks.
    my_tasks = ReactiveTaskList("my_tasks.json")
    # Calculate priority scores and sort the tasks.
    my_tasks = priority_queue_engine(my_tasks)

    # Keep accepting user commands until Exit is selected.
    while True:
        print("\nDynamic Academic Planner")
        print("1. Add task\n2. Edit task\n3. Delete task\n4. View dashboard\n0. Exit")
        try:
            # Repeat until a valid option is entered.
            while True:
                choice = input("Choose an option: ").strip()
                if choice in ("0", "1", "2", "3", "4"):
                    break
                print("Please choose 0, 1, 2, 3 or 4.")
            if choice == "0":
                print("Goodbye.")
                break
            # Open the existing GUI.
            if choice == "4":
                priority_queue_engine(my_tasks)
                print("Starting dashboard...")
                display_dashboard(my_tasks)
                continue

            # Show task IDs so the user can identify an existing task.
            existing = None
            if choice in ("2", "3"):
                if not my_tasks:
                    print("There are no tasks to edit or delete.")
                    continue
                for task in my_tasks:
                    print(f"ID {task['id']}: {task['name']}")
                # Check the ID format and existence before accepting it.
                while True:
                    value = input("Enter task ID: ").strip()
                    if not value.isdecimal():
                        print("Enter a whole-number task ID.")
                        continue
                    target_id = int(value)
                    existing = next((task for task in my_tasks if task["id"] == target_id), None)
                    if existing is not None:
                        break
                    print(f"Task ID {target_id} not found.")

            # Delete the task with the selected ID.
            if choice == "3":
                manage_tasks(my_tasks, "DELETE", {"id": target_id})
            else:
                # Keep the selected ID when editing; otherwise use the highest current ID plus one.
                data = {"id": existing["id"] if existing else max((t["id"] for t in my_tasks), default=0) + 1}
                # Validate each field in its own loop so valid answers are kept.
                for field, label in (("name", "Task name"), ("deadline_date", "Deadline YYYY-MM-DD"),
                                     ("duration", "Duration in hours"), ("difficulty", "Difficulty 1-5")):
                    # Require valid input for every field when adding or editing.
                    prompt = f"{label}: "
                    while True:
                        value = input(prompt).strip()
                        if field == "name":
                            if not value:
                                print("Enter a task name.")
                                continue
                        elif field == "deadline_date":
                            if len(value) != 10 or value[4] != "-" or value[7] != "-":
                                print("Use YYYY-MM-DD for the deadline.")
                                continue
                            # Calendar validation.
                            try:
                                date.fromisoformat(value)
                            except ValueError:
                                print("Enter a valid calendar date.")
                                continue
                        elif field == "duration":
                            if not value.replace(".", "", 1).isdecimal():
                                print("Enter a number for duration, such as 2 or 1.5.")
                                continue
                            value = float(value)
                            if not 0 < value <= 10000:
                                print("Duration must be greater than 0 and at most 10000 hours.")
                                continue
                        elif field == "difficulty":
                            if not value.isdecimal() or not 1 <= int(value) <= 5:
                                print("Difficulty must be a whole number from 1 to 5.")
                                continue
                            value = int(value)
                        data[field] = value
                        break

                # Pass validated input to the task management module.
                manage_tasks(my_tasks, "EDIT" if existing else "ADD", data)

            # Recalculate scores after a successful change; the task list saves automatically.
            priority_queue_engine(my_tasks)
            print("Task list updated and priorities recalculated.")
        # Exit cleanly when terminal input ends or is interrupted.
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
