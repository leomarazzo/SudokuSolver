from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from operator import attrgetter
from typing import List
from cell import Cell



@dataclass
class Sudoku:

    cells: List[Cell] = field(default_factory=list)

    def add_cell(self, cell: Cell):
        self.cells.append(cell)

    def get_specific_cell(self, row: int, column: int):
        for cell in self.cells:
            if cell.row == row and cell.column == column:
                return cell

        raise Exception(row, column)

    def get_cells_from_row(self, row: int):
        return [cell for cell in self.cells if cell.row == row]

    def get_cells_from_column(self, column: int):
        return [cell for cell in self.cells if cell.column == column]

    def get_cells_from_cuadrant(self, cuadrant: int):
        return [cell for cell in self.cells if cell.cuadrant == cuadrant]

    def copy(self):
        cells_copy = [deepcopy(cell) for cell in self.cells]
        return Sudoku(cells_copy)

    def is_different(self, copy_sudoku: Sudoku):
        cells = sorted(self.cells, key=attrgetter("row", "column"))
        blocks_copy = sorted(
            copy_sudoku.cells, key=attrgetter("row", "column"))

        for i in range(len(cells)):
            block = cells[i]
            block_copy = blocks_copy[i]

            if block_copy.number != block.number:
                return True

            if block_copy.possibilities != block.possibilities:
                return True

        return False

    def print(self):
        for i in range(9):
            if i % 3 == 0:
                print("_"*46)
            row = []
            for block in self.get_cells_from_row(i+1):
                possibilities = ",".join(
                    str(x) for x in block.possibilities) if block.possibilities else None
                s = block.number if block.number else possibilities if possibilities else "X"
                row.append(s)
            
            row_string = "|{:^4} {:^4} {:^4}"*3 + "|"
            print(row_string.format(*row))
        print("_"*46)
        
    @staticmethod
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
