from collections import Counter
from collections.abc import Collection

from sudoku import Sudoku


def check_solved(input: Sudoku) -> bool:
    for row in input.getPlayfield():
        if not check_solved_digits(row):
            return False
    for col in zip(*input.getPlayfield()):
        if not check_solved_digits(col):
            return False
    for i in range(1, 10):  # all 3 fields in Sudoko playfield
        if not check_solved_digits(input.getField(i)):
            return False
    return True


def check_solved_digits(input: Collection[int]) -> bool:
    digits = set(input)
    if digits == set([1, 2, 3, 4, 5, 6, 7, 8, 9]):
        return True
    return False


def check_regular(input: Sudoku) -> bool:
    for row in input.getPlayfield():
        if not check_regular_digits(row):
            return False
    for col in zip(*input.getPlayfield()):
        if not check_regular_digits(col):
            return False
    for i in range(1, 10):  # all 3 fields in Sudoko playfield
        if not check_regular_digits(input.getField(i)):
            return False
    return True


def check_regular_digits(input: Collection[int]) -> bool:
    counter = Counter(input)
    if counter.total() != 9:
        return False
    return all(v <= 1 for k, v in counter.items() if k != 0)
