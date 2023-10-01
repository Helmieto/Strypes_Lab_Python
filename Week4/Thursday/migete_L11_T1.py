from tkinter import *
from tkinter import ttk
import math

#TBA float point


root = Tk()
root.geometry("350x250")
root.title("Calculator")

text = Text(root, height=1, width = 20)
text.grid(row=0, column=0, columnspan =2)

res = Text(root, height=1, width = 20)
res.grid(row=0, column=2, columnspan =2)

number1  = 0
number2 = 0
result = 0
operation = ""
memory = 0

def update_input_screen(*args):
    text.delete(1.0, END)
    for str in args:
        text.insert(END, str)
def update_output_screen(arg):
    res.delete(1.0, END)
    res.insert(END, arg)

#function
def click(but):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    operations = ['+', '-', 'x', '÷', '!', '√', '=']
    memory_ops = ['m+', 'm-', 'mr', 'mc']
    global number1
    global number2
    global result
    global operation
    global memory
    global text
    global res


    #if input is number
    if but in numbers:

        if operation == "":
            number1 = number1*10 +(ord(but) - ord('0'))
            update_input_screen(f"{number1}")

        else:
            if operation != '!' and operation != '√':
                number2 = number2 * 10 + (ord(but) - ord('0'))
                update_input_screen(f"{number1}",operation, f"{number2}")
            else:
                if operation == '!':
                        result = math.factorial(number1)
                        number1 = result
                        update_output_screen(f"{result}")
                        operation = ''

                elif operation == '√':
                    if number1 >= 0:
                            result = math.sqrt(number1)
                            number1=result
                            update_output_screen(f"{result}")
                            operation = ''

                    else:
                        update_output_screen("You can't use square root on negative numbers")


    if but in operations:

        if operation == '':

            if but == '!':
                operation = '!'
                update_input_screen(f"{number1}", operation)

            elif but == '√':
                    operation = '√'
                    update_input_screen(f"{number1}", operation)

            else:
                if but != '=':
                    operation = but
                    update_input_screen(f"{number1}", operation)

        else:
            if number2 != 0:
                if operation == '+':
                    result = number1 + number2

                    if but == '=':
                        number1 = result
                        number2 = 0
                        operation = ''
                        update_output_screen(f"{result}")

                    else:
                        number1 = result
                        number2 = 0
                        operation = but
                        update_input_screen(f"{number1}", operation)
                        update_output_screen("")
                elif operation == '-':
                    result= number1 - number2
                    if but == '=':
                        number1 = result
                        number2 = 0
                        operation = ''
                        update_output_screen(f"{result}")

                    else:
                        number1 = result
                        number2 = 0
                        operation = but
                        update_input_screen(f"{number1}", operation)
                        update_output_screen("")
                elif operation == 'x':
                    result = number1 * number2
                    if but == '=':
                        number1 = result
                        number2 = 0
                        operation = ''
                        update_output_screen(f"{result}")

                    else:
                        number1 = result
                        number2 = 0
                        operation = but
                        update_input_screen(f"{number1}", operation)
                        update_output_screen("")
                elif operation == '÷':
                    if number2 != 0:
                        result = number1 / number2
                        if but == '=':
                            number1 = result
                            number2 = 0
                            operation = ''
                            update_output_screen(f"{result}")

                        else:
                            number1 = result
                            number2 = 0
                            operation = but
                            update_input_screen(f"{number1}", operation)
                            update_output_screen("")


            else:
                if operation == '!':
                    if but == '=':
                        result = math.factorial(number1)
                        number1 = result
                        update_output_screen(f"{result}")
                        operation = ''

                elif operation == '√':
                    if number1 >= 0:
                        if but == '=':
                            result = math.sqrt(number1)
                            number1=result
                            update_output_screen(f"{result}")
                            operation = ''

                    else:
                        update_output_screen("You can't use square root on negative numbers")
                if operation == '÷':
                    if but == '=':
                        update_output_screen("You can't devide by 0!")
                if but != '=':
                    operation = but
                    update_input_screen(f"{number1}", operation)

    if but == "AC":
        number1 = 0
        number2 = 0
        result = 0
        operation = ''
        update_input_screen("")
        update_output_screen("")

    if but == "CE":
        if number2 != 0:
            number2 = 0
            update_input_screen(f"{number1}", operation)
            update_output_screen("")
        else:
            number1 = 0
            operation = ''
            update_input_screen("")
            update_output_screen("")

    if but == "+/-":
        if operation == '':
            number1 *= -1
            update_input_screen(f"{number1}")
        else:
            number2 *= -1
            update_input_screen(f"{number1}", operation, f"{number2}")

    if but in memory_ops:
        if but == "m+":
            if number2 != 0:
                memory += number2
            else:
                memory += number1

        elif but == "m-":
            if number2 != 0:
                memory -= number2
            else:
                memory -= number1

        elif but == "mr":
            if operation == '':
                number1   = memory
                update_input_screen(f"{number1}")
            else:
                number2 = memory
                update_input_screen(f"{number1}", operation, f"{number2}")
        else:
            memory = 0



buttons = []

button = ttk.Button(root, text="0",comman=lambda m = "0":click(m))
button.grid(row=6, column=1)
buttons.append(button)
for i in range(1,10):
    button = ttk.Button(root, text=f"{i}",comman=lambda m = f"{i}":click(m))
    button.grid(row=((i-1)//3)+3, column=(i-1)%3)
    buttons.append(button)

#clear buttons
ac_button = ttk.Button(root, text="AC",comman=lambda m = "AC":click(m))
ac_button.grid(row=6, column=0)
ce_button = ttk.Button(root, text="CE",comman=lambda m = "CE":click(m))
ce_button.grid(row=6, column=2)

#operations butoons
plus_button = ttk.Button(root, text="+",comman=lambda m = "+":click(m))
plus_button.grid(row=2, column=3)

minus_button = ttk.Button(root, text="-",comman=lambda m ="-":click(m))
minus_button.grid(row=3, column=3)

multi_button = ttk.Button(root, text="x",comman=lambda m = "x":click(m))
multi_button.grid(row=4, column=3)

div_button = ttk.Button(root, text="÷",comman=lambda m = "÷":click(m))
div_button.grid(row=5, column=3)

fact_button = ttk.Button(root, text="!",comman=lambda m = "!":click(m))
fact_button.grid(row=2, column=0)

root_button = ttk.Button(root, text="√",comman=lambda m = "√":click(m))
root_button.grid(row=2, column=1)

negate_button = ttk.Button(root, text="+/-",comman=lambda m = "+/-":click(m))
negate_button.grid(row=2, column=2)

solve_button = ttk.Button(root, text="=",comman=lambda m = "=":click(m))
solve_button.grid(row=6, column=3)


#memory buttons (1st row)
memoryadd_button = ttk.Button(root, text="m+", comman=lambda m = "m+":click(m))
memoryadd_button.grid(row=1, column=0)

memorysubstr_button = ttk.Button(root, text="m-", comman=lambda m = "m-":click(m))
memorysubstr_button.grid(row=1, column=1)

memoryrecall_button = ttk.Button(root, text="mr", comman=lambda m = "mr":click(m))
memoryrecall_button.grid(row=1, column=2)

memoryclear_button = ttk.Button(root, text="mc", comman=lambda m = "mc":click(m))
memoryclear_button.grid(row=1, column=3)


root.mainloop()