from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Collection
from copy import deepcopy
from enum import Enum, auto
from typing import Dict, List, Set, Tuple

from simpleChecker import SudokuChecker
from sudoku import Sudoku


class SudokuSolver(ABC):
    def __init__(self, sudoku: Sudoku, checker: SudokuChecker) -> None:
        self.sudoku: Sudoku = deepcopy(sudoku)
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


class SimpleSolver(SudokuSolver):
    def __init__(self, sudoku: Sudoku, checker: SudokuChecker) -> None:
        super().__init__(sudoku, checker)

    def getSudoku(self) -> Sudoku:
        return super().getSudoku()

    def solve(self):

        sudoku_intermediate = deepcopy(self.sudoku)
        sudoku_intermediate = self.solveBacktracking(sudoku_intermediate)
        if sudoku_intermediate is None:
            return False
        else:
            self.sudoku = sudoku_intermediate

        return self.checker.isSolved(self.sudoku)

    class CellSet(Sudoku.Cell):
        def __init__(self, row: int, col: int, values: Set[int]) -> None:
            super().__init__(row, col, None)
            self.values = values

        def __lt__(self, other):
            return len(self.values) < len(other.values)

        def __str__(self) -> str:
            return f"({self.row}, {self.col}): {self.values}"

    def solveBacktracking(self, sudoku: Sudoku) -> Sudoku | None:
        self.solveRulebased(sudoku)
        if self.checker.isSolved(sudoku):
            return sudoku

        cellsWPossibleValues = sorted(self.getPossibleValuesForEmptyCells(sudoku))
        if not cellsWPossibleValues:
            return None

        next_Cell = cellsWPossibleValues[0]
        for value in next_Cell.values:
            # print("next try: ", next_Cell, value) # DEBUG
            possible_solution = deepcopy(sudoku)
            next_Cell.value = value
            possible_solution.modifyCell(next_Cell)
            possible_solution = self.solveBacktracking(possible_solution)
            if not possible_solution:
                continue
            if self.checker.isSolved(possible_solution):
                return possible_solution

        return None

    def solveRulebased(self, sudoku: Sudoku):
        sudokuModified = True
        # iterationCounter = 0  # DEBUG ?

        while sudokuModified:
            sudokuModified = False
            # iterationCounter += 1  # DEBUG ?

            allowed_values = self.getPossibleValuesForEmptyCells(sudoku)
            sudokuModified = self.updateSudokuForCellsWithOnlyOnePossibleValue(
                sudoku, allowed_values
            )
            if sudokuModified:
                continue

            sudokuModified = self.updateSudokuWhenValueIsOnlyOnceInAnArea(
                sudoku, allowed_values
            )

        # print("iterations:", iterationCounter)  # DEBUG ?

    def getPossibleValuesForEmptyCells(self, sudoku: Sudoku) -> List[CellSet]:
        """Returns all currently empty (0) cells with all possible values"""
        return [
            self.getPossibleValuesForCell(sudoku, self.CellSet(row, col, set()))
            for row in range(Sudoku.ROWS)
            for col in range(Sudoku.COLS)
            if sudoku.getCellValue(Sudoku.Cell(row, col, None)) == 0
        ]

    def getPossibleValuesForCell(self, sudoku: Sudoku, cell: CellSet) -> CellSet:
        return self.CellSet(
            cell.row,
            cell.col,
            self.getPossibleValues(sudoku.getRow(cell.row))
            & self.getPossibleValues(sudoku.getCol(cell.col))
            & self.getPossibleValues(sudoku.getField(cellInField=cell)),
        )

    @staticmethod
    def getPossibleValues(input: Collection[int]) -> Set[int]:
        """Returns the values of 1...9 which are not used yet"""
        return {1, 2, 3, 4, 5, 6, 7, 8, 9} - set(input)

    def updateSudokuForCellsWithOnlyOnePossibleValue(
        self, sudoku: Sudoku, possibleCellValues: List[CellSet]
    ) -> bool:
        """If a cell has only one possible Value, it is final and sudoku can be modified

        Returns True if modification was done at least once
        """
        modificationDone = False
        for cell in possibleCellValues:
            if len(cell.values) == 1:
                cell.value = cell.values.pop()
                sudoku.modifyCell(cell)
                modificationDone = True

        return modificationDone

    def updateSudokuWhenValueIsOnlyOnceInAnArea(
        self, sudoku: Sudoku, allowed_values: List[CellSet]
    ) -> bool:
        """If in an area a specific value is only possible at on cell, this cell is final.

        Area here is either a row, a col or a field.
        Returns True when an at least one update was done.
        """

        cell_list = self.getCellsWithUniqueValue(allowed_values)
        if not cell_list:
            return False

        for cell in cell_list:
            cell.value = cell.values.pop()
            sudoku.modifyCell(cell)
        return True

    @staticmethod
    def getCellsWithUniqueValue(
        allowed_values: List[CellSet],
    ) -> List[CellSet]:
        """Checks if a cell is the only possibility for a value in an area."""

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
                self.cells: List[Dict[int, Tuple[int, int]]] = [
                    dict() for _ in range(self.area_length)
                ]

            def sig_coord(self, row, col) -> int:
                """Returns significant coordinate per AreaType"""
                match self.type:
                    case AreaType.ROW:
                        return row
                    case AreaType.COL:
                        return col
                    case AreaType.FIELD:
                        return Sudoku.getFieldnum(Sudoku.Cell(row, col, None)) - 1

            def updateFromCellValues(self, cell: SimpleSolver.CellSet) -> None:
                self.counter[self.sig_coord(cell.row, cell.col)].update(cell.values)
                # if value is unique for this row/col/field, remember the cell.
                # if is not unique anymore, don't remember any cell
                # dict is sorted by value (not by coordiate) here
                for value in cell.values:
                    if self.counter[self.sig_coord(cell.row, cell.col)][value] == 1:
                        self.cells[self.sig_coord(cell.row, cell.col)][value] = (
                            cell.row,
                            cell.col,
                        )
                    elif self.counter[self.sig_coord(cell.row, cell.col)][value] == 2:
                        del self.cells[self.sig_coord(cell.row, cell.col)][value]

            def getCellsWithUniqueValues(self) -> List[SimpleSolver.CellSet]:
                return [
                    SimpleSolver.CellSet(cell_coords[0], cell_coords[1], {value})
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
