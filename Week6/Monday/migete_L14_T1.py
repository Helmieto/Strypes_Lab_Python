import tkinter.scrolledtext
from tkinter import *
from tkinter import ttk
from urllib.request import *


root = Tk()
root.title("todays news")
root.columnconfigure(1, weight=2)

main_frame = Frame(root, bg="lightgrey")
main_frame.columnconfigure(0 , weight=2)
main_frame.columnconfigure(1, weight=1)
main_frame.pack()


news_titles_frame = Frame(main_frame, bg="lightgrey", width=100, borderwidth=10)
news_titles_frame.grid(row = 0, column=0,sticky=EW)


lbel = Label(news_titles_frame, text="NEWS FEED", bg="lightgrey", fg="black")
lbel.grid(row=0, sticky=NSEW)

news_frame = Frame(main_frame, bg="lightgrey", width=300, borderwidth=20)
news_frame.grid(row = 0, column=1, columnspan=3, sticky=EW)

description = tkinter.scrolledtext.ScrolledText(news_frame, width=50, wrap="word")
description.grid(row=0)


buttons = []
news_list = {}


def button_function(input_data):
    global news_list

    description.delete(1.0, END)
    description.insert(INSERT, news_list[input_data])




def extract_data_from_webpage():
    global buttons
    global news_list

    # Webpage content
    content = urlopen("https://rss.slashdot.org/Slashdot/slashdotMain").readlines()

    #flags
    read_title = False
    read_text = False
    read_item = False
    title = ""
    text = ""


    word = ""
    for lin in content:
        line = lin.decode()
        # print(line)
        for letter in line:

            if letter == "l":
                if "&" in word:
                    if read_text == True:
                        # print(word)
                        word = word.replace("&", "")
                        text += word
                        news_list[title] = text
                        # print("text: ", text)
                        text = ""
                        title = ""
                        read_text = False
                        read_item = False
            if letter == "<":
                    if read_title == True:
                        title += word
                        temp_button = Button(news_titles_frame, text=title,
                                             command=lambda arg=title: button_function(arg), width=100)
                        buttons.append(temp_button)
                        # print("title:", title)
                        news_list[title] = ""
                        read_title = False

            word += letter

            if "item" in word:
                word = ""
                read_item = True

            if "image" in word or "textinput" in word:
                word = ""
                read_item = False

            if letter == " ":
                if read_text == True:
                    text += word
                if read_title == True:
                    title += word
                word = ""

            if letter == ">":
                if "<title>" in word and read_item == True:
                    word = ""
                    read_title = True

                if "<description>" in word and read_item == True:
                    word = ""
                    read_text = True

def display_buttons():
    global buttons
    global news_list
    for index, butn in enumerate(buttons):
        butn.grid(row=index+1)


extract_data_from_webpage()

display_buttons()

root.mainloop()