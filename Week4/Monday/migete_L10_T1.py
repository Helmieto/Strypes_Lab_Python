from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("150x150")
root.title("BMI calculator")


#frame.config(bg="red")

def calculate_bmi():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        bmi = weight / (height ** 2)
        result_label.config(text=f"BMI: {bmi:.2f}")
        error_label.config(text="")
    except ValueError:
        error_label.config(text="Error! Please enter valid height and weight values.")


height_label = ttk.Label(root, text="height(m) =", foreground="black")
height_label.pack()



height_entry = ttk.Entry(root)
height_entry.pack()

weight_label = ttk.Label(root, text="weight(kg) =", foreground="black")
weight_label.pack()

weight_entry = ttk.Entry(root)
weight_entry.pack()

calculate_button = ttk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.pack()


result_label = ttk.Label(root, text="")
result_label.pack()
result_label.config(text=f"BMI:")

error_label = ttk.Label(root, text="")
error_label.pack()

root.mainloop()