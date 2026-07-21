from serdeSudoku import Rating, SudokuMeta, SudokuStore
from sudoku import Sudoku

sudoku_test = [
    Sudoku.fromStr(
        "001000800902408705080000040200103009010506080500209006070000030103804207004000100"
    ),
    Sudoku.fromStr(
        "451697823932418765786352941268143579319576482547289316875921634193864257624735198"
    ),
    Sudoku.fromStr(
        "006304800320010400901600005800001060000000000060900004200005603003080049009406500"
    ),
    Sudoku.fromStr(
        "576324891328519476941678235835241967497863152162957384284795613653182749719436528"
    ),
    Sudoku.fromStr(
        "073100200600000070000906308050010900000804000006030040205401000080000001009002860"
    ),
    Sudoku.fromStr(
        "973148256618523479542976318354617982721894635896235147265481793487369521139752864"
    ),
    Sudoku.fromStr(
        "001709800003080700740050013020000060900305008030000070650090034004020600009601200"
    ),
    Sudoku.fromStr(
        "561739842293184756748256913425978361917365428836412579652897134184523697379641285"
    ),
    Sudoku.fromStr(
        "009506200030070090500000007800050006040802050900010002400000009010040020006301400"
    ),
    Sudoku.fromStr(
        "179536284634278591582194367823459716741862953965713842458627139317945628296381475"
    ),
]


def test_SudokuMeta() -> None:
    m1 = SudokuMeta(sudoku_test[0], rating=Rating.EASY)
    m2 = SudokuMeta(sudoku_test[0], sudoku_test[1], author="Sebastian")
    m3 = SudokuMeta(sudoku_test[0], sudoku_test[2], sudoku_test[3])

    assert m1.start == sudoku_test[0]
    assert not m1.solutions
    assert m1.rating == Rating.EASY
    assert not m1.metadaten

    assert m2.start == sudoku_test[0]
    assert m2.solutions == [sudoku_test[1]]
    assert m2.metadaten == {"author": "Sebastian"}
    assert m2.rating == Rating.NO_RATING

    assert m3.start == sudoku_test[0]
    assert m3.solutions == [sudoku_test[2], sudoku_test[3]]
    assert m3.rating == Rating.NO_RATING
    assert not m3.metadaten


def test_SudokuStore():
    m1 = SudokuMeta(sudoku_test[0])
    m2 = SudokuMeta(sudoku_test[0], sudoku_test[1], author="Sebastian")
    m3 = SudokuMeta(sudoku_test[0], sudoku_test[2], sudoku_test[3])

    s1 = SudokuStore()
    s1.add(m1)
    assert s1.SudokusMeta == [m1]
    s1.add(m2, m3)
    assert s1.SudokusMeta == [m1, m2, m3]


def test_SudokuStore_str():
    m1 = SudokuMeta(sudoku_test[0])
    m2 = SudokuMeta(sudoku_test[0], sudoku_test[1], author="Sebastian")

    s1 = SudokuStore()
    s1.add(m1, m2)
    assert (
        s1.__str__()
        == "Stored:\n0:\n     1 |       | 8    \n 9   2 | 4   8 | 7   5\n   8   |       |   4  \n-----------------------\n 2     | 1   3 |     9\n   1   | 5   6 |   8  \n 5     | 2   9 |     6\n-----------------------\n   7   |       |   3  \n 1   3 | 8   4 | 2   7\n     4 |       | 1    \n\n1:\n     1 |       | 8    \n 9   2 | 4   8 | 7   5\n   8   |       |   4  \n-----------------------\n 2     | 1   3 |     9\n   1   | 5   6 |   8  \n 5     | 2   9 |     6\n-----------------------\n   7   |       |   3  \n 1   3 | 8   4 | 2   7\n     4 |       | 1    \n\n"
    )


def test_SudokuStore_saveload(tmp_path):
    pkl_file = tmp_path / "test.pkl"

    m1 = SudokuMeta(sudoku_test[0], rating=Rating.DIFFICULT)
    m2 = SudokuMeta(
        sudoku_test[0], sudoku_test[1], rating=Rating.EASY, author="Sebastian"
    )
    m3 = SudokuMeta(sudoku_test[0], sudoku_test[2], sudoku_test[3])

    s_save = SudokuStore()
    s_save.add(m1, m2, m3)
    s_save.saveToFile(pkl_file)

    s_load = SudokuStore()
    s_load.loadFromFile(pkl_file)

    assert len(s_load.SudokusMeta) == len(s_save.SudokusMeta)
