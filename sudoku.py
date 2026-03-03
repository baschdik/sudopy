from dataclasses import dataclass
from typing import Self


@dataclass
class Sudoku:
    """Holds the Sudoku data"""

    _playfield: list[list[int]]
    ROWS = 9
    COLS = 9

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
        if len(input) != 81:
            raise ValueError(
                f"Input String has {len(input)} Digits but should have 81."
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

    def getPlayfield(self) -> list[list[int]]:
        return self._playfield
