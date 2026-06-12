from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Collection

from sudoku import Sudoku


class SudokuChecker(ABC):
    @abstractmethod
    def isRegular(self, sudoku: Sudoku) -> bool:
        pass

    @abstractmethod
    def isSolved(self, sudoku: Sudoku) -> bool:
        pass


class SimpleChecker(SudokuChecker):
    def isRegular(self, sudoku: Sudoku) -> bool:
        for row in sudoku.getPlayfield():
            if not SimpleChecker._check_regular_digits(row):
                return False
        for col in zip(*sudoku.getPlayfield()):
            if not SimpleChecker._check_regular_digits(col):
                return False
        for i in range(1, 10):  # all 9 fields in Sudoko playfield
            if not SimpleChecker._check_regular_digits(sudoku.getField(i)):
                return False
        return True

    @staticmethod
    def _check_regular_digits(input: Collection[int]) -> bool:
        counter = Counter(input)
        if counter.total() != 9:
            return False
        return all(v <= 1 for k, v in counter.items() if k != 0)

    def isSolved(self, sudoku: Sudoku) -> bool:
        for row in sudoku.getPlayfield():
            if not SimpleChecker._check_solved_digits(row):
                return False
        for col in zip(*sudoku.getPlayfield()):
            if not SimpleChecker._check_solved_digits(col):
                return False
        for i in range(1, 10):  # all 9 fields in Sudoko playfield
            if not SimpleChecker._check_solved_digits(sudoku.getField(i)):
                return False
        return True

    @staticmethod
    def _check_solved_digits(input: Collection[int]) -> bool:
        digits = set(input)
        if digits == set([1, 2, 3, 4, 5, 6, 7, 8, 9]):
            return True
        return False
