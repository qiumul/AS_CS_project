def manage_tasks(task_list, command, task_data):
    if command == "ADD":
        task_list.append(task_data)

    elif command == "DELETE":
        target_id = task_data["id"]
        found = False
        for task in task_list:
            if task["id"] == target_id:
                task_list.remove(task)
                found = True
                break
        if not found:
            print(f"Task ID {target_id} not found.")

    elif command == "EDIT":
        target_id = task_data["id"]
        found = False
        for task in task_list:
            if task["id"] == target_id:
                for key in task_data:
                    if key != "id":
                        task[key] = task_data[key]
                found = True
                break
        if not found:
            print(f"Task ID {target_id} not found.")

    else:
        print(f"Invalid command: {command}")

    if hasattr(task_list, "on_change"):
        task_list.on_change()  # Trigger the on_change event

    return task_list
