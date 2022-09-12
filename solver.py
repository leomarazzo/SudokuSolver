from operator import attrgetter
from typing import List
from cell import Cell, get_blocks_from_row
from strategies import Scope, last_possible, last_remaining, obvious_pair, pointing_pair, x_wing


def print_sudoku(sudoku: List[Cell]):
    blocks = sorted(sudoku, key=attrgetter("row", "column"))
    for i in range(9):
        if i % 3 == 0:
            print("_"*46)
        row = []
        for block in get_blocks_from_row(blocks, i+1):
            possibilities = ",".join(
                str(x) for x in block.possibilities) if block.possibilities else None
            s = block.number if block.number else possibilities if possibilities else "X"
            row.append(s)
        print(
            "|{:^4} {:^4} {:^4}|{:^4} {:^4} {:^4}|{:^4} {:^4} {:^4}|".format(*row))
    print("_"*46)


def solve_sudoku(sudoku: List[Cell]):
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


def determine_cuadrant(row, column):
    if row in [1, 2, 3]:
        cuadrant = 1
    elif row in [4, 5, 6]:
        cuadrant = 4
    else:
        cuadrant = 7

    if column in [4, 5, 6]:
        cuadrant += 1
    elif column in [7, 8, 9]:
        cuadrant += 2

    return cuadrant


if __name__ == "__main__":
    sudoku = []
    i = 0
    with open('input.txt', 'r') as f:
        lines = f.read().split("\n")

    i = 1
    for line in lines:
        j = 1
        for input_block in line.split(","):
            cuadrant = determine_cuadrant(i, j)

            try:
                value = int(input_block)
            except ValueError:
                value = None

            block = Cell(i, j, cuadrant, None, value)
            sudoku.append(block)
            j += 1
        i += 1

    print_sudoku(sudoku)
    input()
    solve_sudoku(sudoku)
    print_sudoku(sudoku)
