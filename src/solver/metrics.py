from __future__ import annotations

import time


class SolverMetrics:
    """Tracks algorithm performance data for a single solver run.

    Usage pattern:
        metrics.start()
        # ... solver work, call metrics.increment_nodes() as needed ...
        metrics.stop()
        data = metrics.to_dict()
    """

    def __init__(self) -> None:
        self.nodes_explored: int = 0
        self.elapsed_seconds: float = 0.0
        self._start: float | None = None

    def start(self) -> None:
        """Record the wall-clock start time using a high-resolution counter."""
        self._start = time.perf_counter()

    def stop(self) -> None:
        """Compute elapsed time since the last start() call and clear the timer."""
        if self._start is not None:
            self.elapsed_seconds = time.perf_counter() - self._start
            self._start = None

    def increment_nodes(self, count: int = 1) -> None:
        """Increment the node counter by *count* (default 1)."""
        self.nodes_explored += count

    def reset(self) -> None:
        """Reset all counters so the object can be reused for a new run."""
        self.__init__()  # type: ignore[misc]

    def to_dict(self) -> dict:
        """Return a JSON-serialisable summary of the collected metrics."""
        return {
            "nodes_explored": self.nodes_explored,
            "elapsed_seconds": round(self.elapsed_seconds, 6),
        }
