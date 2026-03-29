# EX07 Developing a To-Do Manager using Python GUI

---

## AIM:

To develop a To-Do Manager application using Python with a graphical user interface to manage tasks with deadlines and status tracking.

---

## DESIGN STEPS:

### Step 1:

Design the user interface layout using Tkinter.

### Step 2:

Create input fields for task entry and date selection.

### Step 3:

Use `DateEntry` widget from tkcalendar for selecting dates.

### Step 4:

Implement task storage using a list and JSON file.

### Step 5:

Display tasks using Treeview widget.

### Step 6:

Add functionality to mark tasks as completed.

### Step 7:

Implement status checking (Pending, Done, Overdue).

### Step 8:

Add save and load functionality using JSON.

### Step 9:

Handle user interactions (button clicks, double-click events).

### Step 10:

Run the application and verify task management features.

---

## PROGRAM:

```python
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

FILE_NAME = "tasks.json"

BG = "#0f0f0f"
CARD = "#1a1a1a"
ACCENT = "#8b0000"
TEXT = "#e5e5e5"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Manager")
        self.root.geometry("650x600")
        self.root.configure(bg=BG)

        self.tasks = []

        tk.Label(root, text="TASK MANAGER", font=("Segoe UI", 22, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=10)

        frame = tk.Frame(root, bg=CARD)
        frame.pack(padx=15, pady=10, fill="x")

        self.task_entry = tk.Entry(frame, font=("Segoe UI", 12),
                                  bg="#262626", fg=TEXT, bd=0,
                                  insertbackground="white")
        self.task_entry.pack(padx=10, pady=10, fill="x")

        self.date_entry = DateEntry(frame,
                                   date_pattern="yyyy-mm-dd",
                                   background=ACCENT,
                                   foreground="white",
                                   borderwidth=0)
        self.date_entry.pack(pady=5)

        tk.Button(frame, text="ADD TASK", bg=ACCENT, fg="white",
                  command=self.add_task, bd=0).pack(pady=10)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background=CARD,
                        foreground=TEXT,
                        fieldbackground=CARD,
                        rowheight=30,
                        font=("Segoe UI", 11))

        style.map("Treeview",
                  background=[("selected", ACCENT)])

        columns = ("Task", "Date", "Status")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.bind("<Double-1>", self.toggle_task)

        tk.Button(root, text="SAVE TASKS", bg=ACCENT, fg="white",
                  command=self.save_tasks, width=25).pack(pady=10)

        self.load_tasks()
        self.refresh_ui()

    def add_task(self):
        task = self.task_entry.get().strip()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")

        if not task:
            messagebox.showwarning("Error", "Task cannot be empty")
            return

        self.tasks.append({
            "task": task,
            "date": date,
            "done": False
        })

        self.task_entry.delete(0, tk.END)
        self.refresh_ui()

    def get_status(self, task):
        if task["done"]:
            return "✔ DONE"

        today = datetime.now().date()
        task_date = datetime.strptime(task["date"], "%Y-%m-%d").date()

        if today > task_date:
            return "⚠ OVERDUE"
        return "⏳ PENDING"

    def refresh_ui(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, t in enumerate(self.tasks):
            status = self.get_status(t)
            checkbox = "☑" if t["done"] else "☐"

            self.tree.insert("", "end", iid=i,
                             values=(f"{checkbox} {t['task']}",
                                     t["date"],
                                     status))

    def toggle_task(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        index = int(selected[0])
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.refresh_ui()

    def save_tasks(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.tasks, f, indent=4)
        messagebox.showinfo("Saved", "Tasks saved successfully!")

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                self.tasks = json.load(f)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
```

---

## OUTPUT:

<img width="810" height="781" alt="image" src="https://github.com/user-attachments/assets/4695bcc8-7cb8-4ff0-8271-e96fb35c9fb9" />



---

## RESULT:

The To-Do Manager application was successfully developed using Python Tkinter. The program allows users to add, manage, and track tasks efficiently with status indicators and persistent storage.
