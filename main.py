import tkinter
from tkinter import DISABLED, NORMAL
import random

timer = None

# functions
def show_text():
    try:
        with open("dictionary.txt") as file:
            choosen_words = random.choices(file.read().splitlines(), k=30)
            list_of_words = ' '.join([l.rstrip() for l in choosen_words])
        all_words.config(state=NORMAL)
        all_words.delete("1.0", tkinter.END)
        all_words.insert(tkinter.END, list_of_words)
        all_words.grid(row=3, column=1, columnspan=3)
        all_words.config(state=DISABLED)
        answer_box.grid(row=4, column=1, columnspan=3)
        score_label.grid_forget()
        try:
            answer_box.delete(0, tkinter.END)
        except tkinter.TclError:
            pass
    except tkinter.TclError:
        show_text()


def time_count(count):

    global timer
    try:
        screen.after_cancel(timer)
    except ValueError:
        pass
    if count > 0:
        timer = screen.after(1000, time_count, count - 1)
    elif count == 0:
        show_score()
    time_label.config(text=f"Time left: {count}s")

def show_score():
    score = 0
    all_words.grid_forget()
    answer_box.grid_forget()
    oryginal = all_words.get("1.0", tkinter.END).replace(" ", "_")
    answer = answer_box.get().replace(" ", "_")
    for letter in answer:
        if letter == oryginal[answer.index(letter)]:
            score += 1
    score_label.config(text=f"Your score is: {score} chars per minute.")
    score_label.grid(row=1, column=1, columnspan=2)
    if high_score() < score:
        with open("highscore.txt", "w") as file:
            file.write(str(score))
    high_score_label.config(text=f"High score: {high_score()}")




def check_answer(sv):
    try:
        oryginal = all_words.get("1.0", tkinter.END).replace(" ", "_")
        answer = sv.get().replace(" ", "_")
        all_words.tag_remove("red", "1.0", tkinter.END)
        all_words.tag_remove("green", "1.0", tkinter.END)
        for i, letter in enumerate(answer):
            if letter == oryginal[i]:
                all_words.tag_add("green", f"1.{i}")
            else:
                all_words.tag_add("red", f"1.{i}")
    except NameError:
        pass

def high_score():
    try:
        with open("highscore.txt", "r") as file:
                return int(file.read())
    except ValueError:
        return 0



# layout
screen = tkinter.Tk()
screen.config(width=150, height=50, padx=5, pady=5)
screen.title("Typing Speed checker")

time_label = tkinter.Label()
time_label.config(text=f"Time left: 60s")
time_label.grid(row=0, column=2)

start_button = tkinter.Button()
start_button.config(text="Start", width=20, command=lambda: [show_text(), time_count(10)])
start_button.grid(row=2, column=2, columnspan=2)

all_words = tkinter.Text()
all_words.config(width=75, height=5)
all_words.tag_configure("green", foreground="green")
all_words.tag_configure("red", foreground="red")

score_label = tkinter.Label()
score_label.config(font=("Courier", 25, "bold"))

high_score_label = tkinter.Label()
high_score_label.config(text=f"High score: {high_score()}")
high_score_label.grid(row=0, column=1)

sv = tkinter.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: check_answer(sv))

answer_box = tkinter.Entry(textvariable=sv)
answer_box.config(width=100)


screen.mainloop()
