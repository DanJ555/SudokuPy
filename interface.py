from tkinter import Tk, Menu, Label, Frame, Button, Entry, END
from solver import *


class SudokuApp:

    def __init__(self) -> None:
        """Initialize the Sudoku GUI application."""

        # Initialize components
        self.root = Tk()
        self.root.title("PySudoku")
        self.root.resizable(width=False, height=False)
        self.menu_bar: Menu = None
        self.error_label: Label = None

        # Initialize solver.Sudoku object
        self.sudoku = Sudoku()
        self.puzzle: list[list[int]] = [[0] * 9 for _ in range(9)]
        self.inputs: list[list[Entry]] = [[None for _ in range(9)] for _ in range(9)]

        # Build rest of UI
        self._create_widgets()

        # Resize root
        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")
        self.error_label.config(text="")

    def _create_widgets(self) -> None:
        """Populates root with widgets."""

        # Menu widgets
        menu_bar = Menu(self.root)
        sudoku_menu = Menu(menu_bar, tearoff=0)
        sudoku_menu.add_command(label="New", command=self.restart_puzzle)
        sudoku_menu.add_separator()
        sudoku_menu.add_command(label="Exit", command=self.close)
        menu_bar.add_cascade(label="Options", menu=sudoku_menu, font=("Arial", 10))
        self.root.config(menu=menu_bar)

        # Text label
        Label(self.root, text="Enter numbers into grid:").grid()

        # Sudoku 9x9 grid
        grid_frame = Frame(self.root)
        grid_frame.grid()

        for y in range(9):
            for x in range(9):
                cell: Entry = Entry(grid_frame, width=3, justify="center")
                cell.grid(row=y, column=x)
                self.inputs[y][x] = cell

        # Solve and Reset buttons
        buttons_frame = Frame(self.root)
        buttons_frame.grid()

        self.solve_button = Button(buttons_frame, text="Solve", command=self.solve_puzzle, width=8)
        self.solve_button.grid(row=0, column=0)

        self.reset_button = Button(buttons_frame, text="Reset", command=self.restart_puzzle)
        self.reset_button.grid(row=0, column=1)

        # Error Label
        self.error_label = Label(self.root, text="Invalid character(s): Only numbers may be in the Sudoku grid.", fg="red", wraplength=260)
        self.error_label.grid()

    def solve_puzzle(self) -> None:
        """Attempts to solve the Sudoku puzzle based on user input."""
        self.error_label.config(text="")

        try:
            for y in range(9):
                for x in range(9):
                    value = self.inputs[y][x].get()
                    if value == "":
                        self.puzzle[y][x] = 0
                    else:
                        self.puzzle[y][x] = int(value)
            self.sudoku.set_grid(self.puzzle)
            if self.sudoku.solve():
                solution = self.sudoku.get_grid()
                for y in range(9):
                    for x in range(9):
                        self.inputs[y][x].delete(0, END)
                        self.inputs[y][x].insert(0, solution[y][x])
                self.solve_button.config(text="Unsolve", command=self.unsolve_puzzle)
        except ValueError:
            self.error_label.config(text="Invalid character(s): Only numbers may be in the Sudoku grid.")
        except SudokuError as e:
            self.error_label.config(text=e)

    def unsolve_puzzle(self) -> None:
        self.solve_button.config(text="Solve", command=self.solve_puzzle)

        for y in range(9):
            for x in range(9):
                self.inputs[y][x].delete(0, END)
                if self.puzzle[y][x] == 0:
                    self.inputs[y][x].insert(0, "")
                else:
                    self.inputs[y][x].insert(0, self.puzzle[y][x])

    def restart_puzzle(self) -> None:
        """Resets the Sudoku grid to an empty state"""
        self.sudoku.reset()
        self.error_label.config(text="")
        self.solve_button.config(text="Solve", command=self.solve_puzzle)

        for y in range(9):
            for x in range(9):
                self.inputs[y][x].delete(0, END)
                self.puzzle[y][x] = 0

    def close(self) -> None:
        """Close application."""
        self.root.quit()

    def mainloop(self) -> None:
        """Initiate mainloop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
