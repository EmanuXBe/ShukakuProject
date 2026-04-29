/**
 * Thin wrapper around the Flask REST API.
 * All functions return the parsed JSON response body.
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

async function apiRunSolver() {
  // TODO: implement when solver endpoint is ready
  throw new Error("not implemented");
}

async function apiGetMetrics() {
  // TODO: implement when metrics endpoint is ready
  throw new Error("not implemented");
}
