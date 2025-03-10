# PySudoku - A Sudoku Solver with GUI

## Description

PySudoku is a Python-based Sudoku solver that includes both a command-line and a graphical user interface (GUI). It uses bitmasking for efficient constraint checking and backtracking to find solutions. The GUI, built with Tkinter, allows users to input puzzles, solve them, and reset them easily.

## Features

- **Bitmask-based Sudoku solving** for optimized performance.
- **Graphical user interface (GUI)** built with Tkinter.
- **Interactive input and solving** via the GUI.
- **Error handling** for invalid puzzles and non-numeric inputs.
- **Console-based solver** for users who prefer a terminal interface.

## Installation

Ensure you have Python 3.9 or later installed.

1. Clone the repository or download the files.
   ```sh
   git clone https://github.com/DanJ555/SudokuPy
   cd PySudoku
   ```
2. No additional dependencies are required as Tkinter comes bundled with Python.

## Usage

### Running the GUI

To start the graphical Sudoku solver, run:

```sh
python interface.py
```

### Running the CLI Solver

To use the command-line Sudoku solver, run:

```sh
python solver.py
```

This will solve a predefined puzzle and print the result. You can instead run python and enter the line `from solver import *` and create a `Sudoku` object and pass as an argument, or later with the `Sudoku.set_grid()` method, a 9 by 9 `list[list[int]]` with `0` representing empty spots.


## File Structure

- `solver.py`: Contains the `Sudoku` class, which implements a bitmask-based backtracking solver.
- `interface.py`: Provides the Tkinter-based GUI, allowing interactive puzzle input and solving.

## How It Works

1. The `Sudoku` class initializes a 9x9 grid with bitmask-based constraint tracking.
2. The solver recursively attempts to place numbers while ensuring validity within rows, columns, and 3x3 boxes.
3. The GUI allows users to enter a puzzle, solve it, reset it, and handle invalid inputs.

## Example CLI Output

```
Initial Puzzle:
. . . | . 6 7 | . . .
. 1 . | 9 . . | 7 . .
. . . | . . 3 | 9 4 .
------+-------+------
1 . . | . 4 . | 3 . 7
. 6 . | . . . | . 8 .
4 . 5 | . 9 . | . . 2
------+-------+------
. 5 3 | 2 . . | . . .
. . 6 | . . 5 | . 2 .
. . . | 8 3 . | . . .

Solved Puzzle:
5 9 4 | 1 6 7 | 2 3 8
3 1 8 | 9 2 4 | 7 6 5
6 2 7 | 5 8 3 | 9 4 1
------+-------+------
1 8 9 | 6 4 2 | 3 5 7
7 6 2 | 3 5 1 | 4 8 9
4 3 5 | 7 9 8 | 6 1 2
------+-------+------
8 5 3 | 2 7 6 | 1 9 4
9 7 6 | 4 1 5 | 8 2 3
2 4 1 | 8 3 9 | 5 7 6
```

## License

This project is licensed under the GPL v3.0 License.

