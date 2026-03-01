import pytest

from sudopy import Sudoku

sudoku_str_regular = [
    (
        "123406789" * 9,
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
        ],
    ),
    (
        "103406111" * 4 + "503606100" * 5,
        [
            [1, 0, 3, 4, 0, 6, 1, 1, 1],
            [1, 0, 3, 4, 0, 6, 1, 1, 1],
            [1, 0, 3, 4, 0, 6, 1, 1, 1],
            [1, 0, 3, 4, 0, 6, 1, 1, 1],
            [5, 0, 3, 6, 0, 6, 1, 0, 0],
            [5, 0, 3, 6, 0, 6, 1, 0, 0],
            [5, 0, 3, 6, 0, 6, 1, 0, 0],
            [5, 0, 3, 6, 0, 6, 1, 0, 0],
            [5, 0, 3, 6, 0, 6, 1, 0, 0],
        ],
    ),
]


@pytest.mark.parametrize("generatorStr, refPlayfield", sudoku_str_regular)
def test_fromStr_regular(generatorStr, refPlayfield):

    sudoku = Sudoku.fromStr(generatorStr)
    assert sudoku._playfield == refPlayfield


# TODO:
# - add test for long numbers of digits
# - wrong digits (not 0 ... 9)
