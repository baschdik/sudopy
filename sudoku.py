from dataclasses import dataclass
from typing import Self


@dataclass
class Sudoku:
    """Holds the Sudoku data"""

    _playfield: list[list[int]]
    ROWS = 9
    COLS = 9
    FIELDS = 9

    class Cell:
        def __init__(self, row: int, col: int, value: int | None) -> None:
            if not 0 <= row <= 8:
                raise ValueError("Input row outside 0...8.")
            if not 0 <= col <= 8:
                raise ValueError("Input col outside 0...8.")
            if value and not 0 <= value <= 9:
                raise ValueError("Input value outside 0...9.")
            self.row = row
            self.col = col
            self.value = value

        def __hash__(self) -> int:
            return hash((self.row, self.col))

        def __lt__(self, other):
            if self.row == other.row:
                return self.col < other.col
            return self.row < other.row

        def __str__(self) -> str:
            return f"({self.row}, {self.col}): {self.value}"

    @classmethod
    def fromStr(cls, input: str) -> Self:
        """Creates Sudoku instance from single input string

        Str can contain digits from 0 ... 9.
        One digit is one position in the Soduko, interpreted as complete first row
        (from left to right) then next row.
        0 represents empty / unsolved position
        """
        if not isinstance(input, str):
            raise TypeError(
                f"Input has type {type(input)} but should have type String."
            )
        input = input.strip()
        if len(input) != cls.ROWS * cls.COLS:
            raise ValueError(
                f"Input string has {len(input)} digits but should have {cls.ROWS * cls.COLS}."
            )
        if not input.isdecimal():
            raise ValueError("Input String contains characters outside of 0123456789.")

        input_list = list(input)
        playfield = [[0 for _ in range(cls.COLS)] for _ in range(cls.ROWS)]
        for row in range(cls.ROWS):
            for col in range(cls.COLS):
                playfield[row][col] = int(input_list.pop(0))

        return cls(playfield)

    def __str__(self) -> str:
        output: str = ""
        for row in range(self.ROWS):
            if row > 0 and row % 3 == 0:
                output += "-" * (self.COLS * 2 + 5) + "\n"
            for col in range(self.COLS):
                if col > 0 and col % 3 == 0:
                    output += " |"
                output += " " + str(self._playfield[row][col]).replace("0", " ")
            output += "\n"

        return output

    def __repr__(self) -> str:
        playfield_as_string = ""
        for row in self._playfield:
            for val in row:
                playfield_as_string += str(val)

        return f"Sudoku: {playfield_as_string}"

    def getPlayfield(self) -> list[list[int]]:
        return self._playfield

    def getField(
        self, numberOfField: int = 0, cellInField: Cell | None = None
    ) -> list[int]:
        # TODO: test additonal input vales
        # TODO: Update FieldsNo from 1...9 to 0...8

        if isinstance(cellInField, self.Cell):
            numberOfField = self.getFieldnum(cellInField)

        if not 1 <= numberOfField <= 9:
            raise ValueError("Field Number outside of 1...9.")
        firstRow = (numberOfField - 1) // 3 * 3
        firstCol = ((numberOfField - 1) * 3) % 9
        fieldlist = list()
        for row in range(firstRow, firstRow + 2 + 1):
            for col in range(firstCol, firstCol + 2 + 1):
                fieldlist.append(self._playfield[row][col])
        return fieldlist

    @staticmethod
    # TODO: Test
    def getFieldnum(cell: Cell) -> int:
        return (cell.row // 3) * 3 + (cell.col // 3) % 3 + 1

    def getCellValue(self, cell: Cell) -> int:
        return self._playfield[cell.row][cell.col]

    def getRow(self, row) -> list[int]:
        return self._playfield[row]

    def getCol(self, col) -> list[int]:
        inverted = list(zip(*self._playfield))
        return list(inverted[col])

    def modifyCell(self, cell: Cell):
        if cell.value is None:
            raise ValueError("Can't modifiy playfield with None value.")
        self._playfield[cell.row][cell.col] = cell.value
