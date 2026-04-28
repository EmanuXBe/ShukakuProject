from .board import Board


class Generator:
    """Generates valid Shukaku puzzle instances."""

    def generate(self, size: int, difficulty: str = "medium") -> Board:
        """Return a new puzzle board with a unique solution."""
        raise NotImplementedError
