from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .board import Board

# (min_area, max_area) por dificultad.
# max_area controla el tamaño máximo de cada región antes de dejar de partir.
# min_area garantiza que ninguna mitad quede con menos celdas de lo deseado.
_DIFFICULTY: Dict[str, Tuple[int, int]] = {
    "easy": (4, 9),
    "medium": (2, 6),
    "hard": (2, 4),
}


@dataclass
class _Rect:
    """Rectángulo interno usado solo durante la fase de partición."""

    row: int
    col: int
    height: int
    width: int

    @property
    def area(self) -> int:
        return self.height * self.width


class Generator:
    """
    Genera instancias válidas de Shikaku mediante Binary Space Partitioning (BSP)
    Top-Down. La partición misma constituye la solución oculta, por lo que todo
    tablero generado tiene al menos una solución garantizada por construcción.
    """

    def generate(self, size: int, difficulty: str = "medium") -> Board:
        """
        Particiona un tablero size×size y devuelve un Board con una pista por región.

        Complejidad global: O(size²)
          - _partition: O(K),   K ≈ size² / área_promedio  (cada rect se procesa una vez)
          - Colocación de pistas: O(K)
          - Inicialización de Board: O(size²)
        """
        min_area, max_area = _DIFFICULTY.get(difficulty, _DIFFICULTY["medium"])
        leaves: List[_Rect] = self._partition(size, size, min_area, max_area)
        clues_data: List[Tuple[int, int, int]] = [
            self._pick_clue(rect) for rect in leaves
        ]
        return Board(size, clues_data)

    # ------------------------------------------------------------------ #
    #  Partición BSP                                                       #
    # ------------------------------------------------------------------ #

    def _partition(
        self,
        total_height: int,
        total_width: int,
        min_area: int,
        max_area: int,
    ) -> List[_Rect]:
        """
        Divide iterativamente el tablero en rectángulos no superpuestos.

        Usa una pila explícita (orden DFS) para evitar el límite de recursión
        de Python en tableros grandes.

        Complejidad: O(K) — cada rectángulo se introduce y extrae de la pila
        exactamente una vez.  K es el número total de regiones finales.
        Espacio: O(K) para la pila y la lista de hojas.
        """
        stack: List[_Rect] = [_Rect(0, 0, total_height, total_width)]
        leaves: List[_Rect] = []

        while stack:
            rect = stack.pop()

            # Condición de parada: el rectángulo ya es suficientemente pequeño.
            if rect.area <= max_area:
                leaves.append(rect)
                continue

            children = self._split(rect, min_area)
            if children is None:
                # No existe corte válido que respete min_area → hoja sobredimensionada.
                leaves.append(rect)
            else:
                stack.extend(children)

        return leaves

    def _split(self, rect: _Rect, min_area: int) -> Optional[List[_Rect]]:
        """
        Elige aleatoriamente un eje y una posición de corte válidos para *rect*.

        Devuelve dos rectángulos hijos, o None si ningún corte satisface min_area.

        Complejidad: O(1) — solo aritmética; no itera sobre celdas.
        """
        h_range = self._cut_range(rect.height, rect.width, min_area)
        v_range = self._cut_range(rect.width, rect.height, min_area)

        options: List[str] = []
        if h_range:
            options.append("h")
        if v_range:
            options.append("v")
        if not options:
            return None

        if random.choice(options) == "h":
            cut = random.randint(*h_range)  # type: ignore[arg-type]
            return [
                _Rect(rect.row, rect.col, cut, rect.width),
                _Rect(rect.row + cut, rect.col, rect.height - cut, rect.width),
            ]
        else:
            cut = random.randint(*v_range)  # type: ignore[arg-type]
            return [
                _Rect(rect.row, rect.col, rect.height, cut),
                _Rect(rect.row, rect.col + cut, rect.height, rect.width - cut),
            ]

    @staticmethod
    def _cut_range(along: int, across: int, min_area: int) -> Optional[Tuple[int, int]]:
        """
        Calcula el rango válido [low, high] para un corte en la dimensión *along*.

        *along*  = longitud de la dimensión a cortar (height para corte H, width para V).
        *across* = longitud de la dimensión perpendicular.

        Un corte en la posición k produce dos mitades de tamaños k y (along - k).
        Ambas deben cumplir: mitad * across >= min_area.

        Complejidad: O(1) — aritmética pura.
        """
        min_slice = math.ceil(min_area / across)
        low, high = min_slice, along - min_slice
        return (low, high) if low <= high else None

    # ------------------------------------------------------------------ #
    #  Selección de pistas                                                 #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _pick_clue(rect: _Rect) -> Tuple[int, int, int]:
        """
        Elige una celda aleatoria uniforme dentro de *rect* como pista del puzzle.

        Devuelve (row, col, área).  Complejidad: O(1).
        """
        row = random.randint(rect.row, rect.row + rect.height - 1)
        col = random.randint(rect.col, rect.col + rect.width - 1)
        return (row, col, rect.area)
