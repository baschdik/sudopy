from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Iterator, Tuple

from simpleChecker import SudokuChecker
from sudoku import Sudoku


class SudokuSolver(ABC):
    def __init__(self, sudoku: Sudoku, checker: SudokuChecker) -> None:
        self.sudoku = deepcopy(sudoku)
        if not checker.isRegular(self.sudoku):
            raise ValueError(
                "Sudoku is not regular. Non-regular sudokus can't be solved."
            )
        self.sudokuIsSolved = checker.isSolved(self.sudoku)

    @abstractmethod
    def solve(self) -> Sudoku:
        pass

    @abstractmethod
    def nextStep(self) -> Iterator[tuple[int, int, int]]:
        """Returns next step for solving.

        returns value, row, col of cell"""
        pass


class SimpleSolver(SudokuSolver):
    def solve(self):
        # TODO!
        sudoku = Sudoku.fromStr(
            "451697823983418765786352941268143579319576482547289316875921634193864257624735198"
        )
        return sudoku

    def nextStep(self):
        # TODO!
        yield 0, 0, 0
