import pytest
from src.game.board import Board
from src.game.rules import Rules


class TestBoard:
    def test_initial_board_is_empty(self):
        board = Board(size=5)
        assert all(board.grid[r][c] is None for r in range(5) for c in range(5))

    def test_place_and_remove(self):
        pytest.skip("implement once Board.place / Board.remove are ready")

    def test_clone_is_independent(self):
        pytest.skip("implement once Board.clone is ready")

    def test_is_complete_when_full_and_valid(self):
        pytest.skip("implement once Board.is_complete is ready")
