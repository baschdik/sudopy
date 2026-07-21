import os
import pickle
from enum import Enum, auto
from typing import List

from sudoku import Sudoku


class Rating(Enum):
    NO_RATING = auto()
    EASY = auto()
    MEDIUM = auto()
    DIFFICULT = auto()

    def __str__(self):
        return f"{self.name}"


class SudokuMeta:
    def __init__(
        self,
        start: Sudoku,
        *solutions: Sudoku,
        rating: Rating = Rating.NO_RATING,
        **metadaten: str,
    ) -> None:
        self.start = start
        self.solutions: List[Sudoku] = list(solutions)
        self.rating = rating
        self.metadaten = metadaten


class SudokuStore:
    def __init__(self) -> None:
        self.SudokusMeta: List[SudokuMeta] = list()

    def __str__(self) -> str:
        nice_str = "Stored:\n"
        for no, meta in enumerate(self.SudokusMeta):
            nice_str += f"{no}:\n{meta.start}\n"
        return nice_str

    def saveToFile(self, filename: str | os.PathLike) -> None:
        with open(filename, "wb") as f:
            pickle.dump(self.SudokusMeta, f)

    def loadFromFile(self, filename: str | os.PathLike) -> None:
        with open(filename, "rb") as f:
            self.SudokusMeta = pickle.load(f)

    def add(self, *sudoku: SudokuMeta) -> None:
        self.SudokusMeta.extend(sudoku)
