from .board import Board

class Rules:
    """
    Encapsula las reglas del juego de Shikaku y la validación de movimientos.
    Proporciona la "inteligencia" para validar las acciones de un jugador humano
    antes de que se apliquen permanentemente en el tablero.
    """

    @staticmethod
    def is_valid_rectangle(board: Board, start_row: int, start_col: int, height: int, width: int) -> bool:
        """
        Valida si un rectángulo dibujado por el usuario es legal según las reglas de Shikaku.
        
        Reglas a verificar:
        1. El rectángulo debe estar dentro de los límites del tablero.
        2. El rectángulo no debe solaparse con otros rectángulos ya colocados.
        3. El rectángulo debe contener EXACTAMENTE UNA pista (número).
        4. El área del rectángulo (ancho * alto) debe ser EXACTAMENTE IGUAL al valor de esa pista.
        """
        # 1. Validación espacial: Límites del tablero
        # Verificamos que las esquinas superior-izquierda e inferior-derecha
        # no excedan el tamaño de la matriz (board.size).
        if start_row < 0 or start_col < 0:
            return False
        if start_row + height > board.size or start_col + width > board.size:
            return False

        # Variables para rastrear las pistas encontradas dentro de este rectángulo
        clues_found = []

        # 2 y 3. Validación espacial: Solapamiento y Pistas
        # Recorremos cada celda que conforma el rectángulo propuesto
        for r in range(start_row, start_row + height):
            for c in range(start_col, start_col + width):
                
                # Verificamos solapamiento: si la celda no está vacía, significa que
                # ya pertenece a otro rectángulo. En Shikaku, los rectángulos no pueden solaparse.
                current_id = board.get_cell_rectangle_id(r, c)
                if current_id is not None:
                    return False
                    
                # Buscamos si hay alguna pista en esta celda específica.
                # Iteramos sobre todas las pistas del tablero.
                for clue in board.clues.values():
                    if clue.row == r and clue.col == c:
                        clues_found.append(clue)

        # Regla crítica de Shikaku: El rectángulo debe contener EXACTAMENTE una pista.
        # Si no tiene pistas, o si encierra a 2 o más pistas simultáneamente, es un movimiento ilegal.
        if len(clues_found) != 1:
            return False
            
        target_clue = clues_found[0]

        # 4. Validación matemática: Área vs Valor de la pista
        # Calculamos el área multiplicando la altura por el ancho (base x altura).
        # Este valor debe coincidir exactamente con el número de la pista contenida.
        area = height * width
        if area != target_clue.value:
            return False

        # Si supera todas las validaciones anteriores de espacio y matemáticas, el rectángulo es legal.
        return True

    @staticmethod
    def is_solved(board: Board) -> bool:
        """
        Verifica si el tablero ha sido completado totalmente y de forma correcta.
        
        Lógica:
        1. Validamos que la cantidad de rectángulos sea igual a la cantidad de pistas.
           (No pueden sobrar ni faltar pistas por cubrir).
        2. Validamos que el tablero completo esté cubierto, es decir, que no exista
           ninguna celda vacía (con valor None en el grid).
        """
        # Verificamos si se ha colocado un rectángulo por cada pista existente
        if len(board.rectangles) != len(board.clues):
            return False
            
        # Validación espacial: Cobertura total
        # Recorremos toda la matriz bidimensional buscando espacios vacíos
        for row in range(board.size):
            for col in range(board.size):
                if board.is_cell_empty(row, col):
                    return False
                    
        # Si todos los rectángulos se colocaron validando las reglas, y no hay 
        # espacios vacíos en ninguna coordenada, el jugador ha ganado.
        return True
