# Shukaku

Proyecto de **Análisis de Algoritmos** — Pontificia Universidad Javeriana.

Implementación del puzzle Shukaku con interfaz web para juego humano y solucionador sintético con métricas de rendimiento.

---

## Contenido

- [Sobre el juego](#sobre-el-juego)
- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [API REST](#api-rest)
- [Pruebas](#pruebas)
- [Roadmap](#roadmap)

---

## Sobre el juego

> Descripción del puzzle Shukaku y sus reglas — completar cuando se defina la especificación formal.

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

El backend expone una REST API en JSON. El frontend es HTML/CSS/JS puro, sin frameworks, y se comunica con el backend vía `fetch`. Los solucionadores heredan de `BaseSolver` y registran métricas automáticamente en `SolverMetrics`.

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
│   │   ├── board.py            # Estado del tablero (grid, place, remove, clone)
│   │   ├── rules.py            # Validación de movimientos y condición de victoria
│   │   └── generator.py        # Generación de puzzles con solución única
│   │
│   ├── solver/
│   │   ├── base_solver.py      # Clase abstracta — todo solver hereda de aquí
│   │   └── metrics.py          # Tiempo de ejecución y nodos explorados
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
│       ├── api.js              # Llamadas al backend
│       └── game.js             # Renderizado del tablero e interacción
│
└── tests/
    ├── test_board.py
    └── test_solver.py
```

---

## Requisitos

- Python 3.11+
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

Abre `http://localhost:5000` en el navegador.

---

## API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/game/new` | Crea un nuevo puzzle y devuelve el estado inicial |
| `POST` | `/api/game/move` | Aplica un movimiento humano y valida las reglas |
| `POST` | `/api/solver/run` | Ejecuta el solucionador y devuelve la solución |
| `GET`  | `/api/solver/metrics` | Devuelve las métricas de la última ejecución |

---

## Pruebas

```bash
pytest
```

---

## Roadmap

- [ ] Definir reglas formales del puzzle
- [ ] Implementar `Board`, `Rules` y `Generator`
- [ ] Implementar solucionador (algoritmo por definir)
- [ ] Conectar frontend con la API
- [ ] Análisis de complejidad y benchmarks
