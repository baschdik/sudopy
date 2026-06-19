from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import Footer, Header, Input, Label


class Cell(Input):
    """Single Element of Sudoko Playfield (View Component)

    If selected, will send key 0-9 as CellUpdate message up.
    """

    def __init__(self, value, row, col) -> None:
        super().__init__(
            value,
            compact=True,
            max_length=1,
            restrict=r"[0-9]",
            id="c" + str(row) + str(col),
        )

    def on_key(self, event: events.Key) -> None:
        if event.key in "0123456789":
            event.stop
            self.post_message(self.CellUpdate(self.id, self.value, event.key))  # type: ignore
            self.clear()

    class CellUpdate(Message):
        """Sent updated value of the Cell when user have changed it"""

        def __init__(self, cellID: str, oldValue: str, newValue: str) -> None:
            super().__init__()
            self.cellID = cellID
            self.newValue = newValue
            self.oldValue = oldValue


class Playfield(Container):
    """The Sudoku Playfield (View Component)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        for row in range(9):
            for col in range(9):
                yield Cell("0", row, col)
        yield Label("123", id="mylabel")  # DEBUG Messages

    def on_cell_cell_update(self, event: Cell.CellUpdate) -> None:
        label = self.query_one("#mylabel", Label)  # DEBUG
        # label.update(f"{event.oldValue}:{event.newValue}")
        label.update(f"{event.cellID}")

        cell = self.query_one("#" + event.cellID, Cell)
        cell.value = f"{int(event.newValue) + 1}"


class SudopyTerminalInterface(App):
    """TUI for Sudopy

    based on Textual
    View + Controller"""

    CSS_PATH = "tui_app.tcss"

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Playfield(id="playfield")
        yield Header()
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        """Globale Tastatursteuerung (z. B. Escape zum Beenden)."""
        if event.key == "escape":
            self.exit()


if __name__ == "__main__":
    app = SudopyTerminalInterface()
    app.run()
