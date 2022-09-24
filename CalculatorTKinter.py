import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tft
from math import sqrt


memoryValue = 0.
memoryOperator = ""
window = tk.Tk()
calc_input = tk.StringVar()
memo_input = tk.StringVar()


def button_pressed(button):
    global memoryValue
    global memoryOperator
    global calc_input

    if (button >= "0" and button <= "9"):
        calc_input.set(calc_input.get() + button)

    elif (button == "."):
        if (validate(calc_input.get() + ".")):
            calc_input.set(calc_input.get() + button)

    elif (button == "←"):
        calc_input.set(calc_input.get()[:-1])

    elif (button == "C"):
        calc_input.set("")
        memoryValue = 0.
        memoryOperator = ""

    elif (button in ["+", "-", "*", "/"]):
        if (memoryOperator in ["+", "-", "*", "/"]):
            button_pressed("=")
        memoryOperator = button
        memoryValue = value(calc_input.get())
        calc_input.set("")

    elif (button == "="):
        # it's necessary to store last user action and repeat on request, thus op2 was written
        if (memoryOperator == "+"):
            temp = value(calc_input.get())
            calc_input.set(string(float(memoryValue) + temp))
            memoryValue = temp
            memoryOperator = "+2"
        elif (memoryOperator == "-"):
            temp = value(calc_input.get())
            calc_input.set(string(float(memoryValue) - temp))
            memoryValue = temp
            memoryOperator = "-2"
        elif (memoryOperator == "*"):
            temp = value(calc_input.get())
            calc_input.set(string(float(memoryValue) * temp))
            memoryValue = temp
            memoryOperator = "*2"
        elif (memoryOperator == "/"):
            temp = value(calc_input.get())
            if (temp == 0):
                memo_input.set("Division by 0!")
                return
            calc_input.set(string(float(memoryValue) / temp))
            memoryValue = temp
            memoryOperator = "/2"
        elif (memoryOperator == "+2"):
            calc_input.set(string(value(calc_input.get()) + float(memoryValue)))
        elif (memoryOperator == "-2"):
            calc_input.set(string(value(calc_input.get()) - float(memoryValue)))
        elif (memoryOperator == "*2"):
            calc_input.set(string(value(calc_input.get()) * float(memoryValue)))
        elif (memoryOperator == "/2"):
            calc_input.set(string(value(calc_input.get()) / float(memoryValue)))

    elif (button == "√"):
        temp = value(calc_input.get())
        if (temp < 0):
            memo_input.set("Square of a negative error!")
            return
        calc_input.set(string(sqrt(value(calc_input.get()))))

    elif (button == "⅟"):
        temp = value(calc_input.get())
        if (temp == 0):
            memo_input.set("Division by 0!")
            return
        calc_input.set(string(1 / temp))

    elif (button == "±"):
        calc_input.set(string(-value(calc_input.get())))

    else:
        print("Unknown button:", button)
    memo_input.set(string(memoryValue))
    input_entry.focus()
    input_entry.icursor(len(calc_input.get()))


def value(x):
    # convert string to float with additional cases
    if (x in ["", "-"]):
        return 0
    return float(x)


def string(x):
    # convert float to string without trailing zeros
    return "%g"%(float(x))


def validate(input):
    try:
        value(input)
    except ValueError:
        return False
    return True


sw = float(window.winfo_screenwidth())
fonts = [tft.Font(family='Helvetica', size=int(sw * 18 / 1366)), tft.Font(family='Helvetica', size=int((sw * 12 / 1366)))]

window.title("Calculator")
window.resizable(width = False, height = False)

main_frame = ttk.Frame(window)
main_frame.grid(sticky = "nsew")

vcmd = main_frame.register(validate)
input_entry = ttk.Entry(main_frame, textvariable=calc_input, validate="key", validatecommand=(vcmd, '%P'), justify="right", font=fonts[0])
input_entry.grid(row=0, column=0, columnspan=5, sticky = "nsew")

# memo_entry's purpose to show memoryValue to user (might be useful in case of sequencial operations without pressing '=' button)
memo_entry = ttk.Entry(main_frame, textvariable=memo_input, state="disabled", justify="right", font=fonts[1])
memo_entry.grid(row=1, column=0, columnspan=5, sticky = "nsew")

buttons = ["← C√ ", "789/ ", "456*⅟", "123-±", " 0.+="]
button_style = ttk.Style()
button_style.configure("button.TButton", font=fonts[1])
for i in range(0, 5):
    for j in range(0, 5):
        ttk.Button(main_frame, style="button.TButton", width=5, text=buttons[i][j], command=lambda x=buttons[i][j]: button_pressed(x)).grid(row=i+2, column=j)

input_entry.focus()
window.mainloop()
