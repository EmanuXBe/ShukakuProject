/**
 * game.js
 *
 * Capas:
 *   coords  — cálculos puros de bounding-box (sin efectos de DOM)
 *   grid    — caché DOM: cellGrid[row][col] = HTMLElement  →  O(1) por celda
 *   drag    — máquina de estados del gesto de arrastre
 *   render  — delta-update de clases CSS sobre el grid cacheado
 *   init    — arranque y renderizado del tablero
 *   events  — delegación de eventos (un listener por tipo, no uno por celda)
 */

// ─── Elementos raíz ──────────────────────────────────────────────────────────

const boardContainer  = document.getElementById("shikaku-board");
const difficultySelect = document.getElementById("difficulty-selector");
const btnRestart      = document.getElementById("btn-restart");
const btnVerify       = document.getElementById("btn-verify");
const winModal        = document.getElementById("win-modal");
const winClose        = document.getElementById("win-close");

// ─── Caché de elementos DOM ───────────────────────────────────────────────────
// Construida en renderBoard. Evita querySelector durante el gesto de arrastre.

/** @type {HTMLElement[][]} */
let cellGrid = [];

// ─── Coords — funciones puras ─────────────────────────────────────────────────

/**
 * Normaliza dos esquinas en un bounding-box (r1 ≤ r2, c1 ≤ c2).
 * @returns {{ r1: number, c1: number, r2: number, c2: number }}
 */
function boundingBox(r1, c1, r2, c2) {
  return {
    r1: Math.min(r1, r2),
    c1: Math.min(c1, c2),
    r2: Math.max(r1, r2),
    c2: Math.max(c1, c2),
  };
}

/** Comprueba si la celda (r, c) está dentro del box. */
function boxContains(box, r, c) {
  return r >= box.r1 && r <= box.r2 && c >= box.c1 && c <= box.c2;
}

// ─── Estado del drag ──────────────────────────────────────────────────────────

const drag = {
  active: false,
  originRow: 0,
  originCol: 0,
  /** @type {{ r1: number, c1: number, r2: number, c2: number } | null} */
  prevBox: null,
  /** @type {Element | null} — última celda procesada (evita trabajo duplicado) */
  lastCell: null,
};

function resetDrag() {
  drag.active   = false;
  drag.prevBox  = null;
  drag.lastCell = null;
  document.body.classList.remove("is-dragging");
}

// ─── Render — delta-update de clases CSS ─────────────────────────────────────

/**
 * Actualiza la preview aplicando solo las diferencias entre el box anterior
 * y el nuevo. Complejidad: O(|prevBox Δ newBox|) — mínimo trabajo posible.
 * Evita recorrer todo el tablero o hacer querySelectorAll en cada mousemove.
 */
function updatePreviewBox(newBox) {
  const prev = drag.prevBox;

  // Quitar .rect-preview de celdas que salieron del box
  if (prev) {
    for (let r = prev.r1; r <= prev.r2; r++) {
      for (let c = prev.c1; c <= prev.c2; c++) {
        if (!boxContains(newBox, r, c)) {
          cellGrid[r][c].classList.remove("rect-preview");
        }
      }
    }
  }

  // Añadir .rect-preview a celdas que entraron en el box
  for (let r = newBox.r1; r <= newBox.r2; r++) {
    for (let c = newBox.c1; c <= newBox.c2; c++) {
      if (!prev || !boxContains(prev, r, c)) {
        cellGrid[r][c].classList.add("rect-preview");
      }
    }
  }

  drag.prevBox = newBox;
}

/** Limpia la preview usando el box cacheado (sin querySelector). */
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

function confirmRectangle(box) {
  for (let r = box.r1; r <= box.r2; r++) {
    for (let c = box.c1; c <= box.c2; c++) {
      cellGrid[r][c].classList.add("rect-confirmed");
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

// ─── Handlers de drag ────────────────────────────────────────────────────────

function handleMouseDown(e) {
  const cell = e.target.closest(".cell");
  if (!cell) return;
  if (cell.classList.contains("rect-confirmed")) return; // rectángulo ya fijado

  e.preventDefault(); // evita selección de texto durante el arrastre

  document.body.classList.add("is-dragging");
  drag.active    = true;
  drag.originRow = +cell.dataset.row;
  drag.originCol = +cell.dataset.col;
  drag.prevBox   = null;
  drag.lastCell  = cell;

  updatePreviewBox(
    boundingBox(drag.originRow, drag.originCol, drag.originRow, drag.originCol),
  );
}

function handleMouseMove(e) {
  if (!drag.active) return;

  const cell = e.target.closest(".cell");
  if (!cell || cell === drag.lastCell) return; // misma celda → sin trabajo
  drag.lastCell = cell;

  updatePreviewBox(
    boundingBox(
      drag.originRow, drag.originCol,
      +cell.dataset.row, +cell.dataset.col,
    ),
  );
}

async function handleMouseUp() {
  if (!drag.active) return;

  const finalBox = drag.prevBox; // guardar antes de limpiar
  clearPreview();
  resetDrag();

  if (!finalBox) return;

  try {
    const result = await apiMakeMove(
      finalBox.r1, finalBox.c1, finalBox.r2, finalBox.c2,
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

// ─── Inicialización ───────────────────────────────────────────────────────────

async function initGame() {
  resetDrag();
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

  // Construir caché 2D junto con el DOM (un solo pass)
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

// ─── Modal de victoria ────────────────────────────────────────────────────────

function showWinModal() {
  boardContainer.classList.add("board-locked");
  winModal.classList.add("visible");
}

// ─── Registro de eventos ─────────────────────────────────────────────────────
// Delegación en boardContainer: un listener por tipo, no uno por celda.

boardContainer.addEventListener("mousedown", handleMouseDown);
boardContainer.addEventListener("mousemove", handleMouseMove);
document.addEventListener("mouseup",         handleMouseUp);
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

// Cerrar modal con Escape (requisito ARIA para role="dialog")
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && winModal.classList.contains("visible")) {
    winModal.classList.remove("visible");
    initGame();
  }
});

initGame();
