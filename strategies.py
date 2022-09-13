from enum import Enum
from sudoku import Sudoku


def xor(x: bool, y: bool):
    return bool((x and not y) or (not x and y))


class Scope(Enum):
    ROW = "row"
    COLUMN = "column"
    CUADRANT = "cuadrant"


def last_possible(sudoku: Sudoku):
    changes = True
    i = 1
    while changes:
        changes = False
        copy = sudoku.copy()
        for cell in sudoku.cells:
            if not cell.number:

                possibilities = cell.possibilities.copy() if cell.possibilities else {
                    1, 2, 3, 4, 5, 6, 7, 8, 9}

                for other_cell in sudoku.get_cells_from_row(cell.row):
                    if other_cell.number and other_cell.number in possibilities:
                        possibilities.remove(other_cell.number)

                for other_cell in sudoku.get_cells_from_column(cell.column):
                    if other_cell.number and other_cell.number in possibilities:
                        possibilities.remove(other_cell.number)

                for other_cell in sudoku.get_cells_from_cuadrant(cell.cuadrant):
                    if other_cell.number and other_cell.number in possibilities:
                        possibilities.remove(other_cell.number)

                if len(possibilities) == 1:
                    cell.number = list(possibilities)[0]
                    cell.possibilities = None
                else:
                    cell.possibilities = possibilities

        changes = sudoku.is_different(copy)
        i += 1
    return i > 2


def last_remaining(sudoku: Sudoku, scope: Scope):
    changes = True
    i = 1
    get_cells = (sudoku.get_cells_from_cuadrant if scope == Scope.CUADRANT else
                 sudoku.get_cells_from_column if scope == Scope.COLUMN else sudoku.get_cells_from_row)

    while changes:
        changes = False
        copy = sudoku.copy()
        for cell in sudoku.cells:
            if not cell.number:
                block_scope = (cell.cuadrant if scope == Scope.CUADRANT else
                               cell.column if scope == Scope.COLUMN else cell.row)

                possibilities = cell.possibilities.copy()
                scope_blocks = [b
                                for b in get_cells(block_scope)
                                if b.possibilities and (b.row != cell.row or b.column != cell.column)]
                scope_possibilities = set()

                for b in scope_blocks:
                    scope_possibilities.update(b.possibilities.copy())

                possibilities = possibilities - scope_possibilities
                if len(possibilities) == 1:
                    cell.number = list(possibilities)[0]
                    cell.possibilities = None

        changes = sudoku.is_different(copy)
        i += 1
    return i > 2


def obvious_pair(sudoku: Sudoku, scope: Scope):
    changes = True
    i = 1
    get_cells = (sudoku.get_cells_from_cuadrant if scope == Scope.CUADRANT else
                 sudoku.get_cells_from_column if scope == Scope.COLUMN else sudoku.get_cells_from_row)

    while changes:
        changes = False
        copy = sudoku.copy()
        for cell in sudoku.cells:
            if not cell.number and 2 <= len(cell.possibilities) <= 4:
                cell_scope = (cell.cuadrant if scope == Scope.CUADRANT else
                              cell.column if scope == Scope.COLUMN else cell.row)

                scope_cells = [b
                               for b in get_cells(cell_scope)
                               if b.possibilities and not cell.is_same_cell(b)]
                excluded = [(cell.row, cell.column)]

                for b in scope_cells:
                    if b.possibilities == cell.possibilities:
                        excluded.append((b.row, b.column))

                if len(excluded) == len(cell.possibilities):
                    for b in scope_cells:
                        if (b.row, b.column) not in excluded:
                            b.possibilities = b.possibilities - cell.possibilities

        changes = sudoku.is_different(copy)
        i += 1
    return i > 2


def pointing_pair(sudoku: Sudoku):
    changes = True
    i = 1

    while changes:
        changes = False
        copy = sudoku.copy()
        for cell in sudoku.cells:
            if not cell.number:
                scope_cells = [b
                               for b in sudoku.get_cells_from_cuadrant(cell.cuadrant)
                               if b.possibilities and not cell.is_same_cell(b)]

                for c in scope_cells:
                    if xor(c.row == cell.row, c.column == cell.column):
                        poss = c.possibilities | cell.possibilities
                        for cl in scope_cells:
                            if not c.is_same_cell(cl):
                                poss = poss - cl.possibilities
                        if len(poss) == 1:
                            scope = Scope.ROW if c.row == cell.row else Scope.COLUMN
                            get_blocks = sudoku.get_cells_from_row if c.row == cell.row else sudoku.get_cells_from_column
                            scope_index = c.row if c.row == cell.row else c.column
                            for cl in get_blocks(scope_index):
                                if scope == Scope.COLUMN:
                                    if cl.possibilities and cl.row != c.row and cl.row != cell.row:
                                        cl.possibilities = cl.possibilities - poss
                                else:
                                    if cl.possibilities and cl.column != c.column and cl.column != cell.column:
                                        cl.possibilities = cl.possibilities - poss
        changes = sudoku.is_different(copy)
        i += 1
    return i > 2


def x_wing(sudoku: Sudoku):
    changes = True
    it = 1

    while changes:
        changes = False
        copy = sudoku.copy()
        for column in range(1, 9):
            for row in range(1, 9):
                column_cell = sudoku.get_specific_cell(row, column)

                if column_cell.possibilities == None:
                    continue

                for possibility in column_cell.possibilities:
                    possible_cells = [cell for cell in sudoku.get_cells_from_column(column)
                                      if cell.possibilities and possibility in cell.possibilities and cell.row != row]

                    if len(possible_cells) != 1:
                        continue

                    possible_block = possible_cells[0]
                    row_2 = possible_block.row
                    for pararell_column in range(column+1, 10):
                        pararell_block1 = sudoku.get_specific_cell(
                            row, pararell_column)
                        if not pararell_block1.possibilities or possibility not in pararell_block1.possibilities:
                            continue

                        pararell_block2 = sudoku.get_specific_cell(
                            row_2, pararell_column)
                        if pararell_block2.possibilities and possibility not in pararell_block2.possibilities:
                            continue

                        cont = False
                        for cell in sudoku.get_cells_from_column(pararell_column):
                            if (cell.possibilities and possibility in cell.possibilities and
                                    cell.row != row and cell.row != row_2):
                                cont = True
                                break

                        if cont:
                            continue

                        for row_cell in sudoku.get_cells_from_row(row):
                            if (row_cell.possibilities and row_cell.column not in (column, pararell_column)):
                                row_cell.possibilities.discard(possibility)

                        for row_cell in sudoku.get_cells_from_row(row_2):
                            if (row_cell.possibilities and row_cell.column not in (column, pararell_column)):
                                row_cell.possibilities.discard(possibility)

        changes = sudoku.is_different(copy)
        it += 1
    return it > 2
