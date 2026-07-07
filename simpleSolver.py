from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Collection
from copy import deepcopy
from enum import Enum, auto
from typing import Dict, Iterator, List, Set, Tuple

from simpleChecker import SudokuChecker
from sudoku import Sudoku


class SudokuSolver(ABC):
    def __init__(self, sudoku: Sudoku, checker: SudokuChecker) -> None:
        self.sudoku = deepcopy(sudoku)
        self.checker = checker
        if not self.checker.isRegular(self.sudoku):
            raise ValueError(
                "Sudoku is not regular. Non-regular sudokus can't be solved."
            )
        self.sudokuIsSolved = self.checker.isSolved(self.sudoku)

    def getSudoku(self) -> Sudoku:
        return self.sudoku

    @abstractmethod
    def solve(self) -> bool:
        """Solves the Sudoku

        Result is in self.sudoku
        Returns True if final solution is reached"""
        pass

    @abstractmethod
    def nextStep(self) -> Iterator[tuple[int, int, int]]:
        """Returns next step for solving.

        returns value, row, col of cell"""
        pass


class SimpleSolver(SudokuSolver):
    def __init__(self, sudoku: Sudoku, checker: SudokuChecker) -> None:
        super().__init__(sudoku, checker)

    def getSudoku(self) -> Sudoku:
        return super().getSudoku()

    def solve(self):
        # TODO!
        # * Add backtracking mode

        sudokuModified = True
        iterationCounter = 0  # DEBUG ?

        while sudokuModified:
            sudokuModified = False
            iterationCounter += 1  # DEBUG ?

            allowed_values = self.getPossibleValuesForEmptyCells(self.sudoku)
            sudokuModified = self.updateSudokuForCellsWithOnlyOnePossibleValue(
                self.sudoku,
                allowed_values
            )
            if sudokuModified:
                continue

            sudokuModified = self.updateSudokuWhenValueIsOnlyOnceInAnArea(
                self.sudoku,
                allowed_values
            )

        print("iterations:", iterationCounter)  # DEBUG ?
        return self.checker.isSolved(self.sudoku)

    def nextStep(self):
        # TODO!
        yield 0, 0, 0

    class Cell():
        def __init__(self, row: int, col: int, values: Set[int]) -> None:
            self.row = row
            self.col = col
            self.values = values

        def __hash__(self) -> int:
            return hash((self.row, self.col))

    @staticmethod
    def solveRulebased(sudoku: Sudoku):
        pass

    def getPossibleValuesForEmptyCells(self, sudoku: Sudoku) -> List[Cell]:
        """Returns a dict with the coordinates of all currently empty (0) cells: all at the possible Values"""
        # TODO: Test
        return [
            self.Cell(row, col, self.getPossibleValuesForCell(sudoku, row, col))
            for row in range(Sudoku.ROWS)
            for col in range(Sudoku.COLS)
            if sudoku.getCellValue(row, col) == 0
        ]

    def getPossibleValuesForCell(self, sudoku:Sudoku, row: int, col: int) -> Set[int]:
        # TODO: Test
        return (
            self.getPossibleValues(sudoku.getRow(row))
            & self.getPossibleValues(sudoku.getCol(col))
            & self.getPossibleValues(sudoku.getField(row=row, col=col))
        )

    @staticmethod
    def getPossibleValues(input: Collection[int]) -> Set[int]:
        """Returns the values of 1...9 which are not used yet"""
        return {1, 2, 3, 4, 5, 6, 7, 8, 9} - set(input)

    def updateSudokuForCellsWithOnlyOnePossibleValue(
        self, sudoku: Sudoku, possibleCellValues: List[Cell]
    ) -> bool:
        """If a Cell only has one possible Value, it is final and Sudoku can be modified

        Returns True if modification was done at least once
        """
        modificationDone = False
        for cell in possibleCellValues:
            if len(cell.values) == 1:
                sudoku.modifyCell(
                    cell.row,
                    cell.col,
                    cell.values.pop(),
                )
                modificationDone = True

        return modificationDone

    def updateSudokuWhenValueIsOnlyOnceInAnArea(
        self, sudoku: Sudoku, allowed_values: List[Cell]
    ) -> bool:
        """If a Value is only allowed once for an area, this cell must get this value.

        Area here is either a row, a col or a field.
        Returns True when an update was done.
        """

        cell_list = self.getCellsWithUniqueValue(allowed_values)
        if not cell_list:
            return False

        for cell in cell_list:
            sudoku.modifyCell(cell.row, cell.col, cell.values.pop())
        return True

    @staticmethod
    def getCellsWithUniqueValue(
        allowed_values: List[Cell],
    ) -> List[Cell]:
        """Checks if a cell is the only possibility for a value in an area.

        Returns a list with this cells (row, col, value)"""

        class AreaType(Enum):
            ROW = auto()
            COL = auto()
            FIELD = auto()

        class Area:
            def __init__(self, type: AreaType):
                self.type = type
                match self.type:
                    case AreaType.ROW:
                        self.area_length = Sudoku.ROWS
                    case AreaType.COL:
                        self.area_length = Sudoku.COLS
                    case AreaType.FIELD:
                        self.area_length = Sudoku.FIELDS
                self.counter = [Counter() for _ in range(self.area_length)]
                self.cells: List[Dict[int, Tuple[int,int]]] = [dict() for _ in range(self.area_length)]

            def sig_coord(self, row, col) -> int:
                """Returns significant coordinate per AreaType"""
                match self.type:
                    case AreaType.ROW:
                        return row
                    case AreaType.COL:
                        return col
                    case AreaType.FIELD:
                        return Sudoku.getFieldnum(row, col) - 1

            def updateFromCellValues(
                self, cell:SimpleSolver.Cell
            ) -> None:
                self.counter[self.sig_coord(cell.row, cell.col)].update(cell.values)
                # if value is unique for this row/col/field, remember the cell.
                # if is not unique anymore, don't remember any cell
                # dict is sorted by value (not by coordiate) here
                for value in cell.values:
                    if self.counter[self.sig_coord(cell.row, cell.col)][value] == 1:
                        self.cells[self.sig_coord(cell.row, cell.col)][value] = (
                            (cell.row, cell.col)
                        )
                    elif self.counter[self.sig_coord(cell.row, cell.col)][value] == 2:
                        del self.cells[self.sig_coord(cell.row, cell.col)][value]

            def getCellsWithUniqueValues(self) -> List[SimpleSolver.Cell]:
                """Returns a list of Cells (row, col, value)"""
                return [
                    SimpleSolver.Cell(cell_coords[0], cell_coords[1], {value} )
                    for cell in self.cells
                    for value, cell_coords in cell.items()
                ]

        row_wise = Area(AreaType.ROW)
        col_wise = Area(AreaType.COL)
        field_wise = Area(AreaType.FIELD)

        for cell in allowed_values:
            row_wise.updateFromCellValues(cell)
            col_wise.updateFromCellValues(cell)
            field_wise.updateFromCellValues(cell)

        return (
            row_wise.getCellsWithUniqueValues()
            + col_wise.getCellsWithUniqueValues()
            + field_wise.getCellsWithUniqueValues()
        )
