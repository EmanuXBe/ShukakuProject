/**
 * Game UI — renders the board and wires up user interaction.
 * Depends on api.js being loaded first.
 */

const boardContainer = document.getElementById("board-container");
const metricsSection = document.getElementById("metrics");
const metricNodes   = document.getElementById("metric-nodes");
const metricTime    = document.getElementById("metric-time");

document.getElementById("btn-new-game").addEventListener("click", async () => {
  // TODO: call apiNewGame() and render the returned board
});

document.getElementById("btn-solve").addEventListener("click", async () => {
  // TODO: call apiRunSolver(), render solution, show metrics panel
});

function renderBoard(boardData) {
  // TODO: build and inject the board grid DOM from boardData
}

function renderMetrics(metrics) {
  metricNodes.textContent = metrics.nodes_explored;
  metricTime.textContent  = metrics.elapsed_seconds;
  metricsSection.hidden   = false;
}
