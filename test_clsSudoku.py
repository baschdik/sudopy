"""Test cls Sudoku

from sudopy.py"""

import pytest

from sudoku import Sudoku

sudoku_regular = [
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
    (
        " " + "123406789" * 9,
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
        "123406789" * 9 + "   ",
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
]


@pytest.mark.parametrize("generatorStr, refPlayfield", sudoku_str_regular)
def test_createPlayfield_regular(generatorStr, refPlayfield):

    sudoku = Sudoku.fromStr(generatorStr)
    assert sudoku.getPlayfield() == refPlayfield


sudoku_input_length = [
    "",
    "1",
    "12345" * 16,
    "99882" * 16 + "03",
    "123456789" * 8,
    "123000789" * 10,
]


@pytest.mark.parametrize("generatorStr", sudoku_input_length)
def test_fromStr_wrongLengthofInput(generatorStr):

    with pytest.raises(ValueError):
        _ = Sudoku.fromStr(generatorStr)


sudoku_input_type = [
    None,
    1,
    float(12345),
    [1, 2, 3, 4, 5, 0, 0, 0, 9] * 9,
]


@pytest.mark.parametrize("generatorStr", sudoku_input_type)
def test_fromStr_wrongTypeOfInput(generatorStr):

    with pytest.raises(TypeError):
        _ = Sudoku.fromStr(generatorStr)


sudoku_input_wrongDigit = [
    "1234a6789" * 9,
    "1234 6789" * 9,
    "1234.6709" * 9,
    "1ll446489" * 9,
    "111446OO9" * 9,
]


@pytest.mark.parametrize("generatorStr", sudoku_input_wrongDigit)
def test_fromStr_wrongDigitInInput(generatorStr):

    with pytest.raises(ValueError):
        _ = Sudoku.fromStr(generatorStr)


@pytest.mark.parametrize("refPlayfield", sudoku_regular)
def test_getField_regular(refPlayfield):
    # Tests only if the field, which comes out, contains 9 digits
    sudoku = Sudoku(refPlayfield)
    for i in range(1, 10):
        assert len(sudoku.getField(i)) == 9


@pytest.mark.parametrize("refPlayfield", sudoku_regular)
def test_getField_wrongValue(refPlayfield):
    sudoku = Sudoku(refPlayfield)
    testValues = [-5, 0, 10, 15, 27]
    for i in testValues:
        with pytest.raises(ValueError):
            sudoku.getField(i)
