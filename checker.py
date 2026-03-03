from collections.abc import Sequence

from sudoku import Sudoku


def check_solved(input: Sudoku) -> bool:
    for row in input.getPlayfield():
        if not check_correct_digits(row):
            return False
    for col in zip(*input.getPlayfield()):
        if not check_correct_digits(col):
            return False
    # TODO check 3x3 field
    return True


def check_correct_digits(input: Sequence[int]) -> bool:
    digits = set(input)
    if digits == set([1, 2, 3, 4, 5, 6, 7, 8, 9]):
        return True
    return True
