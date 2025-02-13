from tkinter import *
from solver import Sudoku


class SudokuApp:
    def __init__(self, root: Tk) -> None:
        """Initialize the Sudoku GUI application."""
        self.root = root
        self.root.title("PySudoku")
        self.root.geometry("271x325")
        self.root.resizable(width=False, height=False)

        # Initialize Sudoku Solver
        self.sudoku = Sudoku()
        self.puzzle: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]
        self.inputs: list[list[Entry]] = [[None for _ in range(9)] for _ in range(9)]

        self._setup_menu()
        self._setup_ui()
        self._setup_buttons()

    def _setup_menu(self) -> None:
        """Creates the menu bar for the application."""
        menu_bar = Menu(self.root)
        sudoku_menu = Menu(menu_bar, tearoff=0)
        sudoku_menu.add_command(label="New", command=self.restart_puzzle)
        sudoku_menu.add_separator()
        sudoku_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="Options", menu=sudoku_menu, font=("Arial", 10))
        self.root.config(menu=menu_bar)

    def _setup_ui(self) -> None:
        """Creates the Sudoku grid and layout."""
        Label(self.root, text="Enter numbers into grid:").grid()

        grid_frame = Frame(self.root)
        grid_frame.grid()

        for y in range(9):
            for x in range(9):
                entry = Entry(grid_frame, width=3, justify="center")
                entry.grid(row=y, column=x)
                self.inputs[y][x] = entry

        self.error_label = Label(self.root, fg="red", wraplength=260)
        self.error_label.grid(row=3)

    def _setup_buttons(self) -> None:
        """Creates buttons for solving and resetting the puzzle."""
        buttons_frame = Frame(self.root)
        buttons_frame.grid(row=2)

        self.solve_button = Button(buttons_frame, text="Solve", command=self.solve_puzzle, width=8)
        self.solve_button.grid(row=0, column=0)

        reset_button = Button(buttons_frame, text="Reset", command=self.restart_puzzle)
        reset_button.grid(row=0, column=1)

    def restart_puzzle(self) -> None:
        """Resets the Sudoku grid to an empty state."""
        self.error_label.config(text="")
        self.sudoku.reset()

        for y in range(9):
            for x in range(9):
                self.inputs[y][x].delete(0, END)
                self.puzzle[y][x] = 0

        self.solve_button.config(text="Solve", command=self.solve_puzzle)

    def solve_puzzle(self) -> None:
        """Attempts to solve the Sudoku puzzle based on user input."""
        self.error_label.config(text="")

        try:
            for y in range(9):
                for x in range(9):
                    value = self.inputs[y][x].get()
                    self.puzzle[y][x] = int(value) if value.isdigit() else 0

            self.sudoku.set_grid(self.puzzle)
            if self.sudoku.solve():
                self._display_solution()
            else:
                self.error_label.config(text="No solution found!")

        except ValueError as e:
            self.error_label.config(text=str(e))

    def _display_solution(self) -> None:
        """Displays the solved Sudoku grid."""
        solution = self.sudoku.get_grid()
        for y in range(9):
            for x in range(9):
                self.inputs[y][x].delete(0, END)
                self.inputs[y][x].insert(0, solution[y][x])

        self.solve_button.config(text="Unsolve", command=self.unsolve_puzzle)

    def unsolve_puzzle(self) -> None:
        """Resets the Sudoku grid to its original input state."""
        self.error_label.config(text="")

        for y in range(9):
            for x in range(9):
                self.inputs[y][x].delete(0, END)
                if self.puzzle[y][x] == 0:
                    self.inputs[y][x].insert(0, "")
                else:
                    self.inputs[y][x].insert(0, self.puzzle[y][x])

        self.solve_button.config(text="Solve", command=self.solve_puzzle)


if __name__ == "__main__":
    root = Tk()
    app = SudokuApp(root)
    root.mainloop()
