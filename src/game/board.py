class Board:
    """Represents the Shukaku puzzle board state."""

    def __init__(self, size: int):
        self.size = size
        self.grid = [[None] * size for _ in range(size)]

    def place(self, row: int, col: int, value) -> bool:
        """Place a value on the board. Returns False if the move is invalid."""
        raise NotImplementedError

    def remove(self, row: int, col: int) -> None:
        """Remove the value at (row, col)."""
        raise NotImplementedError

    def is_complete(self) -> bool:
        """Return True when every cell is filled and all rules are satisfied."""
        raise NotImplementedError

    def clone(self) -> "Board":
        """Return a deep copy of this board."""
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Serialize board state to a JSON-compatible dict."""
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict) -> "Board":
        """Deserialize board state from a dict."""
        raise NotImplementedError
