from typing import List, Dict, Optional, Tuple


class Clue:
    """
    Representa una pista inicial en el tablero de Shikaku.
    Cada pista tiene una posición (fila, columna) y un número objetivo
    que indica el área del rectángulo que debe contenerla.
    """

    def __init__(self, row: int, col: int, value: int, clue_id: int):
        self.row = row
        self.col = col
        self.value = value
        self.clue_id = clue_id


class Rectangle:
    """
    Representa un rectángulo colocado en el tablero.
    Almacena su posición inicial (arriba-izquierda), su tamaño y a qué pista pertenece.
    """

    def __init__(
        self, start_row: int, start_col: int, height: int, width: int, clue_id: int
    ):
        self.start_row = start_row
        self.start_col = start_col
        self.height = height
        self.width = width
        self.clue_id = clue_id


class Board:
    """
    Representa el estado del tablero del rompecabezas Shikaku.

    Estructura de datos elegida:
    1. self.grid: Una matriz (lista de listas) de tamaño N x N.
       - Si una celda está vacía, contiene None.
       - Si una celda pertenece a un rectángulo, contiene el identificador (clue_id) de la pista.
       Esta matriz bidimensional es ideal para juegos de cuadrícula porque
       permite consultar o modificar el estado de cualquier celda en tiempo constante O(1).

    2. self.clues: Un diccionario que mapea el ID de la pista a un objeto Clue.
       Los diccionarios ofrecen acceso O(1) por clave, lo que facilita obtener los datos
       de una pista específica sin tener que buscarla en una lista.

    3. self.rectangles: Un diccionario que guarda los rectángulos activos en el tablero,
       usando el clue_id como clave. Ayuda a rastrear qué pistas ya tienen un área asignada.
    """

    def __init__(
        self, size: int, clues_data: Optional[List[Tuple[int, int, int]]] = None
    ):
        """
        Inicializa un nuevo tablero de Shikaku.

        Args:
            size (int): El tamaño del tablero (N para un tablero N x N).
            clues_data (List[Tuple[int, int, int]]): Lista de pistas. Cada pista es
                                                     una tupla (fila, columna, valor).
        """
        self.size = size
        # Inicializamos la matriz N x N con None (celdas vacías)
        self.grid: List[List[Optional[int]]] = [[None] * size for _ in range(size)]

        self.clues: Dict[int, Clue] = {}
        self.rectangles: Dict[int, Rectangle] = {}

        if clues_data:
            for index, (row, col, value) in enumerate(clues_data):
                clue_id = index + 1  # Empezamos los IDs en 1
                self.clues[clue_id] = Clue(row, col, value, clue_id)

    def is_cell_empty(self, row: int, col: int) -> bool:
        """
        Verifica si una celda específica está vacía (no pertenece a ningún rectángulo).

        La verificación se hace en O(1) simplemente accediendo a las coordenadas
        en la matriz (lista de listas).
        """
        if not self._is_valid_position(row, col):
            raise ValueError("Posición fuera de los límites del tablero.")
        return self.grid[row][col] is None

    def get_cell_rectangle_id(self, row: int, col: int) -> Optional[int]:
        """
        Devuelve el ID del rectángulo/pista al que pertenece la celda,
        o None si está vacía.
        """
        if not self._is_valid_position(row, col):
            raise ValueError("Posición fuera de los límites del tablero.")
        return self.grid[row][col]

    def place_rectangle(
        self, clue_id: int, start_row: int, start_col: int, height: int, width: int
    ) -> bool:
        """
        Coloca un rectángulo en el tablero, asociado a una pista específica.

        Lógica:
        1. Verifica que las dimensiones del rectángulo coincidan con el valor de la pista.
        2. Verifica que el rectángulo encaje dentro del tablero y no se solape con otros.
        3. Verifica que la pista de origen esté contenida dentro del área del rectángulo.
        4. Si todo es válido, actualiza el diccionario y la matriz (grid).
        """
        if clue_id not in self.clues:
            return False

        clue = self.clues[clue_id]

        # 1. Verificar área
        if height * width != clue.value:
            return False

        # 2. Verificar límites del tablero
        if not (
            self._is_valid_position(start_row, start_col)
            and self._is_valid_position(start_row + height - 1, start_col + width - 1)
        ):
            return False

        # Verificar solapamiento (todas las celdas deben estar vacías o ser del mismo clue_id)
        for r in range(start_row, start_row + height):
            for c in range(start_col, start_col + width):
                current_id = self.grid[r][c]
                if current_id is not None and current_id != clue_id:
                    return False

        # 3. Verificar que la pista misma está dentro de este rectángulo
        if not (
            start_row <= clue.row < start_row + height
            and start_col <= clue.col < start_col + width
        ):
            return False

        # Si ya había un rectángulo para esta pista, lo eliminamos primero
        self.remove_rectangle(clue_id)

        # 4. Actualizar la matriz (marca las celdas con el clue_id)
        for r in range(start_row, start_row + height):
            for c in range(start_col, start_col + width):
                self.grid[r][c] = clue_id

        self.rectangles[clue_id] = Rectangle(
            start_row, start_col, height, width, clue_id
        )
        return True

    def remove_rectangle(self, clue_id: int) -> None:
        """
        Elimina un rectángulo del tablero.

        Lógica:
        Busca el rectángulo en el diccionario. Si existe, recorre sus dimensiones
        para limpiar las celdas correspondientes en la matriz (asignándoles None),
        liberando el espacio para futuras jugadas.
        """
        if clue_id in self.rectangles:
            rect = self.rectangles[clue_id]
            for r in range(rect.start_row, rect.start_row + rect.height):
                for c in range(rect.start_col, rect.start_col + rect.width):
                    self.grid[r][c] = None
            del self.rectangles[clue_id]

    def _is_valid_position(self, row: int, col: int) -> bool:
        """Método auxiliar interno para validar si unas coordenadas están dentro del tablero."""
        return 0 <= row < self.size and 0 <= col < self.size

    def is_complete(self) -> bool:
        """
        Comprueba si el rompecabezas está resuelto correctamente.

        Lógica:
        Un rompecabezas de Shikaku está completo si:
        1. Se han colocado todos los rectángulos (uno para cada pista).
        2. No queda ninguna celda vacía en el tablero (todas están llenas).
        (La validación de solapamientos y áreas ya se realiza al colocar).
        """
        if len(self.rectangles) != len(self.clues):
            return False

        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is None:
                    return False
        return True
