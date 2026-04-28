from flask import Blueprint, jsonify, request, render_template

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.post("/api/game/new")
def new_game():
    """Create and return a new puzzle board."""
    raise NotImplementedError


@bp.post("/api/game/move")
def make_move():
    """Validate and apply a human move."""
    raise NotImplementedError


@bp.post("/api/solver/run")
def run_solver():
    """Run the synthetic solver and return the solution + metrics."""
    raise NotImplementedError


@bp.get("/api/solver/metrics")
def solver_metrics():
    """Return the metrics from the last solver run."""
    raise NotImplementedError
