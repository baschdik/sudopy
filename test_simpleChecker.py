"""Test checker functionality

from checker.py"""

import pytest

from simpleChecker import SimpleChecker
from sudoku import Sudoku

sudoku_not_solved = [
    (
        [
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9],
        ]
    ),
]

sudoku_solved = [
    (
        [
            [5, 7, 6, 3, 2, 4, 8, 9, 1],
            [3, 2, 8, 5, 1, 9, 4, 7, 6],
            [9, 4, 1, 6, 7, 8, 2, 3, 5],
            [8, 3, 5, 2, 4, 1, 9, 6, 7],
            [4, 9, 7, 8, 6, 3, 1, 5, 2],
            [1, 6, 2, 9, 5, 7, 3, 8, 4],
            [2, 8, 4, 7, 9, 5, 6, 1, 3],
            [6, 5, 3, 1, 8, 2, 7, 4, 9],
            [7, 1, 9, 4, 3, 6, 5, 2, 8],
        ]
    ),
]


@pytest.mark.parametrize("playfield", sudoku_solved)
def test_check_solved_isSolved(playfield):
    sudoku = Sudoku(playfield)
    checker = SimpleChecker()
    assert checker.isSolved(sudoku)


@pytest.mark.parametrize("playfield", sudoku_not_solved)
def test_check_solved_isNotSolved(playfield):
    sudoku = Sudoku(playfield)
    checker = SimpleChecker()
    assert checker.isSolved(sudoku) is False


digits_solved = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 3, 5, 7, 9, 2, 4, 6, 8],
    [9, 4, 6, 3, 7, 2, 8, 1, 5],
]


@pytest.mark.parametrize("digits", digits_solved)
def test_check_solved_digits_isSolved(digits):
    assert SimpleChecker._check_solved_digits(digits)


digits_notSolved = [
    [1, 2, 3, 4, 0, 6, 7, 8, 9],
    [1, 3, 5, 7, 9, 5, 4, 6, 8],
    [9, 4, 0, 3, 7, 2, 8, 3, 5],
]


@pytest.mark.parametrize("digits", digits_notSolved)
def test_check_solved_digits_notSolved(digits):
    assert SimpleChecker._check_solved_digits(digits) is False


sudoku_not_regular = [
    (
        [
            [5, 7, 6, 3, 2, 4, 8, 9, 1],
            [3, 0, 8, 5, 1, 9, 4, 7, 6],
            [9, 4, 0, 6, 7, 8, 2, 0, 5],
            [8, 3, 5, 2, 9, 0, 9, 6, 7],
            [4, 9, 7, 0, 0, 0, 0, 5, 2],
            [1, 6, 2, 3, 5, 7, 3, 8, 4],
            [2, 8, 4, 0, 9, 0, 5, 1, 3],
            [6, 5, 3, 1, 8, 2, 7, 4, 9],
            [7, 1, 9, 4, 3, 6, 5, 2, 8],
        ]
    ),
]

sudoku_regular = [
    (
        [
            [5, 7, 6, 3, 2, 4, 8, 9, 1],
            [3, 0, 8, 5, 1, 9, 4, 7, 6],
            [9, 4, 0, 6, 7, 8, 2, 0, 5],
            [8, 3, 5, 2, 4, 0, 9, 6, 7],
            [4, 9, 7, 0, 0, 0, 0, 5, 2],
            [1, 6, 2, 9, 5, 7, 3, 8, 4],
            [2, 8, 4, 0, 9, 5, 6, 1, 3],
            [6, 5, 3, 1, 8, 2, 7, 4, 9],
            [7, 1, 9, 4, 3, 6, 5, 2, 8],
        ]
    ),
]


@pytest.mark.parametrize("playfield", sudoku_regular)
def test_check_regular_isRegular(playfield):
    sudoku = Sudoku(playfield)
    checker = SimpleChecker()
    assert checker.isRegular(sudoku)


@pytest.mark.parametrize("playfield", sudoku_not_regular)
def test_check_regular_notRegular(playfield):
    sudoku = Sudoku(playfield)
    checker = SimpleChecker()
    assert checker.isRegular(sudoku) is False


digits_regular = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, 3, 0, 5, 6, 7, 8, 9],
    [1, 3, 5, 7, 9, 0, 0, 6, 8],
    [0, 4, 6, 0, 7, 2, 8, 1, 0],
]


@pytest.mark.parametrize("digits", digits_regular)
def test_check_regular_digits_isRegular(digits):
    assert SimpleChecker._check_regular_digits(digits)


digits_notRegular = [
    [1, 2, 3, 4, 4, 6, 7, 8, 9],
    [1, 0, 5, 7, 9, 5, 4, 6, 8],
    [9, 4, 0, 3, 3, 2, 8, 3, 0],
]


@pytest.mark.parametrize("digits", digits_notRegular)
def test_check_regular_digits_notRegular(digits):
    assert SimpleChecker._check_regular_digits(digits) is False
