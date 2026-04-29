from __future__ import annotations

from abc import ABC, abstractmethod

from src.game.board import Board

from .metrics import SolverMetrics


class BaseSolver(ABC):
    """Abstract base class for all Shukaku solvers."""

    def __init__(self):
        self.metrics = SolverMetrics()

    @abstractmethod
    def solve(self, board: Board) -> Board | None:
        """
        Attempt to solve the given board.
        Returns the solved Board or None if no solution exists.
        Records performance data in self.metrics.
        """

    def get_metrics(self) -> dict:
        return self.metrics.to_dict()
