/**
 * Lógica de Interfaz */

const boardContainer = document.getElementById("shikaku-board");
const difficultySelector = document.getElementById("difficulty-selector");
const btnRestart = document.getElementById("btn-restart");
const btnVerify = document.getElementById("btn-verify");

const boardSizes = {
  easy: 5,
  medium: 7,
  hard: 10,
};

function initGame() {
  const size = boardSizes[difficultySelector.value];
  renderBoard(size);
}

function renderBoard(size) {
  boardContainer.style.setProperty("--grid-size", size);
  boardContainer.innerHTML = "";

  for (let row = 0; row < size; row++) {
    for (let col = 0; col < size; col++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.dataset.row = row;
      cell.dataset.col = col;

      // MOCK: Generar algunas pistas falsas para visualizar
      if (Math.random() < 0.15) {
        cell.classList.add("clue");
        cell.textContent = Math.floor(Math.random() * 8) + 2;
      }

      cell.addEventListener("click", () => {
        cell.classList.toggle("rect-selected");
      });

      boardContainer.appendChild(cell);
    }
  }
}

// Botones
difficultySelector.addEventListener("change", initGame);
btnRestart.addEventListener("click", initGame);
btnVerify.addEventListener("click", () =>
  alert("Lógica de verificación no implementada aún en Python."),
);

// Inicializar la cuadrícula al cargar
initGame();
