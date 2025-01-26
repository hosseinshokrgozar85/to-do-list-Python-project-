#Imports
# from tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox , filedialog
import json
import datetime

data_file = "Data.json"
Tasks = []


# Functions
# Load Json data file
def load_saved_data():
    load_task = json.load(data_file)


def save_data():
# add a new-task
def add_task():
    title = t.get()
    description = d.get()
    date = da.get()
    priority = p.get()


    if not title :
        messagebox.showwarning("Input Error", "Title is required.")
        return







#Edit a task
def edit_task():
    selected_task = task_grid.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task.")
        return















task_grid = ttk.Treeview(root , columns=("Title" , "Date" , "Priority" , "Description" , "stats" )
for col in ["Title", "Description", "Priority", "Due Date", "Status"]:
    task_grid.heading(col, text=col)
    task_grid.column(col, width=150)

task_grid.pack(pady=15)



root = Tk()
root.title("To-Do List ")
root.geometry("900x500")

style = ttk.style()

#title field
t = Entry(root , width=30 , bg="#D3D3D3" , fg="black" )
t.pack()

#description field
d = Entry(root , width=30 , bg="#D3D3D3" , fg="black" )
d.pack( ipady=15)

#date field
da = Entry(root , width=30 , bg="#D3D3D3" , fg="black" )
da.pack()

#priority field
p = Entry(root , width=30 , bg="#D3D3D3" , fg="black" )
p.pack()




load_tasks()
refresh_task_list()

root.mainloop()