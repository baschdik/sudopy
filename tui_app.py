from typing import Tuple

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import Footer, Header, Input, Label

from game import Game

# TODO: remove debug elements


class Cell(Input):
    """Single Element of Sudoko Playfield (View Component)

    If selected, will send key 0-9 as CellUpdate message up.
    """

    def __init__(self, value: str, row: int, col: int) -> None:
        super().__init__(
            value,
            type="integer",
            compact=True,
            max_length=1,
            restrict=r"[0-9]",
            id="c" + str(row) + str(col),
        )

    def on_key(self, event: events.Key) -> None:
        if event.key in "0123456789":
            event.stop()
            self.post_message(self.CellUpdate(self.id, self.value, event.key))  # type: ignore

    class CellUpdate(Message):
        """Sent updated value of the Cell when user try to changed it"""

        def __init__(self, cellID: str, oldValue: str, newValue: str) -> None:
            super().__init__()
            self.cellID = cellID
            self.newValue = newValue
            self.oldValue = oldValue


class Playfield(Container):
    """The Sudoku Playfield (View + Controller Component)."""

    def __init__(self, sudoku: Game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sudoku = sudoku

    def compose(self) -> ComposeResult:
        for row in range(9):
            for col in range(9):
                cellInfo = self.sudoku.getCell(row, col)
                yield Cell(str(cellInfo[0]), row, col)
        yield Label("123", id="mylabel")  # DEBUG Messages

    def on_cell_cell_update(self, event: Cell.CellUpdate) -> None:

        # --- only for DEBUG ---------
        label = self.query_one("#mylabel", Label)  # DEBUG
        # label.update(f"{event.oldValue}:{event.newValue}")
        label.update(f"{event.cellID}")
        # --- only for DEBUG ---------

        actualCell = self.sudoku.modifyCell(
            *self.fromCellID_getRowCol(event.cellID), int(event.newValue)
        )
        cell = self.query_one("#" + event.cellID, Cell)
        cell.value = str(actualCell[0])

    @staticmethod
    def fromCellID_getRowCol(cellID: str) -> Tuple[int, int]:
        return int(cellID[1]), int(cellID[2])


class SudopyTerminalInterface(App):
    """TUI for Sudopy

    based on Textual
    View + Controller"""

    CSS_PATH = "tui_app.tcss"

    def __init__(self, sudoku: Game):
        super().__init__()
        self.sudoku = sudoku

    def compose(self) -> ComposeResult:
        yield Playfield(self.sudoku, id="playfield")
        yield Header()
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        """Globale Tastatursteuerung (z. B. Escape zum Beenden)."""
        if event.key == "escape":
            self.exit()
