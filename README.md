# ShukakuProject

Proyecto de **Análisis de Algoritmos** — Pontificia Universidad Javeriana.

Implementación del puzzle **Shikaku** con interfaz web para juego humano, generador procedural basado en BSP y arquitectura lista para solucionadores con métricas de rendimiento.

---

## Contenido

- [Sobre el juego](#sobre-el-juego)
- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Algoritmos y complejidad](#algoritmos-y-complejidad)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [API REST](#api-rest)
- [Pruebas](#pruebas)

---

## Sobre el juego

**Shikaku** (四角に切れ) es un puzzle lógico japonés publicado por Nikoli. El objetivo es dividir la cuadrícula en rectángulos de forma que:

1. Cada rectángulo contenga **exactamente una pista** (número).
2. El **área** del rectángulo sea igual al número de esa pista.
3. Los rectángulos no se solapan y cubren **todo** el tablero.

### Cómo jugar

- Selecciona la dificultad y se genera un tablero nuevo automáticamente.
- Haz clic y arrastra sobre las celdas para dibujar un rectángulo.
- Si el rectángulo cumple las reglas de Shikaku, queda confirmado en el tablero.
- Si es incorrecto, parpadea en rojo y se descarta.
- El juego termina cuando todos los rectángulos están colocados correctamente.

---

## Arquitectura

```
┌─────────────────────────────────────────────┐
│                  Frontend                   │
│  index.html  ·  style.css  ·  game.js       │
│              api.js (fetch)                 │
└──────────────────┬──────────────────────────┘
                   │ HTTP / JSON
┌──────────────────▼──────────────────────────┐
│             API  (Flask)                    │
│          src/api/routes.py                  │
└────────┬───────────────────┬────────────────┘
         │                   │
┌────────▼────────┐  ┌───────▼────────────────┐
│   src/game/     │  │      src/solver/        │
│  board.py       │  │  base_solver.py         │
│  rules.py       │  │  metrics.py             │
│  generator.py   │  │  (solvers concretos)    │
└─────────────────┘  └────────────────────────┘
```

El backend expone una REST API JSON. El frontend es HTML/CSS/JS puro (sin frameworks) y se comunica con el backend vía `fetch`. Los solucionadores heredan de `BaseSolver` y registran métricas automáticamente en `SolverMetrics`.

---

## Estructura del proyecto

```
ShukakuProject/
├── app.py                      # Punto de entrada — levanta el servidor Flask
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── game/
│   │   ├── board.py            # Estado del tablero (grid, place, remove, is_complete)
│   │   ├── rules.py            # Validación de movimientos y condición de victoria
│   │   └── generator.py        # Generación de puzzles via BSP Top-Down
│   │
│   ├── solver/
│   │   ├── base_solver.py      # Clase abstracta — todo solver hereda de aquí
│   │   └── metrics.py          # Cronómetro y contador de nodos explorados
│   │
│   └── api/
│       ├── __init__.py         # Fábrica de la app Flask
│       └── routes.py           # Endpoints REST
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js              # Llamadas al backend (fetch + manejo de errores)
│       └── game.js             # Renderizado del tablero e interacción drag & drop
│
└── tests/
    ├── test_board.py
    └── test_solver.py
```

---

## Algoritmos y complejidad

### Generador — Binary Space Partitioning (BSP) Top-Down

El generador divide el tablero de forma recursiva usando una **pila explícita** (evita el límite de recursión de Python en tableros grandes).

```
generate(size, difficulty)
  1. Empujar el rectángulo inicial (size × size) a la pila
  2. Mientras la pila no esté vacía:
       rect ← pop()
       Si rect.area ≤ max_area → es una hoja (región final)
       Si no → elegir eje y posición de corte aleatoria → push(hijo_1, hijo_2)
  3. Para cada hoja → elegir celda aleatoria como pista
  4. Devolver Board con todas las pistas
```

| Operación | Complejidad |
|-----------|-------------|
| `_partition` | O(K) — cada región se procesa exactamente una vez |
| `_split` / `_cut_range` | O(1) — solo aritmética |
| `_pick_clue` | O(1) por región |
| Inicialización `Board` | O(N²) |
| **Total `generate`** | **O(N²)** |

*K = número de regiones finales ≈ N² / área\_promedio*

La partición misma **es** la solución oculta, por lo que todo tablero generado tiene solución garantizada por construcción.

### Validación de movimientos — `Rules.is_valid_rectangle`

El método construye un lookup `dict` de pistas en O(P) antes de iterar sobre el área, reduciendo la búsqueda interior de O(P) a O(1) por celda.

| Operación | Complejidad |
|-----------|-------------|
| Construir `clue_by_pos` | O(P) — P = número de pistas |
| Recorrer área del rectángulo | O(h × w) |
| **Total** | **O(P + h×w)** |

### Frontend — drag & drop

La capa de render usa **delta-update**: solo modifica las celdas que entraron o salieron del bounding-box entre dos eventos `mousemove` consecutivos, evitando recorrer todo el tablero.

| Operación | Complejidad |
|-----------|-------------|
| `updatePreviewBox` | O(\|prev Δ new\|) — diferencia simétrica de los dos boxes |
| `confirmRectangle` / `flashInvalid` | O(h × w) |
| Acceso a celda DOM | O(1) — caché `cellGrid[row][col]` |

---

## Requisitos

- Python 3.9+
- pip

---

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ejecución

```bash
python app.py
```

Abre `http://localhost:5001` en el navegador.

> **Nota macOS**: el puerto 5000 está ocupado por AirPlay Receiver desde macOS Monterey. El proyecto usa el puerto 5001.

---

## API REST

### `POST /api/game/new`

Crea un nuevo puzzle y devuelve el estado inicial.

**Request body:**
```json
{ "difficulty": "easy" | "medium" | "hard" }
```

**Response `200`:**
```json
{
  "width": 7,
  "height": 7,
  "clues": [
    { "x": 2, "y": 0, "value": 4 },
    { "x": 5, "y": 1, "value": 6 }
  ]
}
```

---

### `POST /api/game/move`

Valida y aplica un rectángulo dibujado por el jugador.

**Request body:**
```json
{
  "start_row": 0,
  "start_col": 1,
  "end_row": 1,
  "end_col": 3
}
```

**Response `200`:**
```json
{ "valid": true, "game_won": false }
```

**Errores:**
| Código | Motivo |
|--------|--------|
| `400` | Body inválido o campos faltantes |
| `409` | No hay partida activa (llamar `/api/game/new` primero) |

---

### `POST /api/solver/run` *(pendiente)*

Ejecutará el solucionador automático y devolverá la solución. Devuelve `501` hasta que se implemente.

---

### `GET /api/solver/metrics` *(pendiente)*

Devolverá las métricas de la última ejecución del solucionador. Devuelve `501` hasta que se implemente.

---

## Pruebas

```bash
pytest
```

Para ver cobertura:
```bash
pytest --cov=src --cov-report=term-missing
```

---

## Herramientas de desarrollo

El proyecto usa **ruff** para linting y formateo automático:

```bash
ruff check src/          # linting
ruff format src/         # formateo
```
