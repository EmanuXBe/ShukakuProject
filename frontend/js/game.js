/**
 * game.js
 */

const boardContainer = document.getElementById("shikaku-board");
const difficultySelect = document.getElementById("difficulty-selector");
const btnRestart = document.getElementById("btn-restart");
const btnVerify = document.getElementById("btn-verify");
const winModal = document.getElementById("win-modal");
const winClose = document.getElementById("win-close");

let cellGrid = [];

// Paleta de colores para asignar dinámicamente a los rectángulos
const RECT_COLORS = [
  "rgba(255, 107, 107, 0.5)", // Rojo coral
  "rgba(46, 204, 113, 0.5)", // Verde esmeralda
  "rgba(52, 152, 219, 0.5)", // Azul claro
  "rgba(155, 89, 182, 0.5)", // Morado amatista
  "rgba(241, 196, 15, 0.6)", // Amarillo sol
  "rgba(230, 126, 34, 0.5)", // Naranja zanahoria
  "rgba(26, 188, 156, 0.5)", // Turquesa
  "rgba(253, 121, 168, 0.5)", // Rosa
  "rgba(116, 185, 255, 0.5)", // Azul pastel
];

// Contador para llevar registro de qué color usar en el siguiente rectángulo
let globalColorIndex = 0;

function boundingBox(r1, c1, r2, c2) {
  return {
    r1: Math.min(r1, r2),
    c1: Math.min(c1, c2),
    r2: Math.max(r1, r2),
    c2: Math.max(c1, c2),
  };
}

function boxContains(box, r, c) {
  return r >= box.r1 && r <= box.r2 && c >= box.c1 && c <= box.c2;
}

const drag = {
  active: false,
  originRow: 0,
  originCol: 0,
  prevBox: null,
  lastCell: null,
};

function resetDrag() {
  drag.active = false;
  drag.prevBox = null;
  drag.lastCell = null;
  document.body.classList.remove("is-dragging");
}

function updatePreviewBox(newBox) {
  const prev = drag.prevBox;

  if (prev) {
    for (let r = prev.r1; r <= prev.r2; r++) {
      for (let c = prev.c1; c <= prev.c2; c++) {
        if (!boxContains(newBox, r, c)) {
          cellGrid[r][c].classList.remove("rect-preview");
        }
      }
    }
  }

  for (let r = newBox.r1; r <= newBox.r2; r++) {
    for (let c = newBox.c1; c <= newBox.c2; c++) {
      if (!prev || !boxContains(prev, r, c)) {
        cellGrid[r][c].classList.add("rect-preview");
      }
    }
  }

  drag.prevBox = newBox;
}

function clearPreview() {
  if (!drag.prevBox) return;
  const { r1, c1, r2, c2 } = drag.prevBox;
  for (let r = r1; r <= r2; r++) {
    for (let c = c1; c <= c2; c++) {
      cellGrid[r][c].classList.remove("rect-preview");
    }
  }
  drag.prevBox = null;
}

/**
 * Confirma el rectángulo y le aplica un color diferente y el resaltado en sus bordes externos.
 */
function confirmRectangle(box) {
  // Asignamos un color en orden desde nuestra paleta
  const color = RECT_COLORS[globalColorIndex % RECT_COLORS.length];
  globalColorIndex++;

  for (let r = box.r1; r <= box.r2; r++) {
    for (let c = box.c1; c <= box.c2; c++) {
      const cell = cellGrid[r][c];

      // Aplicar estado de completado y el color asignado
      cell.classList.add("rect-confirmed");
      cell.style.setProperty("--rect-color", color);

      // Aplicar clases de bordes SOLO si la celda se encuentra en un límite del rectángulo.
      // El CSS usa variables (--b-top, etc.) con box-shadow para pintar estos bordes internamente.
      if (r === box.r1) cell.classList.add("border-top");
      if (r === box.r2) cell.classList.add("border-bottom");
      if (c === box.c1) cell.classList.add("border-left");
      if (c === box.c2) cell.classList.add("border-right");
    }
  }
}

function flashInvalid(box) {
  for (let r = box.r1; r <= box.r2; r++) {
    for (let c = box.c1; c <= box.c2; c++) {
      const el = cellGrid[r][c];
      el.classList.add("rect-invalid");
      setTimeout(() => el.classList.remove("rect-invalid"), 600);
    }
  }
}

function handleMouseDown(e) {
  const cell = e.target.closest(".cell");
  if (!cell) return;
  if (cell.classList.contains("rect-confirmed")) return;

  e.preventDefault();

  document.body.classList.add("is-dragging");
  drag.active = true;
  drag.originRow = +cell.dataset.row;
  drag.originCol = +cell.dataset.col;
  drag.prevBox = null;
  drag.lastCell = cell;

  updatePreviewBox(
    boundingBox(drag.originRow, drag.originCol, drag.originRow, drag.originCol),
  );
}

function handleMouseMove(e) {
  if (!drag.active) return;

  const cell = e.target.closest(".cell");
  if (!cell || cell === drag.lastCell) return;
  drag.lastCell = cell;

  updatePreviewBox(
    boundingBox(
      drag.originRow,
      drag.originCol,
      +cell.dataset.row,
      +cell.dataset.col,
    ),
  );
}

async function handleMouseUp() {
  if (!drag.active) return;

  const finalBox = drag.prevBox;
  clearPreview();
  resetDrag();

  if (!finalBox) return;

  try {
    const result = await apiMakeMove(
      finalBox.r1,
      finalBox.c1,
      finalBox.r2,
      finalBox.c2,
    );

    if (result.valid) {
      confirmRectangle(finalBox);
    } else {
      flashInvalid(finalBox);
    }

    if (result.game_won) showWinModal();
  } catch {
    console.error("[sendMove] Error al comunicarse con el servidor.");
  }
}

async function initGame() {
  resetDrag();
  globalColorIndex = 0; // Reiniciar los colores al comenzar una partida nueva
  boardContainer.classList.remove("board-locked");
  const difficulty = difficultySelect.value;

  try {
    const data = await apiNewGame(difficulty);
    renderBoard(data);
  } catch {
    alert("No se pudo conectar con el servidor. ¿Está corriendo Flask?");
  }
}

function renderBoard({ width, height, clues }) {
  boardContainer.style.setProperty("--grid-size", width);
  boardContainer.innerHTML = "";

  cellGrid = Array.from({ length: height }, () => new Array(width));

  const clueMap = Object.fromEntries(
    clues.map(({ x, y, value }) => [`${y},${x}`, value]),
  );

  for (let row = 0; row < height; row++) {
    for (let col = 0; col < width; col++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.dataset.row = row;
      cell.dataset.col = col;

      const key = `${row},${col}`;
      if (clueMap[key] !== undefined) {
        cell.classList.add("clue");
        cell.textContent = clueMap[key];
      }

      cellGrid[row][col] = cell;
      boardContainer.appendChild(cell);
    }
  }
}

function showWinModal() {
  boardContainer.classList.add("board-locked");
  winModal.classList.add("visible");
}

boardContainer.addEventListener("mousedown", handleMouseDown);
boardContainer.addEventListener("mousemove", handleMouseMove);
document.addEventListener("mouseup", handleMouseUp);
boardContainer.addEventListener("dragstart", (e) => e.preventDefault());

difficultySelect.addEventListener("change", initGame);

btnRestart.addEventListener("click", () => {
  winModal.classList.remove("visible");
  initGame();
});

btnVerify.addEventListener("click", () => {
  let uncovered = 0;
  for (const row of cellGrid) {
    for (const cell of row) {
      if (!cell.classList.contains("rect-confirmed")) uncovered++;
    }
  }
  if (uncovered === 0) {
    showWinModal();
  } else {
    alert(`Faltan ${uncovered} celda(s) por cubrir.`);
  }
});

winClose.addEventListener("click", () => {
  winModal.classList.remove("visible");
  initGame();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && winModal.classList.contains("visible")) {
    winModal.classList.remove("visible");
    initGame();
  }
});

initGame();
