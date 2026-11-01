from datetime import datetime

def priority_queue_engine(task_list):
    """
    Receives an unsorted task list.
    Validates deadlines, difficulty and duration before processing.
    Calculates a priority score for each task.
    Sorts the list in descending order of priority score.
    Returns the sorted task list.
    """

    # Validate every task.
    for task in task_list:
        deadline = task.get("deadline_date")
        if (not isinstance(deadline, str) or len(deadline) != 10
                or deadline[4] != "-" or deadline[7] != "-"):
            raise ValueError("Deadline must use YYYY-MM-DD format.")
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Deadline must be a valid calendar date.") from None

        # Difficulty must be a whole number within the supported range.
        difficulty = task.get("difficulty")
        if type(difficulty) is not int or not 1 <= difficulty <= 5:
            raise ValueError("Difficulty must be a whole number from 1 to 5.")

        # Duration is measured in hours and follows the form's existing limit.
        duration = task.get("duration")
        if type(duration) not in (int, float) or not 0 < duration <= 100:
            raise ValueError("Duration must be greater than 0 and at most 100 hours.")

    # Calculate how soon each task is due.
    today_date = datetime.now().date()

    # Calculate a score for each task in the shared list.
    for task in task_list:
         
        # Convert the deadline text into a date.
        deadline_date = datetime.strptime(task["deadline_date"], "%Y-%m-%d").date()
        
        # Calculate days until the deadline; negative values indicate overdue tasks.
        deadline_days = (deadline_date - today_date).days
        # Store this value.
        task["deadline_days"] = deadline_days
        difficulty = task["difficulty"]
        duration = task["duration"]
        
        if deadline_days <= 0:
            # Assign a high priority score to tasks due today or overdue.
            task["score"] = 9999.0  
        else:
            # Increase priority for nearer deadlines, greater difficulty and longer duration.
            task["score"] = round(((100 / deadline_days) + (difficulty * 1.5)) * (duration * 0.5), 2)
            

    # Sort by descending priority score; equal scores keep their original order.
    task_list.sort(key=lambda task: task["score"], reverse=True)

    # Return the list.
    return task_list

if __name__ == "__main__":
    # Sample tasks for testing.
    task_list = [
        {"id": 1, "name": "Physics Presentation", "deadline_date": "2026-10-25", "duration": 4, "difficulty": 5, "score": 0.0},
        {"id": 2, "name": "Math Homework", "deadline_date": "2026-11-01", "duration": 2, "difficulty": 3, "score": 0.0},
        {"id": 3, "name": "CS Project Overdue", "deadline_date": "2026-10-10", "duration": 5, "difficulty": 4, "score": 0.0}
    ]

    # Copy each task to preserve the original scores and order for comparison.
    original_tasks = [task.copy() for task in task_list]

    # Call the module and display a message if validation fails.
    try:
        task_list = priority_queue_engine(task_list)
    except ValueError as error:
        print(f"Invalid task: {error}")
    else:
        # Display the original input fields and scores before processing.
        print("Before Processing:")
        if not original_tasks:
            print("No tasks.")
        for task in original_tasks:
            print(f"ID: {task['id']}, Name: {task['name']}, "
                  f"Deadline: {task['deadline_date']}, Duration: {task['duration']} hours, "
                  f"Difficulty: {task['difficulty']}, Score: {task['score']:.2f}")

        # Display each task's ID, score and days until its deadline in sorted order.
        print("\nAfter Processing:")
        if not task_list:
            print("No tasks.")
        for task in task_list:
            print(f"ID: {task['id']}, Score: {task['score']:.2f}, "
                  f"Days until deadline: {task['deadline_days']}")
