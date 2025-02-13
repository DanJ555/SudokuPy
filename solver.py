from copy import deepcopy


class Sudoku:

    def __init__(self, grid=None) -> None:
        if grid is None:
            grid = [[0 for _ in range(9)] for _ in range(9)]
        self._grid: list[list[int]] = deepcopy(grid)
        self._row: list[int] = [0] * 9
        self._col: list[int] = [0] * 9
        self._box: list[int] = [0] * 9
        if not self._initialize_bitmasks():
            self.print()
            raise ValueError("Invalid Sudoku puzzle: Duplicate numbers detected")

    def _initialize_bitmasks(self) -> bool:
        for y in range(9):
            for x in range(9):
                if self._grid != 0:
                    value: int = self._grid[y][x]
                    bit = 1 << value

                    if not self._is_spot_valid(x, y, value):
                        return False

                    self._row[y] |= bit
                    self._col[x] |= bit
                    self._box[(y // 3) * 3 + x // 3] |= bit

        return True

    def set_grid(self, puzzle) -> None:
        self.__init__(puzzle)

    def get_grid(self) -> list[list[int]]:
        return self._grid

    def reset(self) -> None:
        self.__init__()

    def _is_spot_valid(self, x: int, y: int, value: int) -> bool:
        if value == 0:
            return True

        bit = 1 << value
        row_is_invalid: int = self._row[y] & bit
        col_is_invalid: int = self._col[x] & bit
        box_is_invalid: int = self._box[y // 3 * 3 + x // 3] & bit

        return not (row_is_invalid or col_is_invalid or box_is_invalid)

    def solve(self, x=0, y=0) -> bool:
        if y == 9:
            return True

        if x == 9:
            return self.solve(0, y + 1)

        if self._grid[y][x] != 0:
            return self.solve(x + 1, y)

        for value in range(1, 10):
            if self._is_spot_valid(x, y, value):
                self._grid[y][x] = value
                bit = 1 << value

                self._row[y] |= bit
                self._col[x] |= bit
                self._box[(y // 3) * 3 + x // 3] |= bit

                if self.solve(x + 1, y):
                    return True

                self._grid[y][x] = 0
                self._row[y] &= ~bit
                self._col[x] &= ~bit
                self._box[(y // 3) * 3 + x // 3] &= ~bit

        return False

    def print(self) -> None:
        for y in range(9):
            if y % 3 == 0 and y != 0:
                print("-" * 21)
            for x in range(9):
                value = self._grid[y][x]
                if value == 0:
                    value = " "
                if x % 3 == 0 and x != 0:
                    print("| ", end="")
                if x == 8:
                    print(value)
                else:
                    print(f"{value} ", end="")
        print()


def main() -> None:
    puzzle: list[list[int]] = [
        [0, 0, 0, 0, 6, 7, 0, 0, 0],
        [0, 1, 0, 9, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 3, 9, 4, 0],
        [1, 0, 0, 0, 4, 0, 3, 0, 7],
        [0, 6, 0, 0, 0, 0, 0, 8, 0],
        [4, 0, 5, 0, 9, 0, 0, 0, 2],
        [0, 5, 3, 2, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 5, 0, 2, 0],
        [0, 0, 0, 8, 3, 0, 0, 0, 0]]

    sudoku = Sudoku(puzzle)
    sudoku.print()
    sudoku.solve()
    sudoku.print()
    print(puzzle)
    print(sudoku.get_grid())


if __name__ == "__main__":
    main()
