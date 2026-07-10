"""Test solver functionality

from simpleSolver.py"""
# TODO: build solver fixture
# TODO: build sudoku fixture

import pytest

from simpleChecker import SimpleChecker, SudokuChecker
from simpleSolver import SimpleSolver
from sudoku import Sudoku


class CheckerMock_isRegular(SudokuChecker):
    def isRegular(self, sudoku: Sudoku) -> bool:
        return True

    def isSolved(self, sudoku: Sudoku) -> bool:
        return False


class CheckerMock_notRegular(SudokuChecker):
    def isRegular(self, sudoku: Sudoku) -> bool:
        return False

    def isSolved(self, sudoku: Sudoku) -> bool:
        return False


sudoku_test = [
    (
        Sudoku.fromStr(
            "001000800902408705080000040200103009010506080500209006070000030103804207004000100"
        ),
        Sudoku.fromStr(
            "451697823932418765786352941268143579319576482547289316875921634193864257624735198"
        ),
    ),
    (
        Sudoku.fromStr(
            "006304800320010400901600005800001060000000000060900004200005603003080049009406500"
        ),
        Sudoku.fromStr(
            "576324891328519476941678235835241967497863152162957384284795613653182749719436528"
        ),
    ),
    (
        Sudoku.fromStr(
            "073100200600000070000906308050010900000804000006030040205401000080000001009002860"
        ),
        Sudoku.fromStr(
            "973148256618523479542976318354617982721894635896235147265481793487369521139752864"
        ),
    ),
    (
        Sudoku.fromStr(
            "001709800003080700740050013020000060900305008030000070650090034004020600009601200"
        ),
        Sudoku.fromStr(
            "561739842293184756748256913425978361917365428836412579652897134184523697379641285"
        ),
    ),
    (
        Sudoku.fromStr(
            "009506200030070090500000007800050006040802050900010002400000009010040020006301400"
        ),
        Sudoku.fromStr(
            "179536284634278591582194367823459716741862953965713842458627139317945628296381475"
        ),
    ),
]


@pytest.mark.parametrize("sudoku_in, sudoku_solution", sudoku_test)
def test_init_isRegular(sudoku_in: Sudoku, sudoku_solution: Sudoku):
    solver = SimpleSolver(sudoku_in, CheckerMock_isRegular())
    assert solver.sudoku == sudoku_in
    assert not solver.sudokuIsSolved


@pytest.mark.parametrize("sudoku_in, sudoku_solution", sudoku_test)
def test_init_notRegular(sudoku_in: Sudoku, sudoku_solution: Sudoku):
    with pytest.raises(ValueError):
        _ = SimpleSolver(sudoku_in, CheckerMock_notRegular())


@pytest.mark.parametrize("sudoku_in, sudoku_solution", sudoku_test)
def test_solve(sudoku_in: Sudoku, sudoku_solution: Sudoku):
    solver = SimpleSolver(sudoku_in, SimpleChecker())
    solver.solve()
    assert solver.getSudoku().getPlayfield() == sudoku_solution.getPlayfield()


def test_solve_noSolution():
    sudoku_noSolution = Sudoku.fromStr("060000030000976102109200050030000090200609005090010070050007900003865000070000040")
    solver = SimpleSolver(sudoku_noSolution, SimpleChecker())
    assert not solver.solve()


#@pytest.mark.parametrize("sudoku_in, sudoku_solution", sudoku_test)
# def test_nextStep(sudoku_in: Sudoku, sudoku_solution: Sudoku):
#     solver = SimpleSolver(sudoku_in, SimpleChecker())

#     unsolved_cells = {
#         (row, col): sudoku_solution.getCellValue(row, col)
#         for row in range(sudoku_in.ROWS)
#         for col in range(sudoku_in.COLS)
#         if sudoku_in.getCellValue(row, col) == 0
#     }

#     for testval, row, col in solver.nextStep():
#         assert unsolved_cells.pop((row, col)) == testval
#     assert not unsolved_cells


def test_getPossibleValues():
    solver = SimpleSolver(Sudoku.fromStr("001709800003080700740050013020000060900305008030000070650090034004020600009601200"), CheckerMock_isRegular())
    assert solver.getPossibleValues([5,3,1,0]) == set([2,4,6,7,8,9])
