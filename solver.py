from cell import Cell
from strategies import (
    Scope,
    last_possible,
    last_remaining,
    obvious_pair,
    pointing_pair,
    x_wing
)
from sudoku import Sudoku


def solve_sudoku(sudoku: Sudoku):
    changes = True
    scopes = [Scope.CUADRANT, Scope.COLUMN, Scope.ROW]
    while changes:
        changes = False
        changes = last_possible(sudoku)

        for scope in scopes:
            changes = last_remaining(sudoku, scope)
            if changes:
                break

        if changes:
            continue

        for scope in scopes:
            changes = obvious_pair(sudoku, scope)
            if changes:
                break

        if changes:
            continue

        changes = pointing_pair(sudoku)

        if changes:
            continue

        changes = x_wing(sudoku)


if __name__ == "__main__":
    i = 0
    with open('input.txt', 'r') as f:
        lines = f.read().split("\n")

    sudoku = Sudoku()
    i = 1
    for line in lines:
        j = 1
        for input_cell in line.split(","):
            cuadrant = Sudoku.determine_cuadrant(i, j)

            try:
                value = int(input_cell)
            except ValueError:
                value = None

            cell = Cell(i, j, cuadrant, None, value)
            sudoku.add_cell(cell)
            j += 1
        i += 1

    sudoku.print()
    input()
    solve_sudoku(sudoku)
    sudoku.print()
