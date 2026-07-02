from game import Game
from simpleChecker import SimpleChecker
from sudoku import Sudoku
from tui_app import SudopyTerminalInterface


def sudopy():
    sudoko = Sudoku.fromStr(
        "001000800902408705080000040200103009010506080500209006070000030103804207004000100"
    )
    print(sudoko)

    checker = SimpleChecker()
    print(checker.isSolved(sudoko))

    game = Game(sudoko, checker)

    app = SudopyTerminalInterface(game)
    app.run()


if __name__ == "__main__":
    sudopy()
