from .board import Board


class Rules:
    """Encapsulates Shukaku game rules and move validation."""

    @staticmethod
    def is_valid_move(board: Board, row: int, col: int, value) -> bool:
        """Return True if placing value at (row, col) does not violate any rule."""
        raise NotImplementedError

    @staticmethod
    def is_solved(board: Board) -> bool:
        """Return True if the board is in a fully solved state."""
        raise NotImplementedError
