from tkinter import *
from tkinter import ttk
import sqlite3, os
from PIL import ImageTk, Image

root = Tk()
root.geometry("500x280")
root.title("To-do List")

text_to_do = StringVar()
im_checked = ImageTk.PhotoImage(Image.open("im_checked.png").resize((16, 16)))
im_not_checked = ImageTk.PhotoImage(Image.open("im_not_checked.png").resize((16, 16)))

class ToDoList:
    def __init__(self):
        self.main()

    def add_item(self):
        db = sqlite3.connect('connection')
        cursor = db.cursor()
        cursor.execute("INSERT INTO todolist VALUES (NULL, ?, ?)", (False, text_to_do.get()))
        db.commit()
        db.close()
        self.show_items()

    def remove_item(self):
        if todo_list_items.focus() != "":
            db = sqlite3.connect('connection')
            cursor = db.cursor()
            cursor.execute("DELETE FROM todolist WHERE ID = ?", (todo_list_items.focus(),))
            db.commit()
            db.close()
            self.show_items()

    def mark_as_completed(self):
        db = sqlite3.connect("connection")
        cursor = db.cursor()
        cursor.execute('SELECT * FROM todolist')
        result = cursor.fetchall()
        try:
            for row in result:
                if int(row[0]) == int(todo_list_items.focus()):
                    if row[1] == False:
                        cursor.execute("UPDATE todolist SET done = ? WHERE id = ?", (True, todo_list_items.focus()))
                    else:
                        cursor.execute("UPDATE todolist SET done = ? WHERE id = ?", (False, todo_list_items.focus()))
                    db.commit()
                    db.close()
                    break
            self.show_items()
        except:
            db.close()
            pass

    def show_items(self):
        records = todo_list_items.get_children()
        for element in records:
            todo_list_items.delete(element)
        db = sqlite3.connect('connection')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todolist ORDER BY id DESC")
        query = cursor.fetchall()
        for row in query:
            if row[1] == False:
                todo_list_items.insert("", 0, value=row[2:], iid=row[0], tag="unchecked")
            else:
                todo_list_items.insert("", 0, value=row[2:], iid=row[0], tag="checked")
        db.close()

    def main(self):
        if os.path.isfile("connection"):
            db = sqlite3.connect('connection')
            db.close()
        else:
            db = sqlite3.connect('connection')
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE todolist (\
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            done BOOLEAN NOT NULL,
                            task VARCHAR(30) NOT NULL)""")
        self.show_items()

def on_double_click(event):
    todo.mark_as_completed()

def handle_click(event):
    if todo_list_items.identify_region(event.x, event.y) == "separator":
        return "break"

todo_list_items = ttk.Treeview(root, columns=2, height=10, selectmode='browse')
todo_list_items.grid(row=1, column=0)
todo_list_items.heading("#0", text="", anchor=W)
todo_list_items.column("#0", minwidth=40, width=40)
todo_list_items.heading(2, text="Item", anchor=W)
todo_list_items.column(2, minwidth=380, width=380)


todo_list_items.tag_configure("checked", image=im_checked)
todo_list_items.tag_configure("unchecked", image=im_not_checked)
todo_list_items.bind("<Double-1>", on_double_click)
todo_list_items.bind("<Button-1>", handle_click)
todo = ToDoList()
Entry(root, textvariable=text_to_do, width=70).grid(row=0, column=0, sticky=N, padx=5, pady=5)
Button(root, text="Add", command=todo.add_item).grid(row=0, column=1, sticky=NW, padx=5)
Button(root, text="Delete", command=todo.remove_item).grid(row=1, column=1, sticky=NW, padx=0)
root.resizable(False, False)
root.mainloop()