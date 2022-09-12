from ast import Return
from enum import Enum
from operator import attrgetter
from typing import List
from cell import Cell, copy_sudoku, get_blocks_from_column, get_blocks_from_cuadrant, get_blocks_from_row, get_specific_block, is_different


def xor(x: bool, y: bool):
    return bool((x and not y) or (not x and y))


class Scope(Enum):
    ROW = "row"
    COLUMN = "column"
    CUADRANT = "cuadrant"


def last_possible(sudoku: List[Cell]):
    changes = True
    i = 1
    while changes:
        changes = False
        copy = copy_sudoku(sudoku)
        for block in sudoku:
            if not block.number:
                possibilities = block.possibilities or {
                    1, 2, 3, 4, 5, 6, 7, 8, 9}
                row_blocks = get_blocks_from_row(sudoku, block.row)
                column_blocks = get_blocks_from_column(sudoku, block.column)
                cuadrant_blocks = get_blocks_from_cuadrant(
                    sudoku, block.cuadrant)

                for other_block in row_blocks:
                    if other_block.number and other_block.number in possibilities:
                        possibilities.remove(other_block.number)

                for other_block in column_blocks:
                    if other_block.number and other_block.number in possibilities:
                        possibilities.remove(other_block.number)

                for other_block in cuadrant_blocks:
                    if other_block.number and other_block.number in possibilities:
                        possibilities.remove(other_block.number)

                if len(possibilities) == 1:
                    block.number = list(possibilities)[0]
                    block.possibilities = None
                else:
                    block.possibilities = possibilities
        changes = is_different(sudoku, copy)
        i += 1
    return i > 2


def last_remaining(sudoku: List[Cell], scope: Scope):
    changes = True
    i = 1
    get_blocks = (get_blocks_from_cuadrant if scope == Scope.CUADRANT else
                  get_blocks_from_column if scope == Scope.COLUMN else get_blocks_from_row)

    while changes:
        changes = False
        copy = copy_sudoku(sudoku)
        for block in sudoku:
            if not block.number:
                block_scope = (block.cuadrant if scope == Scope.CUADRANT else
                               block.column if scope == Scope.COLUMN else block.row)

                possibilities = block.possibilities
                scope_blocks = [b
                                for b in get_blocks(sudoku, block_scope)
                                if b.possibilities and (b.row != block.row or b.column != block.column)]
                scope_possibilities = set()

                for b in scope_blocks:
                    scope_possibilities.update(b.possibilities)

                possibilities = possibilities - scope_possibilities
                if len(possibilities) == 1:
                    block.number = list(possibilities)[0]
                    block.possibilities = None

        changes = is_different(sudoku, copy)
        i += 1
    return i > 2


def obvious_pair(sudoku: List[Cell], scope: Scope):
    changes = True
    i = 1
    get_blocks = (get_blocks_from_cuadrant if scope == Scope.CUADRANT else
                  get_blocks_from_column if scope == Scope.COLUMN else get_blocks_from_row)

    while changes:
        changes = False
        copy = copy_sudoku(sudoku)
        for block in sudoku:
            if not block.number and 2 <= len(block.possibilities) <= 4:
                block_scope = (block.cuadrant if scope == Scope.CUADRANT else
                               block.column if scope == Scope.COLUMN else block.row)

                scope_blocks = [b
                                for b in get_blocks(sudoku, block_scope)
                                if b.possibilities and (b.row != block.row or b.column != block.column)]
                excluded = [(block.row, block.column)]

                for b in scope_blocks:
                    if b.possibilities == block.possibilities:
                        excluded.append((b.row, b.column))

                if len(excluded) == len(block.possibilities):
                    for b in scope_blocks:
                        if (b.row, b.column) not in excluded:
                            b.possibilities = b.possibilities - block.possibilities

        changes = is_different(sudoku, copy)
        i += 1
    return i > 2


def pointing_pair(sudoku: List[Cell]):
    changes = True
    i = 1

    while changes:
        changes = False
        copy = copy_sudoku(sudoku)
        for block in sudoku:
            if not block.number:
                scope_blocks = [b
                                for b in get_blocks_from_cuadrant(sudoku, block.cuadrant)
                                if b.possibilities and (b.column != block.column or b.row != block.row)]

                for b in scope_blocks:
                    if xor(b.row == block.row, b.column == block.column):
                        poss = b.possibilities | block.possibilities
                        for bl in scope_blocks:
                            if bl.column != b.column or bl.row != b.row:
                                poss = poss - bl.possibilities
                        if len(poss) == 1:
                            scope = Scope.ROW if b.row == block.row else Scope.COLUMN
                            get_blocks = get_blocks_from_row if b.row == block.row else get_blocks_from_column
                            scope_index = b.row if b.row == block.row else b.column
                            for bl in get_blocks(sudoku, scope_index):
                                if scope == Scope.COLUMN:
                                    if bl.possibilities and bl.row != b.row and bl.row != block.row:
                                        bl.possibilities = bl.possibilities - poss
                                else:
                                    if bl.possibilities and bl.column != b.column and bl.column != block.column:
                                        bl.possibilities = bl.possibilities - poss
        changes = is_different(sudoku, copy)
        i += 1
    return i > 2


def x_wing(sudoku: List[Cell]):
    changes = True
    it = 1
    
    while changes:
        changes = False
        copy = copy_sudoku(sudoku)
        for column in range(1, 9):
            for row in range(1, 9):
                column_block = get_specific_block(sudoku, row, column)

                if column_block.possibilities == None:
                    continue
                
                for possibility in column_block.possibilities:
                    possible_blocks = [block for block in get_blocks_from_column(sudoku, column)
                                       if block.possibilities and possibility in block.possibilities and block.row != row]

                    if len(possible_blocks) != 1:
                        continue

                    possible_block = possible_blocks[0]
                    row_2 = possible_block.row
                    for pararell_column in range(column+1, 10):
                        pararell_block1 = get_specific_block(
                            sudoku, row, pararell_column)
                        if not pararell_block1.possibilities or possibility not in pararell_block1.possibilities:
                            continue

                        pararell_block2 = get_specific_block(
                            sudoku, row_2, pararell_column)
                        if pararell_block2.possibilities and possibility not in pararell_block2.possibilities:
                            continue

                        cont = False
                        for block in get_blocks_from_column(sudoku, pararell_column):
                            if (block.possibilities and possibility in block.possibilities and
                                    block.row != row and block.row != row_2):
                                cont = True
                                break

                        if cont:
                            continue

                        for row_block in get_blocks_from_row(sudoku, row):
                            if (row_block.possibilities
                                    and row_block.column not in (column, pararell_column)):
                                row_block.possibilities.discard(possibility)

                        for row_block in get_blocks_from_row(sudoku, row_2):
                            if (row_block.possibilities
                                    and row_block.column not in (column, pararell_column)):
                                row_block.possibilities.discard(possibility)

        changes = is_different(sudoku, copy)
        it += 1
    return it > 2
