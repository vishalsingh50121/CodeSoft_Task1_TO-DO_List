import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.filename = "todo_gui.json"
        self.tasks = self.load_tasks()
        
        # Create UI
        self.create_widgets()
        self.update_task_list()
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
    
    def create_widgets(self):
        # Frame for task entry
        entry_frame = ttk.Frame(self.root, padding="10")
        entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Task description
        ttk.Label(entry_frame, text="Task:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(entry_frame, width=40)
        self.task_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Priority
        ttk.Label(entry_frame, text="Priority:").grid(row=1, column=0, sticky=tk.W)
        self.priority_var = tk.StringVar(value="medium")
        priorities = ttk.Combobox(entry_frame, textvariable=self.priority_var, 
                                 values=["high", "medium", "low"], width=10)
        priorities.grid(row=1, column=1, sticky=tk.W)
        
        # Due date
        ttk.Label(entry_frame, text="Due Date:").grid(row=2, column=0, sticky=tk.W)
        self.due_entry = ttk.Entry(entry_frame, width=15)
        self.due_entry.grid(row=2, column=1, sticky=tk.W)
        ttk.Label(entry_frame, text="(YYYY-MM-DD)").grid(row=2, column=2, sticky=tk.W)
        
        # Add button
        add_btn = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=3, column=1, sticky=tk.E)
        
        # Task list
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.task_tree = ttk.Treeview(list_frame, columns=("ID", "Description", "Priority", "Due", "Status"), 
                                     show="headings", selectmode="browse")
        
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Due", text="Due Date")
        self.task_tree.heading("Status", text="Status")
        
        self.task_tree.column("ID", width=50)
        self.task_tree.column("Description", width=200)
        self.task_tree.column("Priority", width=80)
        self.task_tree.column("Due", width=100)
        self.task_tree.column("Status", width=100)
        
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons frame
        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        complete_btn = ttk.Button(btn_frame, text="Mark Complete", command=self.complete_task)
        complete_btn.grid(row=0, column=0, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete Task", command=self.delete_task)
        delete_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Clear Completed", command=self.clear_completed)
        clear_btn.grid(row=0, column=2, padx=5)
        
        filter_frame = ttk.Frame(btn_frame)
        filter_frame.grid(row=0, column=3, padx=20)
        
        ttk.Label(filter_frame, text="Filter:").grid(row=0, column=0)
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, 
                       value="all", command=self.update_task_list).grid(row=0, column=1)
        ttk.Radiobutton(filter_frame, text="Pending", variable=self.filter_var, 
                       value="pending", command=self.update_task_list).grid(row=0, column=2)
        ttk.Radiobutton(filter_frame, text="Completed", variable=self.filter_var, 
                       value="completed", command=self.update_task_list).grid(row=0, column=3)
    
    def add_task(self):
        description = self.task_entry.get().strip()
        if not description:
            messagebox.showwarning("Warning", "Task description cannot be empty!")
            return
            
        priority = self.priority_var.get()
        due_date = self.due_entry.get().strip() or None
        
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.update_task_list()
        
        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.task_entry.focus()
    
    def update_task_list(self):
        # Clear current items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        filter_type = self.filter_var.get()
        
        for task in self.tasks:
            if filter_type == "all" or \
               (filter_type == "completed" and task["completed"]) or \
               (filter_type == "pending" and not task["completed"]):
                
                status = "Completed" if task["completed"] else "Pending"
                due_date = task["due_date"] if task["due_date"] else ""
                
                self.task_tree.insert("", tk.END, values=(
                    task["id"],
                    task["description"],
                    task["priority"].capitalize(),
                    due_date,
                    status
                ))
    
    def complete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return
            
        item = self.task_tree.item(selected[0])
        task_id = item["values"][0]
        
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                self.update_task_list()
                return
    
    def delete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
            
        item = self.task_tree.item(selected[0])
        task_id = item["values"][0]
        
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
        self.update_task_list()
    
    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.save_tasks()
        self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
