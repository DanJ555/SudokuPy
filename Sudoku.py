class Grid:

    def __init__(self, puzzle: list[int] = None) -> None:
        self.values_stream: list[Cell] = [Cell() for _ in range(81)]
        self.rows: list[list[Cell]] = [[] for _ in range(9)]
        self.columns: list[list[Cell]] = [[] for _ in range(9)]
        self.boxes: list[list[Cell]] = [[] for _ in range(9)]
        self.__establish_sublists()
        self.printable: bool = False
        if puzzle is not None:
            self.set_values(puzzle)

    def __establish_sublists(self) -> None:
        row_index = -1
        box_index = -1
        for index, cell in enumerate(self.values_stream):
            # establish columns
            column_index = index % 9
            self.columns[column_index].append(cell)
            cell.parent_column = self.columns[column_index]
            # establish rows
            if column_index == 0:
                row_index += 1
            self.rows[row_index].append(cell)
            cell.parent_row = self.rows[row_index]
            # establish 3x3 boxes
            if column_index % 3 == 0:
                box_index += 1
            self.boxes[box_index].append(cell)
            cell.parent_box = self.boxes[box_index]
            if column_index == 8 and index % 27 != 26:
                box_index -= 3
            cell.parent_grid = self

    def __str__(self) -> str:
        cumulative = f"{"_" * 19}\n"
        for row in self.rows:
            addition = "|"
            for cell in row:
                if cell.value == 0:
                    addition += " |"
                else:
                    addition += str(f"{cell}|")
            cumulative += f"{addition}\n"
        cumulative += "¯" * 19
        return cumulative

    def set_values(self, puzzle: list[int]) -> None:
        for index, value in enumerate(puzzle):
            self.values_stream[index].assign_value(value)
        self.printable = True
        print(self)

    def reset(self) -> None:
        self.printable = False
        for cell in self.values_stream:
            cell.reset()
        self.printable = True
        print(self)

    def print_possibles_by_box(self) -> None:
        for box in self.boxes:
            print(f"{"_" * 55}\nNew box output")
            for cell in box:
                print(f"{cell.__repr__()}")

    def is_solved(self) -> bool:
        for groups in (self.rows, self.columns, self.boxes):
            for group in groups:
                if sum(group) != 45:
                    return False
        print("Puzzle has been solved.")
        return True

    def solve(self) -> None:
        # I just want this to work. I'm not too concerned about efficiency right now.
        # Hidden Singles search
        for index, groups in enumerate((self.rows, self.columns, self.boxes)):
            for group in groups:
                occurrences: list[list[Cell]] = []
                for n in range(9):
                    occurrences.append([])
                    for cell in group:
                        if (n + 1) in cell.possible_values:
                            occurrences[n].append(cell)
                for i, occurrence in enumerate(occurrences):
                    occurrence_amount: int = len(occurrence)
                    if occurrence_amount == 1:
                        occurrence[0].assign_value(i + 1)
        # Naked pairs
        for box in self.boxes:
            for cell in box:
                if not cell.possible_values:
                    pass
                else:
                    same_possibles: list[Cell] = []
                    for sibling_cell in box:
                        if cell.possible_values == sibling_cell.possible_values:
                            same_possibles.append(sibling_cell)
                    possibles = same_possibles[0].possible_values
                    if len(same_possibles) == 2:
                        if len(possibles) == 2:
                            for cell_ii in box:
                                if cell_ii not in same_possibles:
                                    cell_ii.remove_possible_value(possibles[0])
                                    cell_ii.remove_possible_value(possibles[1])
                    # Naked Triples
                    if len(same_possibles) == 3:
                        if len(possibles) == 3:
                            for cell_ii in box:
                                if cell_ii not in same_possibles:
                                    cell_ii.remove_possible_value(possibles[0])
                                    cell_ii.remove_possible_value(possibles[1])
                                    cell_ii.remove_possible_value(possibles[2])
                    # print(len(same_possibles))
                    # for c in same_possibles:
                    #    print(f"{c} has possibles {c.possible_values}")
        for box in self.boxes:
            occurrences: list[list[Cell]] = []
            for n in range(9):
                a: list[Cell] = []
                occurrences.append(a)
                for cell in box:
                    if (n + 1) in cell.possible_values:
                        a.append(cell)
            print(f"{"_" * 55}\nNew box output")
            for n in range(9):
                print(f"Cells where {n+1} is possible: {occurrences[n]}")
            for occurrence in occurrences:
                if len(occurrence) == 2:
                    if occurrence[0].parent_column == occurrence[1].parent_column:
                        print("Hidden Pair found!")
                        for cell in occurrence[0].parent_column:
                            if cell not in occurrence:
                                print(occurrence[0].possible_values)
                                try:
                                    cell.remove_possible_value(occurrence[0].possible_values[0])
                                    cell.remove_possible_value(occurrence[0].possible_values[1])
                                except IndexError:
                                    pass
            # print(occurrences)

            '''
            if 2 <= occurrence_amount <= 3:
                if occurrence[0].parent_row == occurrence[1].parent_row == occurrence[-1].parent_row:
                    for cell in occurrence[0].parent_column:
                        # if cell != occurrence[0]:
                        if cell not in occurrence:
                            cell.remove_possible_value(i)
                if occurrence[0].parent_column == occurrence[1].parent_column == occurrence[-1].parent_column:
                    for cell in occurrence[0].parent_row:
                        # if cell != occurrence[0]:
                        if cell not in occurrence:
                            cell.remove_possible_value(i)
        '''
        print("end")


class Cell:

    def __init__(self, value: int = 0) -> None:
        self.value: int = None
        self.possible_values: list[int] = None
        self.assign_value(value)
        self.parent_box: list[Cell] = None
        self.parent_row: list[Cell] = None
        self.parent_column: list[Cell] = None
        # self.parents: list[list[Cell]] = None   # Boxes, Rows, Columns
        self.parent_grid: Grid = None

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Cell({self.value}: {self.possible_values})"

    def __add__(self, other) -> int:
        return self.value + other

    def __radd__(self, other) -> int:
        return self.__add__(other)

    def remove_possible_value(self, value: int) -> None:
        try:
            self.possible_values.remove(value)
        except ValueError:
            pass
        if len(self.possible_values) == 1 and self.value == 0:
            self.assign_value(self.possible_values[0])
            self.possible_values = []

    def assign_value(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError("Invalid type for Sudoku Puzzle: {type(value)}. Puzzle should consist of type 'int'")
        if not (0 <= value <= 9):
            raise ValueError("Invalid integer: numbers should be from 0 to 9.")
        if value == self.value:
            pass
        else:
            self.value = value
            if value == 0:
                self.possible_values = [i + 1 for i in range(9)]
            else:
                self.possible_values = []
            try:
                if self.parent_grid.printable:
                    print(self.parent_grid)
                parents = [self.parent_box, self.parent_row, self.parent_column]
                for parent in parents:
                    for cell in parent:
                        cell.remove_possible_value(value)
            except AttributeError:
                pass

    def reset(self) -> None:
        self.value = 0
        self.possible_values = [i+1 for i in range(9)]


puzzle = [0, 0, 0, 0, 0, 0, 0, 0, 0,
          9, 0, 0, 0, 6, 3, 0, 0, 1,
          0, 0, 6, 0, 2, 7, 9, 5, 0,
          1, 0, 0, 0, 0, 9, 0, 0, 0,
          4, 7, 3, 0, 0, 0, 1, 6, 9,
          0, 0, 0, 1, 0, 0, 0, 0, 8,
          0, 8, 4, 3, 1, 0, 6, 0, 0,
          2, 0, 0, 6, 8, 0, 0, 0, 5,
          0, 0, 0, 0, 0, 0, 0, 0, 0]


def create_grid(puzzle: list[int]) -> Grid:
    return Grid(puzzle)


def main() -> Grid:
    grid = Grid(puzzle)
    grid.solve()
    # grid = create_grid(puzzle)
    # while not grid.is_solved():
    #    grid.solve()
    return grid


if __name__ == "__main__":
    main()

grid = main()
