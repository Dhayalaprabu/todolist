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

        # Title
        tk.Label(root, text="TASK MANAGER", font=("Segoe UI", 22, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=10)

        # Input Frame
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

        # Treeview (Better than Listbox)
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

        # Bind click
        self.tree.bind("<Double-1>", self.toggle_task)

        # Save button
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

            # Checkbox style text
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