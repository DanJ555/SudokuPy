from tkinter import Tk, Menu, Label, Frame, Button, Entry, END
from solver import *


class SudokuApp:

    def __init__(self) -> None:
        """Initialize the Sudoku GUI application."""

        # Initialize components
        self._root = Tk()
        self._root.title("PySudoku")
        self._root.resizable(width=False, height=False)
        self._menu_bar: Menu = None
        self._error_label: Label = None

        # Initialize solver.Sudoku object
        self._sudoku = Sudoku()
        self._puzzle: list[list[int]] = [[0] * 9 for _ in range(9)]
        self._inputs: list[list[Entry]] = [[None for _ in range(9)] for _ in range(9)]

        # Build rest of UI
        self._create_widgets()

        # Resize root
        self._root.update_idletasks()
        self._root.geometry(f"{self._root.winfo_reqwidth()}x{self._root.winfo_reqheight()}")
        self._error_label.config(text="")

    def _create_widgets(self) -> None:
        """Populates root with widgets."""

        # Menu widgets
        menu_bar = Menu(self._root)
        sudoku_menu = Menu(menu_bar, tearoff=0)
        sudoku_menu.add_command(label="New", command=self.restart_puzzle)
        sudoku_menu.add_separator()
        sudoku_menu.add_command(label="Exit", command=self.close)
        menu_bar.add_cascade(label="Options", menu=sudoku_menu, font=("Arial", 10))
        self._root.config(menu=menu_bar)

        # Text label
        Label(self._root, text="Enter numbers into grid:").grid()

        # Sudoku 9x9 grid
        grid_frame = Frame(self._root, padx=20, pady=5)
        grid_frame.grid()

        box_frames: list[list[Frame]] = [[None] * 3 for _ in range(3)]
        for y in range(3):
            for x in range(3):
                box_frames[y][x] = Frame(grid_frame, bd=1, highlightbackground="black", highlightcolor="black", highlightthickness=1)
                box_frames[y][x].grid(row=y, column=x)

        for y in range(9):
            for x in range(9):
                cell_frame = Frame(box_frames[y // 3][x // 3], highlightbackground="white",  highlightcolor="white", highlightthickness=1)
                cell_frame.grid(row=(y % 3), column=(x % 3))
                cell = Entry(cell_frame, width=3, justify="center")
                cell.grid()
                self._inputs[y][x] = cell

        # Solve and Reset buttons
        buttons_frame = Frame(self._root)
        buttons_frame.grid()

        self._solve_button = Button(buttons_frame, text="Solve", command=self.solve_puzzle, width=8)
        self._solve_button.grid(row=0, column=0)

        self._reset_button = Button(buttons_frame, text="Reset", command=self.restart_puzzle)
        self._reset_button.grid(row=0, column=1)

        # Error Label
        self._error_label = Label(self._root, text="Invalid character(s): Only numbers may be in the Sudoku grid.",
                                  fg="red", wraplength=260, pady=5)
        self._error_label.grid()

    def solve_puzzle(self) -> None:
        """Attempts to solve the Sudoku puzzle based on user input."""
        self._error_label.config(text="")

        try:
            for y in range(9):
                for x in range(9):
                    value = self._inputs[y][x].get()
                    if value == "":
                        self._puzzle[y][x] = 0
                    else:
                        self._puzzle[y][x] = int(value)
            self._sudoku.set_grid(self._puzzle)
            if self._sudoku.solve():
                solution = self._sudoku.get_grid()
                for y in range(9):
                    for x in range(9):
                        self._inputs[y][x].delete(0, END)
                        self._inputs[y][x].insert(0, solution[y][x])
                self._solve_button.config(text="Unsolve", command=self.unsolve_puzzle)
        except ValueError:
            self._error_label.config(text="Invalid character(s): Only numbers may be in the Sudoku grid.")
        except SudokuError as e:
            self._error_label.config(text=e)

    def unsolve_puzzle(self) -> None:
        """Returns Sudoku puzzle to state from before running self.solve_puzzle()"""
        self._solve_button.config(text="Solve", command=self.solve_puzzle)

        for y in range(9):
            for x in range(9):
                self._inputs[y][x].delete(0, END)
                if self._puzzle[y][x] == 0:
                    self._inputs[y][x].insert(0, "")
                else:
                    self._inputs[y][x].insert(0, self._puzzle[y][x])

    def restart_puzzle(self) -> None:
        """Resets the Sudoku grid to an empty state"""
        self._sudoku.reset()
        self._error_label.config(text="")
        self._solve_button.config(text="Solve", command=self.solve_puzzle)

        for y in range(9):
            for x in range(9):
                self._inputs[y][x].delete(0, END)
                self._puzzle[y][x] = 0

    def set_value(self, value: int, x: int, y: int) -> None:
        """Sets a specific call in the Sudoku grid and updates the GUI."""
        if not (0 <= x < 9 and 0 <= y < 9):
            raise ValueError(f"Grid coordinates {x},{y} are out of range.")
        if not (0 <= value <= 9):
            raise ValueError(f"Value {value} is not a valid Sudoku number (0-9).")
        self._puzzle[y][x] = value
        self.unsolve_puzzle()

    def close(self) -> None:
        """Close application."""
        self._root.quit()

    def mainloop(self) -> None:
        """Initiate mainloop."""
        self._root.mainloop()


if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
