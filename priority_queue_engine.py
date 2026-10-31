from datetime import datetime

def priority_queue_engine(task_list):
    """
    Receives an unsorted task list.
    Calculates a priority score for each task.
    Sorts the list in descending order of priority score.
    Returns the sorted task list.
    """

    # Use the current date to calculate how soon each task is due.
    today_date = datetime.now().date()

    # Calculate a score for each task in the shared list.
    for task in task_list:
         
        # Convert the deadline text into a date for subtraction.
        deadline_date = datetime.strptime(task["deadline_date"], "%Y-%m-%d").date()
        
        # Calculate days until the deadline; negative values indicate overdue tasks.
        deadline_days = (deadline_date - today_date).days
        # Store this value so the dashboard can display it.
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

    # Output task list before processing the module
    print("Before Processing:")
    for task in task_list:
        print(task)

    # Call the developed module
    task_list = priority_queue_engine(task_list)

    # Output task list after processing the module
    print("\nAfter Processing: ")
    for task in task_list:
         print(task)