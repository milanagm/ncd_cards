"""Valid Sudoku: only filled cells are checked (rows, columns, 3x3 boxes)."""
METHOD = "isValidSudoku"
COMPARE = "exact"

VALID = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]


def reference(board):
    units = [[(r, c) for c in range(9)] for r in range(9)]
    units += [[(r, c) for r in range(9)] for c in range(9)]
    units += [[(br + r, bc + c) for r in range(3) for c in range(3)] for br in (0, 3, 6) for bc in (0, 3, 6)]
    for unit in units:
        values = [board[r][c] for r, c in unit if board[r][c] != "."]
        if len(values) != len(set(values)):
            return False
    return True


def board_with(*cells):
    board = [["."] * 9 for _ in range(9)]
    for r, c, v in cells:
        board[r][c] = v
    return board


def with_change(r, c, v):
    board = [row[:] for row in VALID]
    board[r][c] = v
    return board


CASES = [
    (VALID,),
    (with_change(0, 0, "8"),),                          # 8 twice in column 0 and box 0
    (board_with(),),
    (board_with((0, 0, "1"), (1, 1, "1")),),            # duplicate only inside a box
    (board_with((4, 0, "7"), (4, 8, "7")),),            # duplicate only in a row
    (board_with((0, 5, "2"), (8, 5, "2")),),            # duplicate only in a column
    (board_with((0, 0, "1"), (3, 3, "1"), (6, 6, "1")),),
]


def random_case(rng):
    board = [row[:] for row in VALID]
    for _ in range(rng.randint(1, 2)):
        r, c = rng.choice([(r, c) for r in range(9) for c in range(9) if board[r][c] == "."])
        board[r][c] = str(rng.randint(1, 9))
    return (board,)
