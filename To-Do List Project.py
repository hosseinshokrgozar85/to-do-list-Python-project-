
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import datetime

# Initialize global variables
data_file = "tasks.json"
tasks = []

# Load tasks from JSON file
def load_tasks():
    global tasks
    try:
        with open(data_file, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []

# Save tasks to JSON file
def save_tasks():
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

# Validate date format
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Add a new task
def add_task():
    title = title_entry.get()
    description = description_entry.get()
    priority = priority_combobox.get()
    due_date = due_date_entry.get()

    if not title:
        messagebox.showwarning("Input Error", "Title is required.")
        return

    if priority not in ["High", "Medium", "Low"]:
        messagebox.showwarning("Input Error", "Invalid priority selected.")
        return

    if due_date and not validate_date(due_date):
        messagebox.showwarning("Input Error", "Invalid date format. Use YYYY-MM-DD.")
        return

    new_task = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks()
    refresh_task_list()
    clear_inputs()

# Clear input fields
def clear_inputs():
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    priority_combobox.set("Medium")
    due_date_entry.delete(0, tk.END)

# Refresh the task list in the UI
def refresh_task_list():
    task_tree.delete(*task_tree.get_children())
    for i, task in enumerate(tasks):
        task_tree.insert("", "end", iid=i, values=(
            task["title"],
            task["description"],
            task["priority"],
            task["due_date"],
            "Done" if task["completed"] else "Pending"
        ))

# Mark a task as completed or pending
def toggle_task_status():
    selected_item = task_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task.")
        return

    index = int(selected_item[0])
    tasks[index]["completed"] = not tasks[index]["completed"]
    save_tasks()
    refresh_task_list()

# Edit a task
def edit_task():
    selected_item = task_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task.")
        return

    index = int(selected_item[0])
    task = tasks[index]

    title_entry.delete(0, tk.END)
    title_entry.insert(0, task["title"])
    description_entry.delete(0, tk.END)
    description_entry.insert(0, task["description"])
    priority_combobox.set(task["priority"])
    due_date_entry.delete(0, tk.END)
    due_date_entry.insert(0, task["due_date"])

    delete_task(index)

# Delete a task
def delete_task(index=None):
    if index is None:
        selected_item = task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task.")
            return

        index = int(selected_item[0])

    tasks.pop(index)
    save_tasks()
    refresh_task_list()

# Search tasks by title or description
def search_tasks():
    query = search_entry.get().lower()
    task_tree.delete(*task_tree.get_children())
    for i, task in enumerate(tasks):
        if query in task["title"].lower() or query in task["description"].lower():
            task_tree.insert("", "end", iid=i, values=(
                task["title"],
                task["description"],
                task["priority"],
                task["due_date"],
                "Done" if task["completed"] else "Pending"
            ))

# Sort tasks by date or priority
def sort_tasks(key):
    if key == "priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        tasks.sort(key=lambda x: priority_order[x["priority"]])
    elif key == "date":
        tasks.sort(key=lambda x: x["due_date"] or "9999-12-31")
    save_tasks()
    refresh_task_list()

# Set up the main window
root = tk.Tk()
root.title("To-Do List Manager")
root.geometry("900x500")
root.configure(bg="#818589")

# Input fields
input_frame = tk.Frame(root, bg="#818589")
input_frame.pack(pady=10)

# Title
tk.Label(input_frame, text="Title:", bg="#818589").grid(row=0, column=0, sticky=tk.W)
title_entry = tk.Entry(input_frame, width=30, relief="solid", bd=2)
title_entry.grid(row=0, column=1, padx=5)

# Description
tk.Label(input_frame, text="Description:", bg="#818589").grid(row=1, column=0, sticky=tk.W)
description_entry = tk.Entry(input_frame, width=30, relief="solid", bd=2)
description_entry.grid(row=1, column=1, padx=5)

# Priority
tk.Label(input_frame, text="Priority:", bg="#818589").grid(row=2, column=0, sticky=tk.W)
priority_combobox = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], width=28, state="readonly")
priority_combobox.set("Medium")
priority_combobox.grid(row=2, column=1, padx=5)

# Date
tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#818589").grid(row=3, column=0, sticky=tk.W)
due_date_entry = tk.Entry(input_frame, width=30, relief="solid", bd=2)
due_date_entry.grid(row=3, column=1, padx=5)

# Buttons
button_frame = tk.Frame(root, bg="#818589")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Task", command=add_task, relief="solid", bd=2).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Delete Task", command=delete_task, relief="solid", bd=2).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Edit Task", command=edit_task, relief="solid", bd=2).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Change Status", command=toggle_task_status, relief="solid", bd=2).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Sort by Priority", command=lambda: sort_tasks("priority"), relief="solid", bd=2).grid(row=0, column=4, padx=5)
tk.Button(button_frame, text="Sort by Due Date", command=lambda: sort_tasks("date"), relief="solid", bd=2).grid(row=0, column=5, padx=5)

# Search bar and button
search_frame = tk.Frame(button_frame, bg="#818589")
search_frame.grid(row=1, columnspan=6, pady=5)

tk.Label(search_frame, text="Search:", bg="#818589").grid(row=0, column=0, sticky=tk.W)
search_entry = tk.Entry(search_frame, width=20, relief="solid", bd=2)
search_entry.grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="Search", command=search_tasks, relief="solid", bd=2).grid(row=0, column=2, padx=5)

# Task list
task_tree = ttk.Treeview(root, columns=("Title", "Description", "Priority", "Due Date", "Status"), show="headings")
for col in ["Title", "Description", "Priority", "Due Date", "Status"]:
    task_tree.heading(col, text=col)
    task_tree.column(col, width=150)
task_tree.tag_configure("done", background="#A9DFBF")
task_tree.tag_configure("pending", background="#F5B7B1")

def refresh_task_list():
    task_tree.delete(*task_tree.get_children())
    for i, task in enumerate(tasks):
        tag = "done" if task["completed"] else "pending"
        task_tree.insert("", "end", iid=i, values=(
            task["title"],
            task["description"],
            task["priority"],
            task["due_date"],
            "Done" if task["completed"] else "Pending"
        ), tags=(tag,))

 
task_tree.pack(pady=10)

# Load initial tasks
load_tasks()
refresh_task_list()

# Run the main loop
root.mainloop()
