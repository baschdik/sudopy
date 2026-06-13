"""Test cls Sudoku

from sudopy.py"""

import pytest

from sudoku import Sudoku

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

sudoku_str_works = [
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


@pytest.mark.parametrize("generatorStr, refPlayfield", sudoku_str_works)
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


@pytest.mark.parametrize("refPlayfield", sudoku_regular)
def test_modify_correct(refPlayfield):
    sudoku = Sudoku(refPlayfield)
    for i in range(0, 10):
        sudoku.modify(i % 9, i * 2 % 9, i)
        assert sudoku._playfield[i % 9][i * 2 % 9] == i


@pytest.mark.parametrize("refPlayfield", sudoku_regular)
def test_modify_error(refPlayfield):
    sudoku = Sudoku(refPlayfield)
    testValues = [-5, -1, 10, 15]
    for i in testValues:
        print(i)
        with pytest.raises(ValueError):
            sudoku.modify(1, 2, i)
