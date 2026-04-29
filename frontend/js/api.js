/**
 * api.js — thin wrapper around the Shikaku Flask REST API.
 *
 * All functions are async and return the parsed JSON response body on success.
 * They throw on network errors or non-2xx HTTP status codes so callers can
 * handle failures with a single try/catch.
 */

/**
 * Start a new game and receive the initial board state.
 *
 * @param {"easy"|"medium"|"hard"} [difficulty="medium"]
 * @returns {Promise<{width: number, height: number, clues: Array<{x:number, y:number, value:number}>}>}
 */
async function apiNewGame(difficulty = "medium") {
  try {
    const res = await fetch("/api/game/new", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ difficulty }),
    });
    if (!res.ok) throw new Error(`Server error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("[apiNewGame]", err);
    throw err;
  }
}

/**
 * Submit a rectangle drawn by the player and get a validity verdict.
 *
 * Corners are sent in their original order; the server normalises them.
 *
 * @param {number} startRow  top-left row (0-indexed)
 * @param {number} startCol  top-left column
 * @param {number} endRow    bottom-right row
 * @param {number} endCol    bottom-right column
 * @returns {Promise<{valid: boolean, game_won: boolean}>}
 */
async function apiMakeMove(startRow, startCol, endRow, endCol) {
  try {
    const res = await fetch("/api/game/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        start_row: startRow,
        start_col: startCol,
        end_row: endRow,
        end_col: endCol,
      }),
    });
    if (!res.ok) throw new Error(`Server error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("[apiMakeMove]", err);
    throw err;
  }
}

/**
 * Trigger the automatic solver.
 * @returns {Promise<object>}
 */
async function apiRunSolver() {
  // TODO: implement when solver endpoint is ready
  throw new Error("not implemented");
}

/**
 * Fetch performance metrics from the last solver run.
 * @returns {Promise<{nodes_explored: number, elapsed_seconds: number}>}
 */
async function apiGetMetrics() {
  // TODO: implement when metrics endpoint is ready
  throw new Error("not implemented");
}
