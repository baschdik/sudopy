from simpleChecker import SudokuChecker
from sudoku import Sudoku

# TODO:
# * Tests
# * Docs


class Game:
    """Game handles the logik for one round of Sudoku"""

    def __init__(self, sudoku: Sudoku, checker: SudokuChecker) -> None:
        self.sudoku = sudoku
        self.checker = checker

    def getCellValue(self, row: int, col: int) -> int:
        return self.sudoku.getCellValue(row, col)

    def modifyCell(self, row: int, col: int, newValue: int) -> int:
        """Modifies one Cell of the Sudoku-Playfield

        Modifikation is only done if the updated Playfield is still regular
        """
        oldValue = self.sudoku.getCellValue(row, col)
        self.sudoku.modifyCell(row, col, newValue)
        if not self.checker.isRegular(self.sudoku):
            self.sudoku.modifyCell(row, col, oldValue)
            return oldValue
        return newValue

    def isSolved(self) -> bool:
        return self.checker.isSolved(self.sudoku)
