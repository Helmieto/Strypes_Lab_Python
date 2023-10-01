from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
import os


class Image_viewer:

    def __init__(self, frame):
        self.times_saved = 0
        self.name = ""
        self.extension = ""
        self.main_frame = frame

        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack()

        self.image_frame = Frame(self.main_frame)
        self.image_frame.pack(expand=True)

        self.name_label = Label(self.button_frame, text="")
        self.name_label.grid(row=0, column=0)

        self.size_label = Label(self.button_frame, text="")
        self.size_label.grid(row=1, column=0)

        self.color_label = Label(self.button_frame, text="")
        self.color_label.grid(row=2, column=0)

        self.image_label =  Label(self.image_frame)
        self.image_label.grid(row=0, column=0)

        self.show_btn = Button(self.button_frame, text="Show", width=20, command=self.load_image)
        self.show_btn.grid(row=3, column=0)

        self.rotate_clockwise = Button(self.button_frame, text="Rotate clockwise", width=20, command=lambda dir="clockwise" :self.rotate_image(dir))
        self.rotate_clockwise.grid(row=4, column=0)

        self.rotate_counterclockwise = Button(self.button_frame, text="Rotate counterclockwise", width=20, command=lambda dir="counter" :self.rotate_image(dir))
        self.rotate_counterclockwise.grid(row=5, column=0)

        self.hmirror_btn = Button(self.button_frame, text="Mirror horizontally", width=20, command=self.mirror_horizontally)
        self.hmirror_btn.grid(row=6, column=0)

        self.vmirror_btn = Button(self.button_frame, text="Mirror vertically", width=20, command=self.mirror_vertically)
        self.vmirror_btn.grid(row=7, column=0)

        self.blur_btn = Button(self.button_frame, text="Apply blur", width=20, command=self.apply_blur)
        self.blur_btn.grid(row=8, column=0)

        self.shrink_btn = Button(self.button_frame, text="Shrink", width=20, command=self.shrink_image)
        self.shrink_btn.grid(row=9,column=0)

        self.expand_btn = Button(self.button_frame, text="Expand", width=20, command=self.expand_image)
        self.expand_btn.grid(row=10, column=0)

        self.median_btn = Button(self.button_frame, text="Apply median filter", width=20, command=self.apply_median)
        self.median_btn.grid(row=11, column=0)

        self. save_btn = Button(self.button_frame, text="Save", width=20, command=self.save_image)
        self.save_btn.grid(row=12, column=0)



    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.jfif;*.bmp;*.gif;")])

        if path:
            self.show_image(path)


    def update_image_info(self):
        size = f"Size:{self.curr.width}x{self.curr.height}"
        self.size_label.config(text=size)
        colorsys = f"Mode:{self.curr.mode}"
        self.color_label.config(text=colorsys)


    def show_image(self, path):
        self.curr = Image.open(path)
        self.curr.thumbnail((2000, 2000))
        self.displayed = ImageTk.PhotoImage(self.curr)
        self.image_label.config(image=self.displayed)

        base_name = os.path.basename(path)
        self.name,  self.extension = os.path.splitext(base_name)

        text_to_display = f"Name:{self.name}  Type:{self.extension}"
        self.name_label.config(text = f"{text_to_display}")
        self.update_image_info()


    def rotate_image(self,direction):
        if self.curr:
            angle = 0
            if direction == "clockwise":
                rotated = self.curr.transpose(Image.ROTATE_270)
            else:
                rotated = self.curr.transpose(Image.ROTATE_90)


            rotated_tk = ImageTk.PhotoImage(rotated)
            self.image_label.config(image=rotated_tk)
            self.image_label.image = rotated_tk
            self.curr = rotated
            self.displayed = rotated_tk
            #self.show_image()
            self.update_image_info()


    def mirror_horizontally(self):
        mirrored = self.curr.transpose(Image.FLIP_LEFT_RIGHT)
        mirrored_tk = ImageTk.PhotoImage(mirrored)
        self.image_label.config(image=mirrored_tk)
        self.image_label.image=mirrored_tk
        self.curr = mirrored
        self.displayed = mirrored_tk
        self.update_image_info()


    def mirror_vertically(self):
        mirrored = self.curr.transpose(Image.FLIP_TOP_BOTTOM)
        mirrored_tk = ImageTk.PhotoImage(mirrored)
        self.image_label.config(image=mirrored_tk)
        self.image_label.image = mirrored_tk
        self.curr = mirrored
        self.displayed = mirrored_tk
        self.update_image_info()


    def apply_blur(self):
        blurred = self.curr.filter(ImageFilter.BLUR)
        blurred_tk = ImageTk.PhotoImage(blurred)
        self.image_label.config(image=blurred_tk)
        self.image_label.image=blurred_tk
        self.curr = blurred
        self.displayed= blurred_tk
        self.update_image_info()


    def shrink_image(self):
        smaller_width = self.curr.width // 2
        smaller_height = self.curr.height // 2
        resized = self.curr.resize((smaller_width, smaller_height))
        resized_tk = ImageTk.PhotoImage(resized)

        self.image_label.config(image=resized_tk)
        self.image_label.image=resized_tk

        self.curr = resized
        self.displayed = resized_tk
        self.update_image_info()

    def expand_image(self):
        bigger_width = self.curr.width * 2
        bigger_height = self.curr.height * 2
        resized = self.curr.resize((bigger_width, bigger_height))
        resized_tk = ImageTk.PhotoImage(resized)

        self.image_label.config(image=resized_tk)
        self.image_label.image = resized_tk

        self.curr = resized
        self.displayed = resized_tk
        self.update_image_info()


    def apply_median(self):
        edited = self.curr.filter(ImageFilter.MedianFilter)
        edited_tk = ImageTk.PhotoImage(edited)

        self.image_label.config(image=edited_tk)
        self.image_label.image=edited_tk

        self.curr = edited
        self.displayed = edited_tk
        self.update_image_info()


    def save_image(self):
        self.times_saved += 1
        new_name = f"{self.name}{self.times_saved}{self.extension}"
        self.curr.save(new_name)



root = Tk()
root.title("Image viewer")
root.geometry("1200x1200")

main_frame = Frame(root)
main_frame.pack()

Image_viewer(main_frame)

root.mainloop()