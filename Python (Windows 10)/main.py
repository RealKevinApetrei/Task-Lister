import tkinter as tk
from tkinter import font
from tkinter import messagebox

import os

import config


class Application(tk.Tk): # Application Class Object
    def __init__(self):
        super().__init__() # Superclass (tk.Tk)
        
        self.title(config.PROGRAM_NAME + " | " + config.BUILD_VERSION + " | By " + config.AUTHOR) # Window Title
        self.geometry("500x500") # Window Size (Template)
        self.resizable(0, 0) # not Resizable
        
        # Fonts
        self.hel15b = font.Font(family="Helvetica", size=15, weight="bold") # Font (Helvetica, 15, Bold)
        self.hel30b = font.Font(family="Helvetica", size=30, weight="bold") # Font (Helvetica, 30, Bold)
        self.sys20bu = font.Font(family="system", size=20, weight="bold", underline=1) # Font (system, 20, Bold, Underline)
        self.hel15 = font.Font(family="Helvetica", size=15) # Font (Helvetica, 15)

    def __repr__(self):
        __name = self.__class__
        __type = type(self)
        __module = type.__module__
        __qualname = type.__qualname__

        return f"""\
        Class Name: {__name}
        Class Details: {config.PROGRAM_NAME}

        Build Version: {config.BUILD_VERSION}
        Author: {config.AUTHOR}
        
        Class Type: {__type}
        Class Module: {__module}
        Class Qualname: {__qualname}
        """
        

class CustomListbox(tk.Listbox):
    def __init__(self, master=None,**kw):
        tk.Listbox.__init__(self, master, kw)
        kw['selectmode'] = tk.SINGLE

        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)
        
        self.curIndex = None

    def set_current(self, event=None):
        self.curIndex = self.nearest(event.y)

    def shift_selection(self, event=None):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i


class CustomEntry(tk.Entry):
    def __init__(self, master=None, label="Enter a task", fg="gray35", **kwargs):
        tk.Entry.__init__(self, master, **kwargs)

        self.typing_fg = "black"
        self.out_fg = fg
        self.label = label
        
        self.on_exit()
        self.bind('<FocusIn>', self.on_entry)
        self.bind('<FocusOut>', self.on_exit)
        
    def on_entry(self, event=None):
        if self.get() == self.label:
            self.delete(0, tk.END)
            self.configure(fg=self.typing_fg)

    def on_exit(self, event=None):
        if not self.get():
            self.insert(0, self.label)
            self.reset_font()

    def reset_font(self):
        self.configure(fg=self.out_fg)


class Main(Application): # Main Window
    def __init__(self, imported_tasks):
        super().__init__() # Superclass (Application)

        # Variables
        self.task_list = imported_tasks

        # Other Setup
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Window Contents
            # Enter Task
        self.task_entry = CustomEntry(self, width=43, font=self.hel15)
        self.task_entry.place(x=10, y=10)

            # List Task
        self.list_task_button = tk.Button(self, text="List", command=self.list_task, width=10, relief="raised", bd=3, bg="gray85")
        self.list_task_button.place(x=10, y=50)
        
            # Delete Task
        self.delete_task_button = tk.Button(self, text="Delete", command=self.delete_task, width=10, relief="raised", bd=3, bg="gray85")
        self.delete_task_button.place(x=110 , y=50)

            # Task Listbox
        # self.task_listbox = tk.Listbox(self, width=79, height=20, relief="solid")
        self.task_listbox = CustomListbox(self, width=79, height=20, relief="solid")
        self.task_listbox.place(x=10, y=90)

        self.update_tasks()

    def list_task(self): # Lists task based on Entry input
        self.to_list = self.task_entry.get()
        self.task_list_lower = [item.lower() for item in self.task_list]

        self.task_entry.delete(0, "end")
        self.task_entry.reset_font()

        if self.to_list != "Enter a task" and self.to_list != "":
            if self.to_list.lower() in self.task_list_lower:
                if not messagebox.askyesno("Duplicate Task", "Are you sure you want to list a duplicate/similar task?"):
                    return
            self.task_list.append(self.to_list)
            self.update_tasks()
        else:
            messagebox.showinfo("Uh oh!", "You need to enter an item.")

    def update_tasks(self): # Update Current Tasks
        self.task_listbox.delete(0, "end")
        for task in self.task_list:
            self.task_listbox.insert("end", task)

    def close(self): # If program is closed...
        if messagebox.askokcancel("Quit", "Are you sure you want to quit and save?"):
            try:
                with open("tasks.data", "w+") as task_file:
                    task_file.truncate(0)
                    task_file.write(",".join(self.task_list))
            except Exception as e:
                print(f"ERROR: {e}")
            finally:
                self.destroy()
    
    def delete_task(self): # Delete task...
        try:
            self.task_list.remove(self.task_listbox.get(tk.ANCHOR))
            self.update_tasks()
        except ValueError:
            pass

def setup(): # Main Menu Setup
    try:
        os.chdir(r"./Data/")
    except FileNotFoundError:
        os.chdir(r"./Python (for Windows 10)/Data/") # Edit based on folder name

    # Get Task Data
    with open("tasks.data", "w+") as task_file:
        data = task_file.read()
        if data:
            imported_tasks = data.split(",")
        else:
            imported_tasks = []

    main = Main(imported_tasks) # Main Menu Window (init)
    main.mainloop() # Window Loop


if __name__ == "__main__": # If Program is run directly...
    setup() # App Setup