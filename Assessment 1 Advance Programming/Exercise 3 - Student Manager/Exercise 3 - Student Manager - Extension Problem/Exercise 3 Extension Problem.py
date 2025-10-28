# Exercise 3: Student Manager (GUI with improved layout)

import tkinter as tk
from tkinter import ttk, messagebox
import os

# ----------------------- CONFIG -----------------------
STUDENT_FILE = "C:/Users/peter/.vscode/Activity/Assessment 1 Advance Programming/Exercise 3 - Student Manager/Exercise 3 - Student Manager - Extension Problem/studentMarks.txt.txt"

# ----------------------- HELPER FUNCTIONS -----------------------
def load_students(filename=STUDENT_FILE):
    students_dict = {}
    if not os.path.isfile(filename):
        return students_dict
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line: continue
            parts = line.split(',')
            if len(parts) == 6:
                name, number, coursework, exam, overall, grade = parts
                students_dict[name] = (number, int(coursework), int(exam), int(overall), grade)
    return students_dict

def save_to_file():
    with open(STUDENT_FILE, "w", encoding="utf-8") as f:
        for name, (number, coursework, exam, overall, grade) in students.items():
            f.write(f"{name},{number},{coursework},{exam},{overall},{grade}\n")

def capitalize_name(name):
    return name.title()

def find_student(target):
    target = target.strip().lower()
    for name, data in students.items():
        if name.lower() == target or data[0].lower() == target:
            return name
    return None

def check_highest_lowest(new_name):
    if not students: return
    highest = max(students.items(), key=lambda x: x[1][3])
    lowest = min(students.items(), key=lambda x: x[1][3])
    overall = students[new_name][3]
    if overall == highest[1][3]:
        messagebox.showinfo("New Highest Score!", f"{new_name} now has the highest overall score ({overall}). 🎉")
    elif overall == lowest[1][3]:
        messagebox.showinfo("New Lowest Score!", f"{new_name} now has the lowest overall score ({overall}). 😢")

# ----------------------- GUI SETUP -----------------------
root = tk.Tk()
root.title("Student Manager")
root.geometry("650x600")
root.resizable(0, 0)

# Title
title = tk.Label(root, text='Student Manager', font=('Helvetica', 18, 'bold'))
title.pack(pady=10)

# Combo Box for selecting student
combo_frame = tk.Frame(root)
combo_frame.pack(pady=5)
tk.Label(combo_frame, text="Select Student:", font=('Helvetica', 12)).pack(side='left', padx=5)
selected_student = tk.StringVar()
students = load_students()
entry = ttk.Combobox(combo_frame, textvariable=selected_student, values=list(students.keys()), width=30, state='readonly')
entry.pack(side='left', padx=5)

# Info frame for student details
info_frame = tk.Frame(root, bg='lightgrey', bd=2, relief='groove', width=600, height=250)
info_frame.pack(pady=10)
info_frame.pack_propagate(False)

# ----------------------- GUI FUNCTIONS -----------------------
def clear_info_frame():
    for w in info_frame.winfo_children():
        w.destroy()

def display_student_info(student_name):
    clear_info_frame()
    if student_name not in students:
        messagebox.showerror("Error", "Student not found.")
        return
    number, coursework, exam, overall, grade = students[student_name]
    txt = tk.Text(info_frame, bg='lightgrey', bd=0, wrap='word', font=('Helvetica', 11))
    txt.pack(fill='both', expand=True, padx=5, pady=5)
    txt.insert('end', f"  Name: {student_name}\n")
    txt.insert('end', f"  Number: {number}\n")
    txt.insert('end', f"  Coursework: {coursework}\n")
    txt.insert('end', f"  Exam: {exam}\n")
    txt.insert('end', f"  Overall: {overall}\n")
    txt.insert('end', f"  Grade: {grade}\n\n")
    txt.config(state='disabled')

def show_all_students():
    clear_info_frame()
    txt = tk.Text(info_frame, bg='lightgrey', bd=0, wrap='word', font=('Helvetica', 11))
    txt.pack(fill='both', expand=True, padx=5, pady=5)
    for name, data in students.items():
        number, coursework, exam, overall, grade = data
        txt.insert('end', f"  Name: {name}\n")
        txt.insert('end', f"  Number: {number}\n")
        txt.insert('end', f"  Coursework: {coursework}\n")
        txt.insert('end', f"  Exam: {exam}\n")
        txt.insert('end', f"  Overall: {overall}\n")
        txt.insert('end', f"  Grade: {grade}\n\n")
    txt.config(state='disabled')

def show_highest():
    if not students: return
    name, _ = max(students.items(), key=lambda x: x[1][3])
    display_student_info(name)

def show_lowest():
    if not students: return
    name, _ = min(students.items(), key=lambda x: x[1][3])
    display_student_info(name)

def view_record():
    name = selected_student.get()
    if name:
        display_student_info(name)
    else:
        messagebox.showinfo("No selection", "Please select a student.")

# ----------------------- BUTTON FUNCTIONS -----------------------
def add_record():
    add_win = tk.Toplevel(root)
    add_win.title("Add Student Record")
    add_win.geometry("300x300")
    fields = ["Name", "Number", "Coursework", "Exam", "Overall", "Grade"]
    entries = {}
    for i, field in enumerate(fields):
        tk.Label(add_win, text=field).grid(row=i, column=0, padx=5, pady=5)
        e = tk.Entry(add_win)
        e.grid(row=i, column=1, padx=5, pady=5)
        entries[field] = e

    def save_new():
        try:
            name = capitalize_name(entries["Name"].get())
            number = entries["Number"].get().strip()
            coursework = int(entries["Coursework"].get())
            exam = int(entries["Exam"].get())
            overall = int(entries["Overall"].get())
            grade = entries["Grade"].get().strip().upper()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for numbers.")
            return
        students[name] = (number, coursework, exam, overall, grade)
        save_to_file()
        check_highest_lowest(name)
        entry['values'] = list(students.keys())
        show_all_students()
        add_win.destroy()

    tk.Button(add_win, text="Save", font=('Helvetica',10), command=save_new).grid(row=len(fields), column=0, columnspan=2, pady=10)

def delete_record():
    target = selected_student.get()
    if not target:
        messagebox.showerror("Error", "Please select a student to delete.")
        return
    if target in students:
        del students[target]
        save_to_file()
        entry['values'] = list(students.keys())
        show_all_students()
        messagebox.showinfo("Deleted", f"{target} deleted successfully.")

# ----------------------- BUTTON LAYOUT -----------------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

buttons = [
    ("View All", show_all_students),
    ("Highest Score", show_highest),
    ("Lowest Score", show_lowest),
    ("View Record", view_record),
    ("Add Record", add_record),
    ("Delete Record", delete_record),
    ("Exit", root.destroy)
]

for i, (text, cmd) in enumerate(buttons):
    tk.Button(btn_frame, text=text, width=14, height=2, font=('Helvetica',10), command=cmd).grid(row=i//3, column=i%3, padx=10, pady=5)

# ----------------------- RUN -----------------------
show_all_students()
root.mainloop()
