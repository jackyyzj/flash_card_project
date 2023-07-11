import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
data_dict = {}

try:
	data = pd.read_csv("data/new_data.csv")
except FileNotFoundError:
	original_data = pd.read_csv("data/french_words.csv")
	data_dict = original_data.to_dict(orient="records")
else:
	data_dict = data.to_dict(orient="records")


def switch_word():
	global current_card, flip_timer
	window.after_cancel(flip_timer)
	current_card = random.choice(data_dict)
	canvas.itemconfig(card_title, text="French", fill="black")
	canvas.itemconfig(card_word, text=current_card["French"], fill="black")
	canvas.itemconfig(card_background, image=card_font_img)
	flip_timer = window.after(3000, func=flip_card)


def flip_card():
	canvas.itemconfig(card_title, text="English", fill = "white")
	canvas.itemconfig(card_word, text=current_card["English"], fill="white")
	canvas.itemconfig(card_background, image=card_back_img)


def is_known():
	data_dict.remove(current_card)
	new_data = pd.DataFrame(data_dict)
	new_data.to_csv("data/new_data.csv", index=False)
	switch_word()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_font_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_font_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=switch_word)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

switch_word()

window.mainloop()
