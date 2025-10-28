import tkinter as tk
from tkinter import ttk, messagebox
import os

# -------------------- CONFIG --------------------
FILE_NAME = "C:/Users/peter/.vscode/Activity/Assessment 1 Advance Programming/Exercise 3 - Student Manager/studentMarks.txt.txt"

# -------------------- FUNCTIONS --------------------
def load_students():
    students = {}
    if not os.path.isfile(FILE_NAME):
        messagebox.showerror("File Error", f"{FILE_NAME} not found.")
        return students
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # skip first line
        for line in lines:
            parts = [p.strip() for p in line.strip().split(',')]
            if len(parts) == 6:
                code, name, cw1, cw2, cw3, exam = parts
                students[name] = (code, int(cw1), int(cw2), int(cw3), int(exam))
    return students

def total_and_grade(student):
    cw_total = sum(student[1:4])
    overall = (cw_total + student[4]) / 160 * 100
    if overall >= 70: grade = 'A'
    elif overall >= 60: grade = 'B'
    elif overall >= 50: grade = 'C'
    elif overall >= 40: grade = 'D'
    else: grade = 'F'
    return cw_total, overall, grade

def display_students(names_list):
    info_text.config(state='normal')
    info_text.delete('1.0', tk.END)
    total_percent = 0
    for name in names_list:
        student = students[name]
        cw_total, overall, grade = total_and_grade(student)
        total_percent += overall
        info_text.insert(tk.END, f"Name: {name}\n")
        info_text.insert(tk.END, f"Code: {student[0]}\n")
        info_text.insert(tk.END, f"Total Coursework: {cw_total}\n")
        info_text.insert(tk.END, f"Exam: {student[4]}\n")
        info_text.insert(tk.END, f"Overall %: {overall:.2f}\n")
        info_text.insert(tk.END, f"Grade: {grade}\n\n")
    if len(names_list) == len(students):
        info_text.insert(tk.END, f"Number of Students: {len(students)}\n")
        info_text.insert(tk.END, f"Class Average: {total_percent/len(students):.2f}%\n")
    info_text.config(state='disabled')

def show_all(): display_students(list(students.keys()))
def view_record():
    name = selected_student.get()
    if not name:
        messagebox.showinfo("No selection", "Please select a student.")
        return
    display_students([name])

def show_highest():
    if students:
        name = max(students, key=lambda n: total_and_grade(students[n])[1])
        display_students([name])

def show_lowest():
    if students:
        name = min(students, key=lambda n: total_and_grade(students[n])[1])
        display_students([name])

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Student Manager")
root.geometry("650x450")
root.resizable(0,0)

# --- Title ---
tk.Label(root, text="Student Manager", font=('Helvetica',18,'bold')).pack(pady=10)

# --- Top Buttons ---
top_frame = tk.Frame(root)
top_frame.pack(pady=5)

btn_opts = {'height':2, 'bd':2, 'relief':'groove', 'font':('Helvetica',10)}
tk.Button(top_frame, text="View All Records", command=show_all, **btn_opts).grid(row=0, column=0, padx=5)
tk.Button(top_frame, text="Highest Score", command=show_highest, **btn_opts).grid(row=0, column=1, padx=5)
tk.Button(top_frame, text="Lowest Score", command=show_lowest, **btn_opts).grid(row=0, column=2, padx=5)

# --- Student Selector ---
selector_frame = tk.Frame(root)
selector_frame.pack(pady=10)

tk.Label(selector_frame, text="Select Student:", font=('Helvetica',12)).grid(row=0, column=0, padx=5)
students = load_students()
selected_student = tk.StringVar()
entry = ttk.Combobox(selector_frame, textvariable=selected_student, values=list(students.keys()), width=25, state='readonly')
entry.grid(row=0, column=1, padx=5)
tk.Button(selector_frame, text="View Selected", command=view_record, **btn_opts).grid(row=0, column=2, padx=5)

# --- Info Display ---
info_frame = tk.Frame(root, bg='lightgrey', bd=2, relief='groove')
info_frame.pack(padx=20, pady=10, fill='both', expand=True)
info_text = tk.Text(info_frame, bg='lightgrey', bd=0, font=('Helvetica',10), wrap='word')
info_text.pack(fill='both', expand=True, padx=5, pady=5)
info_text.config(state='disabled')

root.mainloop()
