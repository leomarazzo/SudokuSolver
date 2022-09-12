from copy import deepcopy
from dataclasses import dataclass
from operator import attrgetter
from typing import List, Optional, Set


@dataclass
class Cell:
    row: int
    column: int
    cuadrant: int
    possibilities: Optional[Set[int]]
    number: Optional[int]


def get_specific_block(blocks: List[Cell], row, column):
    for block in blocks:
        if block.row == row and block.column == column:
            return block
        
    raise Exception(row, column)


def get_blocks_from_row(blocks: List[Cell], row):
    return [block for block in blocks if block.row == row]


def get_blocks_from_column(blocks: List[Cell], column):
    return [block for block in blocks if block.column == column]


def get_blocks_from_cuadrant(blocks: List[Cell], cuadrant):
    return [block for block in blocks if block.cuadrant == cuadrant]


def is_different(sudoku: List[Cell], copy_sudoku: List[Cell]):
    blocks = sorted(sudoku, key=attrgetter("row", "column"))
    blocks_copy = sorted(copy_sudoku, key=attrgetter("row", "column"))
    for i in range(len(blocks)):
        block = blocks[i]
        block_copy = blocks_copy[i]

        if block_copy.number != block.number:
            return True

        if block_copy.possibilities != block.possibilities:
            return True

    return False


def copy_sudoku(sudoku: List[Cell]):
    return [deepcopy(block) for block in sudoku]
