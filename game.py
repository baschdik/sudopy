from enum import Enum, auto
from typing import Dict, Tuple, Type

from simpleChecker import SudokuChecker
from simpleSolver import SudokuSolver
from sudoku import Sudoku

# TODO:
# * Tests
# * Docs


class Game:
    """Game handles the logik for one round of Sudoku"""

    class CellType(Enum):
        EMPTY = auto()
        START = auto()
        CORRECT = auto()
        WRONG = auto()

        def __repr__(self) -> str:
            return f"{self.name}"

    def __init__(
        self, sudoku: Sudoku, Checker: Type[SudokuChecker], Solver: Type[SudokuSolver]
    ) -> None:
        self.sudoku = sudoku
        self.checker = Checker()
        self.solver = Solver(self.sudoku, self.checker)

        if not self.solver.solve():
            raise ValueError("Given Sudoku has no solution and can't be played!")
        self.solution = self.solver.getSudoku()
        self._initCellTypes()

    def _initCellTypes(self):
        self.cellTypes: Dict[Tuple[int, int], Game.CellType] = dict()
        for row in range(self.sudoku.ROWS):
            for col in range(self.sudoku.COLS):
                if self.sudoku.getCellValue(row, col) == 0:
                    self.cellTypes[(row, col)] = self.CellType.EMPTY
                else:
                    self.cellTypes[(row, col)] = self.CellType.START

    def getCell(self, row: int, col: int) -> Tuple[int, CellType]:
        return self.sudoku.getCellValue(row, col), self.cellTypes[(row, col)]

    def modifyCell(
        self, row: int, col: int, newValue: int
    ) -> Tuple[int, CellType, bool]:
        """Modifies one Cell of the Sudoku-Playfield

        Modifikation is only done if the cell is not type START
        Modifies CellType as well

        Returns current cell value, current cell type and if Sudoku is solved
        """
        if self.cellTypes[(row, col)] == Game.CellType.START:
            return self.sudoku.getCellValue(row, col), Game.CellType.START, False

        self.sudoku.modifyCell(row, col, newValue)
        self._updateCellType(row, col, newValue)
        return newValue, self.cellTypes[(row, col)], self.checker.isSolved(self.sudoku)

    def _updateCellType(self, row: int, col: int, newValue: int) -> None:
        if self.cellTypes[(row, col)] == Game.CellType.START:
            return
        if newValue == 0:
            self.cellTypes[(row, col)] = Game.CellType.EMPTY
            return
        if self.solution.getCellValue(row, col) == newValue:
            self.cellTypes[(row, col)] = Game.CellType.CORRECT
            return
        self.cellTypes[(row, col)] = Game.CellType.WRONG

    def isSolved(self) -> bool:
        return self.checker.isSolved(self.sudoku)


if __name__ == "__main__":
    from simpleChecker import SimpleChecker
    from simpleSolver import SimpleSolver

    sudoku = Sudoku.fromStr(
        "001709800003080700740050013020000060900305008030000070650090034004020600009601200"
    )

    game = Game(sudoku, SimpleChecker, SimpleSolver)
    print(game.sudoku, game.solution, game.cellTypes)

    print(game.modifyCell(0, 0, 4))
    print(game.modifyCell(0, 0, 5))
    print(game.modifyCell(0, 2, 7))
    print(game.modifyCell(6, 3, 0))
