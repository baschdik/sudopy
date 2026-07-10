from game import Game
from simpleChecker import SimpleChecker
from simpleSolver import SimpleSolver
from sudoku import Sudoku
from tui_app import SudopyTerminalInterface


def sudopy():
    sudoko = Sudoku.fromStr(
        "009506200030070090500000007800050006040802050900010002400000009010040020006301400"  # Schwer von Evgeniia
        #"060000030000976102109200050030000090200609005090010070050007900003865000070000040"
    )

    print("Input:\n", sudoko)

    checker = SimpleChecker()
    # print(checker.isSolved(sudoko))

    solver = SimpleSolver(sudoko, checker)

    print("Result is solved ",solver.solve())
    print("Result:\n", solver.getSudoku())
    print(solver.getSudoku().__repr__())

    # game = Game(sudoko, checker)

    # app = SudopyTerminalInterface(game)
    # app.run()


if __name__ == "__main__":
    sudopy()
