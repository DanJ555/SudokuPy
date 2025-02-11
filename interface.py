from tkinter import *


def show_window_size():
    width = root.winfo_width()
    height = root.winfo_height()
    print(f"Window size: {width}x{height}")

def restart_puzzle():
    pass


def place_holder():
    print("click")


def move_focus(event, next_widget_index):
    if event.char.isdigit():
        inputs[next_widget_index].focus_set()


root = Tk()
root.title("PySudoku")
root.geometry("271x500")
root.resizable(width=False, height=True)

menu_bar = Menu(root)

sudoku_menu = Menu(menu_bar, tearoff=0)
sudoku_menu.add_command(label="New", command=place_holder)
sudoku_menu.add_separator()
sudoku_menu.add_command(label="Exit", command=place_holder)

menu_bar.add_cascade(label="Options", menu=sudoku_menu, font=("Arial", 10))

root.config(menu=menu_bar)

label = Label(root, text="Enter numbers into grid:")
label.grid()

grid = Frame(root)
grid.grid()
inputs = [Entry(grid, width=3, justify="center") for _ in range(81)]
row_index = -1
for i, txt in enumerate(inputs):
    column_index = i % 9
    if column_index == 0:
        row_index += 1
    txt.grid(row=row_index, column=column_index)

def submit_values():
    print([txt.get() for txt in inputs])


button = Button(root, text="Display Window Size", command=show_window_size)
button.grid()
button_2 = Button(root, text="submit values", command=submit_values)
button_2.grid()
'''
txt = Entry(root, width=3)
txt.grid(row=1, column=0)
txt_2 = Entry(root, width=3)
txt_2.grid(row=1, column=1)
'''

root.mainloop()
