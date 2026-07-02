from typing import Tuple, cast
from unittest.mock import patch

import pytest
from textual.app import App, ComposeResult

import tui_app
from game import Game


# --- TUI Integration Test ---
class Mock_Game:
    "Simulates the Game cls from game.py"

    @staticmethod
    def getCellValue(row: int, col: int) -> int:
        return (row * col) % 10

    @staticmethod
    def modifyCell(row: int, col: int, newValue: int) -> int:
        return (row * col + newValue) % 10


@pytest.mark.asyncio
async def test_SudopyTerminalInterface_init() -> None:
    with patch("game.Game", Mock_Game):
        mock_game = Mock_Game()
        app = tui_app.SudopyTerminalInterface(cast(Game, mock_game))
        assert app is not None
        async with app.run_test() as _:
            for row in range(9):
                for col in range(9):
                    cell = app.query_one(f"#c{row}{col}", tui_app.Cell)
                    assert cell.value == str(Mock_Game.getCellValue(row, col))


@pytest.mark.asyncio
async def test_SudopyTerminalInterface_exit() -> None:
    with patch("game.Game", Mock_Game):
        mock_game = Mock_Game()
        app = tui_app.SudopyTerminalInterface(
            cast(Game, mock_game)
        )  # cast: just show the IDE checker that the type of mock_game is correct
        assert app is not None
        async with app.run_test() as pilot:
            await pilot.press("escape")
            assert not app.is_running


# --- Unit test the Cell widget ---
class CellApp(App):
    def __init__(self):
        super().__init__()
        self.received_messages = []

    def compose(self) -> ComposeResult:
        yield tui_app.Cell("5", 0, 0)

    def on_cell_cell_update(self, message: tui_app.Cell.CellUpdate) -> None:
        self.received_messages.append(message)


@pytest.mark.asyncio
async def test_Cell_init():
    app = CellApp()
    assert app is not None
    async with app.run_test() as _:
        cell = app.query_one(tui_app.Cell)
        assert cell.id == "c00"
        assert cell.value == "5"


@pytest.mark.asyncio
async def test_Cell_on_key():
    app = CellApp()
    async with app.run_test() as pilot:
        await pilot.press("7")
        # Check that post_message was called with a CellUpdate
        assert len(app.received_messages) == 1
        msg = app.received_messages[0]
        assert isinstance(msg, tui_app.Cell.CellUpdate)
        assert msg.cellID == "c00"
        assert msg.oldValue == "5"
        assert msg.newValue == "7"


# --- Unit test the Playfield widget ---
cellID_valid = [
    ("c00", (0, 0)),
    ("c17", (1, 7)),
    ("c93", (9, 3)),
]


@pytest.mark.parametrize("cellID, row_col", cellID_valid)
def test_Playfield_fromCellID_getRowCol(cellID: str, row_col: Tuple[int, int]):
    assert tui_app.Playfield.fromCellID_getRowCol(cellID) == row_col
