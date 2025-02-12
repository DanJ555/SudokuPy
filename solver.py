def print_grid(grid) -> None:
    for row in range(len(grid)):
        if row % 3 == 0 and row != 0:
            print("-" * 21)
        for col in range(len(grid[row])):
            if col % 3 == 0 and col != 0:
                print("| ", end="")
            if col == 8:
                print(grid[row][col])
            else:
                print(f"{grid[row][col]} ", end="")


def is_spot_valid(x: int, y: int, value: int, row: list[int], col: list[int], box: list[int]) -> bool:
    row_is_invalid: int = row[y] & (1 << value)
    col_is_invalid: int = col[x] & (1 << value)
    box_is_invalid: int = box[y // 3 * 3 + x // 3] & (1 << value)

    if row_is_invalid or col_is_invalid or box_is_invalid:
        return False

    return True


def solve_grid(grid, x, y, row, col, box) -> bool:
    start_next_row = 9

    if y == start_next_row - 1 and x == start_next_row:
        return True

    if x == start_next_row:
        y += 1
        x = 0

    if grid[y][x] != 0:
        return solve_grid(grid, x+1, y, row, col, box)

    for value in range(1, 10):
        if is_spot_valid(x, y, value, row, col, box):
            grid[y][x] = value
            row[y] |= (1 << value)
            col[x] |= (1 << value)
            box[(y // 3) * 3 + x // 3] |= (1 << value)

            if solve_grid(grid, x, y, row, col, box):
                return True

            grid[y][x] = 0
            row[y] &= ~(1 << value)
            col[x] &= ~(1 << value)
            box[(y // 3) * 3 + x // 3] &= ~(1 << value)

    return False


def init_bits(grid: list[list[int]]) -> (list[int]):
    row: list[int] = [0] * 9
    col: list[int] = [0] * 9
    box: list[int] = [0] * 9

    for y in range(9):
        for x in range(9):
            if grid[y][x] != 0:
                row[y] |= (1 << grid[y][x])
                col[x] |= (1 << grid[y][x])
                box[(y // 3) * 3 + x // 3] |= (1 << grid[y][x])

    return row, col, box


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
    row, col, box = init_bits(puzzle)
    print_grid(puzzle)
    print()
    solve_grid(puzzle, 0, 0, row, col, box)
    print_grid(puzzle)


if __name__ == "__main__":
    main()
