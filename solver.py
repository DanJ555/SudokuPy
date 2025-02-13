class Grid:

    def __init__(self, grid: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]) -> None:
        self.grid: list[list[int]] = grid
        self.row: list[int] = [0] * 9
        self.col: list[int] = [0] * 9
        self.box: list[int] = [0] * 9
        self._initialize_bitmasks()

    def _initialize_bitmasks(self) -> None:
        for y in range(9):
            for x in range(9):
                if self.grid != 0:
                    value: int = self.grid[y][x]
                    self.row[y] |= (1 << value)
                    self.col[x] |= (1 << value)
                    self.box[(y // 3) * 3 + x // 3] |= (1 << value)
                    
    def set_grid(self, puzzle) -> None:
        self.__init__(puzzle)

    def is_spot_valid(self, x: int, y: int, value: int)-> bool:
        row_is_invalid: int = self.row[y] & (1 << value)
        col_is_invalid: int = self.col[x] & (1 << value)
        box_is_invalid: int = self.box[y // 3 * 3 + x // 3] & (1 << value)

        return not (row_is_invalid or col_is_invalid or box_is_invalid)

    def solve(self, x=0, y=0) -> bool:
        if y == 9:
            return True

        if x == 9:
            return self.solve(0, y + 1)

        if self.grid[y][x] != 0:
            return self.solve(x + 1, y)

        for value in range(1, 10):
            if self.is_spot_valid(x, y, value):
                self.grid[y][x] = value
                self.row[y] |= (1 << value)
                self.col[x] |= (1 << value)
                self.box[(y // 3) * 3 + x // 3] |= (1 << value)

                if self.solve(x + 1, y):
                    return True

                # Backtracking
                self.grid[y][x] = 0
                self.row[y] &= ~(1 << value)
                self.col[x] &= ~(1 << value)
                self.box[(y // 3) * 3 + x // 3] &= ~(1 << value)

    def print(self) -> None:
        for y in range(9):
            if y % 3 == 0 and y != 0:
                print("-" * 21)
            for x in range(9):
                if x % 3 == 0 and x != 0:
                    print("| ", end="")
                if x == 8:
                    print(self.grid[y][x])
                else:
                    print(f"{self.grid[y][x]} ", end="")
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
        [0, 0, 0, 8, 3, 0, 0, 0, 0]
    ]

    grid = Grid(puzzle)
    grid.print()
    grid.solve()
    grid.print()

if __name__ == "__main__":
    main()
