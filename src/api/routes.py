from flask import Blueprint, jsonify, render_template, request

from src.game.generator import Generator
from src.game.rules import Rules

bp = Blueprint("main", __name__)

current_board = None

_SIZE_MAP = {"easy": 5, "medium": 7, "hard": 10}


@bp.get("/")
def index():
    return render_template("index.html")


@bp.post("/api/game/new")
def new_game():
    global current_board

    data = request.get_json(silent=True) or {}
    difficulty = data.get("difficulty", "medium")
    size = _SIZE_MAP.get(difficulty, 7)

    current_board = Generator().generate(size, difficulty)

    clues = [
        {"x": clue.col, "y": clue.row, "value": clue.value}
        for clue in current_board.clues.values()
    ]
    return jsonify({"width": size, "height": size, "clues": clues})


@bp.post("/api/game/move")
def make_move():
    if current_board is None:
        return jsonify({"error": "No active game. Call /api/game/new first."}), 409

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    required = {"start_row", "start_col", "end_row", "end_col"}
    missing = required - data.keys()
    if missing:
        return jsonify({"error": f"Missing fields: {sorted(missing)}"}), 400

    try:
        r1 = min(int(data["start_row"]), int(data["end_row"]))
        r2 = max(int(data["start_row"]), int(data["end_row"]))
        c1 = min(int(data["start_col"]), int(data["end_col"]))
        c2 = max(int(data["start_col"]), int(data["end_col"]))
    except (ValueError, TypeError):
        return jsonify(
            {"error": "Fields start_row, start_col, end_row, end_col must be integers."}
        ), 400
    height = r2 - r1 + 1
    width = c2 - c1 + 1

    valid = Rules.is_valid_rectangle(current_board, r1, c1, height, width)

    game_won = False
    if valid:
        clue_id = next(
            (
                cid
                for cid, clue in current_board.clues.items()
                if r1 <= clue.row <= r2 and c1 <= clue.col <= c2
            ),
            None,
        )
        if clue_id is not None:
            current_board.place_rectangle(clue_id, r1, c1, height, width)
            game_won = current_board.is_complete()

    return jsonify({"valid": valid, "game_won": game_won})


@bp.post("/api/solver/run")
def run_solver():
    return jsonify({"error": "Not implemented yet."}), 501


@bp.get("/api/solver/metrics")
def solver_metrics():
    return jsonify({"error": "Not implemented yet."}), 501
