# Exercise 2: Alexa Tell Me a Joke (GUI + Functional Logic)

import tkinter as tk
import random
import os

# ----------------------- CONFIG -----------------------
JOKES_FILE = "C:/Users/peter/.vscode/Activity/Assessment 1 Advance Programming/Exercise 2 - Alexa tell me a Joke/randomJokes.txt.txt"  # Full path

# ----------------------- GUI SETUP -----------------------
root = tk.Tk()
root.title("Alexa Tell Me A Joke")
root.geometry("600x600")
root.resizable(0, 0)

frame = tk.Frame(root, bg="lightgreen", width=550, height=550)
frame.pack_propagate(False)
frame.pack(expand=True)

# ----------------------- FUNCTIONAL LOGIC -----------------------
def load_jokes(filename=JOKES_FILE):
    """Load jokes from a text file. Each line must contain '?' separating setup and punchline."""
    if not os.path.isfile(filename):
        return ["File not found?Make sure the joke file exists."]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if '?' in line]
    except Exception as e:
        return [f"Error reading file: {e}"]

def get_random_joke(jokes_list):
    """Return a random joke and remove it from the list to avoid repeats."""
    joke = random.choice(jokes_list)
    jokes_list.remove(joke)
    setup, punchline = joke.split('?', 1)
    return setup + '?', punchline

def emoji_reaction():
    """Display a random emoji (console fallback)."""
    emojis = ['😄', '😂', '🤣', '😆', '😎', '😜', '🤪', '😁']
    print(random.choice(emojis))

def surprise_mode(unused_jokes, jokes):
    """Select 3 jokes in a row."""
    for _ in range(3):
        if not unused_jokes:
            unused_jokes = jokes.copy()
        setup, punchline = get_random_joke(unused_jokes)
        print("\n" + setup)
        input("Press Enter for the punchline...")
        print(punchline)
        emoji_reaction()
    return unused_jokes

# ----------------------- GUI HELPERS -----------------------
def clear_frame():
    for w in frame.winfo_children():
        w.destroy()

def make_label(text, size, y, bold=False, color="black"):
    style = ("Helvetica", size, "bold") if bold else ("Helvetica", size)
    tk.Label(frame, text=text, font=style, fg=color, bg="lightgreen",
             wraplength=500, justify="center").place(relx=0.5, rely=y, anchor="center")

def show_joke():
    """Display a single joke in GUI."""
    clear_frame()
    global unused_jokes, jokes
    if not jokes:
        jokes = load_jokes()
    if not unused_jokes:
        unused_jokes = jokes.copy()

    setup, punchline = get_random_joke(unused_jokes)

    make_label(f"Alexa: {setup}", 18, 0.35)

    ans_label = tk.Label(frame, text="", font=("Helvetica", 25, "bold"), fg="green", bg="lightgreen", wraplength=500, justify="center")
    ans_label.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(frame, text="Show Answer", font=("Helvetica", 16, "bold"), bg="green", fg="white",
              command=lambda: ans_label.config(text=punchline)).place(relx=0.5, rely=0.65, anchor="center")

    tk.Button(frame, text="Tell me another Joke", font=("Helvetica", 16, "bold"), bg="green", fg="white",
              command=show_joke).place(relx=0.5, rely=0.75, anchor="center")

# ----------------------- GUI MENU -----------------------
def show_menu():
    clear_frame()
    make_label("Welcome to Alexa's Joke Site!", 22, 0.3, bold=True)
    make_label("Click the button below to hear a joke!", 14, 0.45)
    tk.Button(frame, text="Tell me a Joke", font=("Helvetica", 18, "bold"), bg="green", fg="white",
              command=show_joke).place(relx=0.5, rely=0.6, anchor="center")

# ----------------------- GLOBAL VARIABLES -----------------------
jokes = load_jokes()
unused_jokes = jokes.copy() if jokes else []

# ----------------------- RUN -----------------------
show_menu()
root.mainloop()
