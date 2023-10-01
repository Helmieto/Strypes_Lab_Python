from tkinter import *
from tkinter import ttk
import random


hangman_visuals = [
    """
     ------
     |    
     |    
     |   
    -|-
    """,
    """
     ------
     |    O
     |    
     |  
    -|-
    """,
    """
     ------
     |    O
     |    |
     |   
    -|-
    """,
    """
     ------
     |    O
     |   /|
     |  
    -|-
    """,
    """
     ------
     |    O
     |   /|\
     |  
    -|-
    """,
    """
     ------
     |    O
     |   /|\
     |   /   
    -|-
    """,
    """
     ------
     |    O
     |   /|\
     |   / \
    -|-
    """
]


def choose_word():
    #BE CAREFUL, FILE MIGHT BE MISSING :D
    #file = open("words.txt", 'r')
   # all_words = file.readlines()
    #file.close()
    word_list = [
        "chocolate", "elephant", "flamingo", "internet", "kangaroo",
        "mountain", "notebook", "watermelon", "xylophone", "zeppelin",
        "butterfly", "caterpillar", "dinosaur", "gorilla", "hedgehog",
        "iguana", "jellyfish", "kangaroo", "mongoose", "narwhal",
        "opossum", "peacock", "quetzal", "rhinoceros", "squirrel",
        "tortoise", "archery", "basketball", "cricket", "equestrian",
        "football", "motorsport", "netball", "olympics", "polo",
        "quidditch", "volleyball", "wrestling", "yachting"
    ]
    chosen_word = random.choice(word_list).strip()
    return chosen_word

#only in the beginning
def update_hidden_word(key, buttons):
    global letters_guessed
    letters_count = len(key)

    first_letter = key[0]
    last_letter = key[-1]

    first_letter_index = ord(first_letter) - ord('a')
    last_letter_index = ord(last_letter) - ord('a')

    buttons[first_letter_index].config(state="disabled")
    buttons[last_letter_index].config(state="disabled")

    hidden_word = "_ " * letters_count

    hidden_word_list = list(hidden_word)

    for index, letter in enumerate(key):
        if letter == first_letter:
            hidden_word_list[index * 2] = first_letter
            letters_guessed += 1
        if letter == last_letter:
            hidden_word_list[index * 2] = last_letter
            letters_guessed += 1

    hidden_word = ''.join(hidden_word_list)
    return hidden_word


def init_word_label(word_frame):
    global hidden_word
    word_label = ttk.Label(word_frame, text=hidden_word, font=2)
    word_label.pack(anchor="center")
    return word_label


def ubdate_word_label_text(word_label, new_text):

    word_label.config(text =new_text)


def makeButtons(letters_frame):
    buttons = []

    for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
        button = ttk.Button(letters_frame, text=letter, command=lambda l=letter: make_guess(l), state="normal")
        button.grid(row=(i // 6) , column=i % 6)
        buttons.append(button)

    return buttons


def disable_button(index):
    global buttons
    buttons[index].config(state='disabled')
    buttons[index].config(command=lambda :none)


def make_guess(letter):
    global word
    global hidden_word
    global buttons
    global lives
    global letters_guessed

    hidden_word_list = list(hidden_word)
    has_that_letter = False
    letter_index = ord(letter) - ord('a')

    for index, character in enumerate(word):
            if character == letter:
                has_that_letter = True
                hidden_word_list[index * 2] = letter
                letters_guessed += 1

#doesn't work...
    if has_that_letter is False:
        lives -=1

    hidden_word = ''.join(hidden_word_list)

    ubdate_word_label_text(word_label, hidden_word)

    disable_button(letter_index)


def display_hangman(hangman_frame):
    global lives
    global hangman_visuals

    visual = hangman_visuals[6-lives]
    hangman_label = ttk.Label(hangman_frame, text=visual, font=2)
    hangman_label.grid(row=0, column=0, rowspan=6)

#def check_game_state():
    #if(lives == 0):
        # u lost
    #if(letters_guessed == len(word)):
        # u won


lives = 6
letters_guessed = 0

root = Tk()
root.title("Hangman")

word_frame = ttk.Frame(root)
word_frame.grid(row=20, column=0)

letters_frame=ttk.Frame(root)
letters_frame.grid(row=30, column=0)

hangman_frame = ttk.Frame(root)
hangman_frame.grid(row=0,  column=0, rowspan=15, columnspan=10)

word = choose_word()
hidden_word = "_ " * len(word)
buttons = makeButtons(letters_frame)
hidden_word= update_hidden_word(word, buttons)


word_label = init_word_label(word_frame)
display_hangman(hangman_frame)
#check_game_state()


root.mainloop()