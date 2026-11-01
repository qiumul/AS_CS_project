"""Display a sorted task schedule in a graphical desktop dashboard."""

import tkinter as tk
from tkinter import ttk

# Accept the task-operation callback.
def display_dashboard(sorted_task_list, on_action=None):
    """Open a graphical dashboard containing tasks in priority order.

    Args:
        sorted_task_list: A list of task dictionaries sorted by descending
            priority score.
        on_action: Optional callback that validates and processes task operations.

    Returns:
        True after the user closes the dashboard window.
    """
    window = tk.Tk()
    window.title("Smart Task Scheduler")
    window.geometry("1100x620")
    window.minsize(850, 480)
    window.configure(bg="#F3F6FA")

    # Configure the table's visual style.
    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure(
        "Task.Treeview",
        background="#FFFFFF",
        fieldbackground="#FFFFFF",
        foreground="#1F2937",
        rowheight=42,
        font=("Arial", 11),
        borderwidth=0,
    )
    style.configure(
        "Task.Treeview.Heading",
        background="#E8EEF7",
        foreground="#334155",
        font=("Arial", 10, "bold"),
        relief="flat",
        padding=10,
    )
    style.map("Task.Treeview", background=[("selected", "#DCE8FF")])

    # Give invalid input fields a red border and a light red background.
    style.map(
        "Task.TEntry",
        bordercolor=[("invalid", "#DC2626")],
        lightcolor=[("invalid", "#DC2626")],
        darkcolor=[("invalid", "#DC2626")],
        fieldbackground=[("invalid", "#FEF2F2")],
    )

    # The header introduces the schedule and reports the collection size.
    header = tk.Frame(window, bg="#172554", padx=32, pady=24)
    header.pack(fill="x")
    tk.Label(
        header,
        text="SMART TASK SCHEDULER",
        bg="#172554",
        fg="#FFFFFF",
        font=("Arial", 22, "bold"),
    ).pack(anchor="w")
    # Keep the label so the task count can be updated.
    count_label = tk.Label(
        header,
        text=f"{len(sorted_task_list)} task(s) in your current schedule",
        bg="#172554",
        fg="#BFDBFE",
        font=("Arial", 11),
    )
    count_label.pack(anchor="w", pady=(6, 0))

    content = tk.Frame(window, bg="#F3F6FA", padx=32, pady=28)
    content.pack(fill="both", expand=True)

    # Keep the selected ID and input widgets.
    selected_id = None
    fields = {}
    entries = {}
    buttons = {}

    # Fill the form for a selected task, or clear it when selection is cancelled.
    def select_task(task_id):
        nonlocal selected_id
        # Clicking blank table space clears the selection.
        if task_id is None:
            selected_id = None
            for field, variable in fields.items():
                variable.set("")
                entries[field].state(["!invalid"])
            buttons["Edit selected"].configure(state="disabled")
            buttons["Delete selected"].configure(state="disabled")
            status_message.set("Enter a new task, or select a row to edit or delete.")
            return
        task = next(task for task in sorted_task_list if task["id"] == task_id)
        selected_id = task_id
        for field, variable in fields.items():
            variable.set(str(task[field]))
            entries[field].state(["!invalid"])
        buttons["Edit selected"].configure(state="normal")
        buttons["Delete selected"].configure(state="normal")
        status_message.set(f"Selected task #{task_id}. Change the fields and click Edit selected.")

    # Send button actions and display the returned result.
    def submit_task(command):
        nonlocal selected_id
        if command != "ADD" and selected_id is None:
            status_message.set("Select a task row first.")
            return
        data = {field: variable.get() for field, variable in fields.items()}
        data["id"] = selected_id
        # Clear previous field highlights before checking the current input.
        for entry in entries.values():
            entry.state(["!invalid"])
        success, message, invalid_field = on_action(command, data)
        status_message.set(message)
        if not success:
            # Highlight the field rejected by the input check.
            entries[invalid_field].state(["invalid"])
            entries[invalid_field].focus_set()
            return
        refresh()
        selected_id = None
        for variable in fields.values():
            variable.set("")
        buttons["Edit selected"].configure(state="disabled")
        buttons["Delete selected"].configure(state="disabled")

    # Reuse the code after each task operation.
    def refresh():
        """Update the task count and redraw the original task display."""
        # Update the count and remove the previous display.
        count_label.configure(text=f"{len(sorted_task_list)} task(s) in your current schedule")
        for child in content.winfo_children():
            child.destroy()
        # Selection handles an empty collection without attempting table output.
        if len(sorted_task_list) == 0:
            empty_panel = tk.Frame(
                content,
                bg="#FFFFFF",
                highlightbackground="#DDE4EE",
                highlightthickness=1,
            )
            empty_panel.pack(fill="both", expand=True)
            tk.Label(
                empty_panel,
                text="✓",
                bg="#FFFFFF",
                fg="#16A34A",
                font=("Arial", 42, "bold"),
            ).pack(pady=(95, 12))
            tk.Label(
                empty_panel,
                text="No tasks for now, just have a rest!",
                bg="#FFFFFF",
                fg="#1F2937",
                font=("Arial", 18, "bold"),
            ).pack()
            tk.Label(
                empty_panel,
                text="New tasks will appear here after they are scheduled.",
                bg="#FFFFFF",
                fg="#64748B",
                font=("Arial", 11),
            ).pack(pady=(10, 0))
        else:
            columns = (
                "position",
                "task",
                "deadline",
                "duration",
                "difficulty",
                "score",
                "status",
            )
            task_table = ttk.Treeview(
                content,
                columns=columns,
                show="headings",
                selectmode="browse",
                style="Task.Treeview",
            )

            headings = {
                "position": "NO.",
                "task": "TASK",
                "deadline": "DEADLINE",
                "duration": "DURATION",
                "difficulty": "DIFFICULTY",
                "score": "SCORE",
                "status": "STATUS",
            }
            widths = {
                "position": 55,
                "task": 260,
                "deadline": 120,
                "duration": 130,
                "difficulty": 110,
                "score": 90,
                "status": 130,
            }

            # Sequence the table configuration before inserting task rows.
            for column in columns:
                task_table.heading(column, text=headings[column])
                task_table.column(
                    column,
                    width=widths[column],
                    minwidth=widths[column],
                    anchor="center" if column != "task" else "w",
                )

            task_table.tag_configure(
                "urgent",
                background="#FFF1F2",
                foreground="#B91C1C",
                font=("Arial", 11, "bold"),
            )
            task_table.tag_configure("standard", background="#FFFFFF")

            # Iterate through the shared list-of-dictionaries data structure.
            for index, task in enumerate(sorted_task_list):
                status = ""
                row_tag = "standard"

                # Show overdue tasks separately; tasks due today are urgent.
                if task["deadline_days"] < 0:
                    status = "● OVERDUE"
                    row_tag = "urgent"
                elif task["deadline_days"] == 0:
                    status = "● URGENT"
                    row_tag = "urgent"

                task_table.insert(
                    "",
                    "end",
                    # Identify the selected task by its ID.
                    iid=str(task["id"]) if on_action is not None else str(index),
                    values=(
                        index + 1,
                        task["name"],
                        f"{task['deadline_days']} day(s)",
                        f"{task['duration']} hour(s)",
                        task["difficulty"],
                        f"{task['score']:.2f}",
                        status,
                    ),
                    tags=(row_tag,),
                )

            scrollbar = ttk.Scrollbar(content, orient="vertical", command=task_table.yview)
            task_table.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            task_table.pack(side="left", fill="both", expand=True)

            # Let the input controls know which task the user selected.
            if on_action is not None:
                task_table.bind(
                    "<<TreeviewSelect>>",
                    lambda event: select_task(int(task_table.selection()[0]))
                    if task_table.selection() else None,
                )
                # Cancel selection when clicking blank space.
                task_table.bind(
                    "<Button-1>",
                    lambda event: (
                        task_table.selection_remove(task_table.selection()),
                        task_table.focus(""),
                        select_task(None),
                    ) if task_table.identify_region(event.x, event.y) == "nothing"
                    and selected_id is not None else None,
                )

    # Create input controls when supplied an operation callback.
    if on_action is not None:
        window.geometry("1100x740")
        window.minsize(1100, 640)
        status_message = tk.StringVar(window, "Enter a new task, or select a row to edit or delete.")
        panel = tk.Frame(window, bg="#F3F6FA", padx=32, pady=14)
        panel.pack(fill="x", before=content)
        # Create the four task input fields.
        for column, (field, label) in enumerate((("name", "Task name"),
                ("deadline_date", "Deadline YYYY-MM-DD"), ("duration", "Duration in hours"),
                ("difficulty", "Difficulty 1-5"))):
            tk.Label(panel, text=label, bg="#F3F6FA", fg="#334155",
                     font=("Arial", 10)).grid(row=0, column=column, sticky="w")
            fields[field] = tk.StringVar(window)
            entry = ttk.Entry(panel, textvariable=fields[field], width=20, style="Task.TEntry")
            entry.grid(row=1, column=column, sticky="ew", padx=(0, 12), pady=(5, 12))
            entries[field] = entry
            panel.columnconfigure(column, weight=1)

        # Connect the three GUI buttons and display operation results.
        button_panel = tk.Frame(panel, bg="#F3F6FA")
        button_panel.grid(row=2, column=0, columnspan=4, sticky="w")
        for label, command in (("Add task", "ADD"), ("Edit selected", "EDIT"),
                               ("Delete selected", "DELETE")):
            button = ttk.Button(button_panel, text=label,
                                command=lambda action=command: submit_task(action))
            button.pack(side="left", padx=(0, 12))
            buttons[label] = button
            if command != "ADD":
                button.configure(state="disabled")
        tk.Label(panel, textvariable=status_message, bg="#F3F6FA", fg="#334155",
                 font=("Arial", 10), anchor="w", wraplength=1000).grid(
                     row=3, column=0, columnspan=4, sticky="ew", pady=(10, 0))
    # Draw the initial task display.
    refresh()

    close_button = tk.Button(
        window,
        text="Close Dashboard",
        command=window.destroy,
        bg="#2563EB",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=18,
        pady=10,
        cursor="hand2",
    )
    # Reserve space for the close button before the task table fills the window.
    close_button.pack(side="bottom", before=content, pady=(0, 22))

    window.mainloop()
    return True

if __name__ == "__main__":
    # Open an empty dashboard when this module is assessed independently.
    display_dashboard([])
