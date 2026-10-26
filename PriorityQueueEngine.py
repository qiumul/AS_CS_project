from datetime import datetime

def priority_queue_engine(task_list):
    """
    Receives an unsorted task list.
    Calculates a priority score for each task.
    Sorts the list in descending order of priority score.
    Returns the sorted task list.
    """

    # Get the current date
    today_date = datetime.now().date()

    # Iterate through every task to set priority score
    for task in task_list:
         
        # Convert the string type into date type
        deadline_date = datetime.strptime(task["deadline_date"], "%Y-%m-%d").date()
        
        # Get factors of priority score
        deadline_days = (deadline_date - today_date).days # Calculate the days before the ddl
        difficulty = task["difficulty"]
        duration = task["duration"]
        
        if deadline_days <= 0:
            # If the deadline has passed or is today, set the maximum possible priority score
            task["score"] = 9999.0  
        else:
            # Otherwise calculate the priority score
            task["score"] = round(((100 / deadline_days) + (difficulty * 1.5)) * (duration * 0.5), 2)
            

    # Bubble sort
    list_length = len(task_list)

    # Outer loop for sort
    for row in range(list_length):
        # Boolean to indicate whether objects have been swapped
        is_swapped = False

        # Inner loop for sort
        for column in range(0, list_length - row - 1):
            if task_list[column]["score"] < task_list[column + 1]["score"]:
                # Swap the dictionary objects in place if current is less than next
                task_list[column], task_list[column + 1] = task_list[column + 1], task_list[column]
                is_swapped = True
                
        # If no elements were swapped in this pass, the list is already sorted
        if not is_swapped:
            break
            
    # Return sorted task list
    return task_list

if __name__ == "__main__":
    # Simulated input
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