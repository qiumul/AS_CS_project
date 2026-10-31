"""Display a sorted task schedule in a graphical desktop dashboard."""

import tkinter as tk
from tkinter import ttk


def display_dashboard(sorted_task_list):
    """Open a graphical dashboard containing tasks in priority order.

    Args:
        sorted_task_list: A list of task dictionaries sorted by descending
            priority score.

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
    tk.Label(
        header,
        text=f"{len(sorted_task_list)} task(s) in your current schedule",
        bg="#172554",
        fg="#BFDBFE",
        font=("Arial", 11),
    ).pack(anchor="w", pady=(6, 0))

    content = tk.Frame(window, bg="#F3F6FA", padx=32, pady=28)
    content.pack(fill="both", expand=True)

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

            # Module 2 places the highest-priority task at index zero.
            if index == 0:
                status = "● URGENT"
                row_tag = "urgent"

            task_table.insert(
                "",
                "end",
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
    """
    close_button.pack(pady=(0, 22))
    """
    # Added: reserve space for the close button before the task table fills the window.
    close_button.pack(side="bottom", before=content, pady=(0, 22))

    window.mainloop()
    return True


if __name__ == "__main__":
    # Open an empty dashboard when this module is assessed independently.
    display_dashboard([])
