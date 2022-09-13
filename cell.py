from __future__ import annotations
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
    
    def is_same_cell(self, cell: Cell):
        return self.row == cell.row and self.column == cell.column