import time


class SolverMetrics:
    """Tracks algorithm performance data for analysis."""

    def __init__(self):
        self.nodes_explored: int = 0
        self.elapsed_seconds: float = 0.0
        self._start: float | None = None

    def start(self) -> None:
        self._start = time.perf_counter()

    def stop(self) -> None:
        if self._start is not None:
            self.elapsed_seconds = time.perf_counter() - self._start
            self._start = None

    def increment_nodes(self, count: int = 1) -> None:
        self.nodes_explored += count

    def reset(self) -> None:
        self.__init__()

    def to_dict(self) -> dict:
        return {
            "nodes_explored": self.nodes_explored,
            "elapsed_seconds": round(self.elapsed_seconds, 6),
        }
