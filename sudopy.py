from sudoku import Sudoku


def sudopy():
    sudoko = Sudoku.fromStr(
        "576324891328519476941678235835241967497863152162957384284795613653182749719436528"
    )
    print(sudoko)


if __name__ == "__main__":
    sudopy()
