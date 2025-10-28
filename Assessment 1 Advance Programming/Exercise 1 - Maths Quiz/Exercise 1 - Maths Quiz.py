import tkinter as tk
import random

# ------------------- GUI SETUP -------------------
root = tk.Tk()
root.title("Math Quiz")
root.geometry("600x600")
root.resizable(0, 0)

frame = tk.Frame(root, bg="lightblue", width=550, height=550)
frame.place(relx=0.5, rely=0.5, anchor="center")
frame.pack_propagate(False)

# ------------------- FUNCTIONAL LOGIC -------------------
def randomInt(level):
    """Generate two random numbers based on difficulty"""
    if level == "Easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "Moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:  # Advance
        return random.randint(100, 999), random.randint(100, 999)

def decideOperation():
    """Randomly choose + or -"""
    return random.choice(['+', '-'])

def isCorrect(userAnswer, num1, num2, operation):
    """Check if user's answer is correct"""
    correctAnswer = num1 + num2 if operation == '+' else num1 - num2
    return userAnswer == correctAnswer

def displayResults(score):
    """Determine grade and show final results"""
    if score >= 90: grade = "A+"
    elif score >= 80: grade = "A"
    elif score >= 70: grade = "B"
    elif score >= 60: grade = "C"
    elif score >= 50: grade = "D"
    else: grade = "F"
    return f"Final Score: {score}/100\nGrade: {grade}"

# ------------------- QUIZ CLASS -------------------
class MathQuiz:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.q_count = 0
        self.attempts = 0
        self.answer = None
        self.build_quiz_ui()
        self.next_question()

    def generate_question(self):
        num1, num2 = randomInt(self.difficulty)
        op = decideOperation()
        if op == "-":
            if num2 > num1: num1, num2 = num2, num1
            self.answer = num1 - num2
        else:
            self.answer = num1 + num2
        return f"{num1} {op} {num2} = "

    def build_quiz_ui(self):
        for widget in frame.winfo_children():
            widget.destroy()
        cancel_btn = tk.Button(frame, text="✖", font=("Helvetica",14,"bold"), fg="red",
                               command=show_menu, bd=0, bg="lightblue", activebackground="lightblue")
        cancel_btn.place(x=510, y=10)
        self.q_label = tk.Label(frame, text="", font=("Helvetica",22,"bold"), bg="lightblue")
        self.q_label.pack(pady=30)
        self.entry = tk.Entry(frame, font=("Helvetica",18), justify="center")
        self.entry.pack(pady=10)
        self.submit_btn = tk.Button(frame, text="Submit", font=("Helvetica",16), command=self.check_answer)
        self.submit_btn.pack(pady=15)
        self.feedback = tk.Label(frame, text="", font=("Helvetica",16), bg="lightblue")
        self.feedback.pack(pady=10)
        self.score_label = tk.Label(frame, text=f"Score: 0", font=("Helvetica",16), bg="lightblue")
        self.score_label.pack(pady=10)

    def next_question(self):
        if self.q_count == 10:
            self.show_results()
            return
        self.q_count += 1
        self.attempts = 0
        question = self.generate_question()
        self.q_label.config(text=f"Q{self.q_count}: {question}")
        self.entry.delete(0, tk.END)
        self.feedback.config(text="")

    def check_answer(self):
        resp = self.entry.get().strip()
        if not resp.isdigit() and not (resp.startswith("-") and resp[1:].isdigit()):
            self.feedback.config(text="Enter a valid integer!", fg="red")
            return
        user_answer = int(resp)
        if isCorrect(user_answer, *map(int, self.q_label.cget("text").split()[1:4:2]), self.q_label.cget("text").split()[2]):
            if self.attempts == 0:
                self.score += 10
                self.feedback.config(text="Correct! (+10)", fg="green")
            else:
                self.score += 5
                self.feedback.config(text="Correct! (+5)", fg="green")
            self.score_label.config(text=f"Score: {self.score}")
            root.after(1000, self.next_question)
        else:
            self.attempts += 1
            if self.attempts < 2:
                self.feedback.config(text="Incorrect — try again!", fg="orange")
                self.entry.delete(0, tk.END)
            else:
                self.feedback.config(text=f"Wrong! Correct was {self.answer}", fg="red")
                root.after(1500, self.next_question)

    def show_results(self):
        for widget in frame.winfo_children():
            widget.destroy()
        result_text = displayResults(self.score)
        tk.Label(frame, text=result_text, font=("Helvetica",24,"bold"), bg="lightblue").pack(pady=40)
        tk.Button(frame, text="Play Again", font=("Helvetica",18), command=show_menu).pack(pady=20)
        tk.Button(frame, text="Exit", font=("Helvetica",18), command=root.quit).pack(pady=10)

# ------------------- MENU -------------------
def show_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text="Welcome to the Math Quiz!\nSelect a difficulty level to begin:",
             font=("Helvetica",22,"bold"), bg="lightblue", justify="center").pack(pady=40)
    tk.Button(frame, text="Easy", font=("Helvetica",18), width=20, height=2, command=lambda: MathQuiz("Easy")).pack(pady=10)
    tk.Button(frame, text="Moderate", font=("Helvetica",18), width=20, height=2, command=lambda: MathQuiz("Moderate")).pack(pady=10)
    tk.Button(frame, text="Advance", font=("Helvetica",18), width=20, height=2, command=lambda: MathQuiz("Advance")).pack(pady=10)

show_menu()
root.mainloop()
