"""
MODELO DEL PROBLEMA:

    VARIABLES:
        Cada celda vacía del tablero 9x9 es una variable.
        Se identifican como (fila, columna) donde fila y columna tienen posiciones {0, 1, 2, 3, 4, 5, 6, 7, 8}.
        Total: hasta 81 variables (las que estan llenas son constantes).

    DOMINIOS:
        Para cada variable (celda vacía), el dominio es {1, 2, 3, 4, 5, 6, 7, 8, 9}.

    RESTRICCIONES:
        1. Fila: Para cada fila, todas las celdas deben contener valores distintos.
        2. Columna: Para cada columna, todas las celdas deben contener valores distintos.
        3. Bloque: Para cada bloque 3x3, todas las celdas deben contener valores distintos.
        
"""

from collections import deque
import copy

def imprimir_tablero(tablero, titulo="Tablero"):
    """Imprime el tablero con separadores de bloque."""
    print(f"\n{'─'*25}  {titulo}  {'─'*25}")
    for i, fila in enumerate(tablero):
        if i in (3, 6):
            print("─" * 21)
        linea = ""
        for j, val in enumerate(fila):
            if j in (3, 6):
                linea += "│ "
            linea += (str(val) if val != 0 else "·") + " "
        print(linea)
    print()

def obtener_vecinos(fila, columna):
    """Devuelve las posiciones de las celdas que comparten fila, 
    columna o bloque con la celda dada."""
    vecinos = set()

    # Vecinos de la fila
    for c in range(9):
        if c != columna:
            vecinos.add((fila, c))

    # Vecinos de la columna
    for f in range(9):
        if f != fila:
            vecinos.add((f, columna))

    # Vecinos del bloque 3x3
    bloque_fila = (fila // 3) * 3 # fila donde empieza el bloque
    bloque_columna = (columna // 3) * 3 # columna donde empieza el bloque
    for f in range(bloque_fila, bloque_fila + 3):
        for c in range(bloque_columna, bloque_columna + 3):
            if (f, c) != (fila, columna):
                vecinos.add((f, c))

    return vecinos


def valores_validos(tablero, fila, columna):
    usados = set() # Conjunto de valores usados

    for (f, c) in obtener_vecinos(fila, columna):
        if tablero[f][c] != 0:
            usados.add(tablero[f][c])

    return set(range(1, 10)) - usados # {1, 2, ..., 9} menos los usados

def siguiente_vacia(tablero):
    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                return (f, c)
    return None  # no hay celdas vacías

def backtracking(tablero, contador):
    contador[0] += 1
    vacia = siguiente_vacia(tablero)
    if not vacia:
        return True  # Solución encontrada

    fila, columna = vacia
    for valor in valores_validos(tablero, fila, columna):
        tablero[fila][columna] = valor  # Asignar valor

        if backtracking(tablero, contador):
            return True  # Continuar con esta asignación

        tablero[fila][columna] = 0  # Desasignar (backtrack)

    return False  # No se encontró solución con esta asignación

def siguiente_vacia_mrv(tablero):
    valores_minimos = 9  # Más que el máximo posible
    mejor_celda = None

    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                numero_valores = len(valores_validos(tablero, f, c))
                if numero_valores < valores_minimos:
                    valores_minimos = numero_valores
                    mejor_celda = (f, c)

    return mejor_celda

def backtracking_mrv(tablero, contador):
    contador[0] += 1
    vacia = siguiente_vacia_mrv(tablero)
    if not vacia:
        return True  # Solución encontrada

    fila, columna = vacia
    for valor in valores_validos(tablero, fila, columna):
        tablero[fila][columna] = valor  # Asignar valor

        if backtracking_mrv(tablero, contador):
            return True  # Continuar con esta asignación

        tablero[fila][columna] = 0  # Desasignar (backtrack)

    return False  # No se encontró solución con esta asignación

# La idea clave es: entre más restringida es una variable, más urgente es asignarla primero.

def construir_dominios(tablero):
    dominios = {}
    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                dominios[(f, c)] = valores_validos(tablero, f, c)
            else:
                dominios[(f, c)] = {tablero[f][c]}  # Dominio fijo para celdas ya llenas
    return dominios

def revisar(Xi, Xj, dominios):
    """¿Cada valor de Xi tiene soporte en Xj?"""
    eliminado = False
    for x in set(dominios[Xi]): # Para cada valor posible de Xi
        if dominios[Xj] == {x}: # Si Xj solo tiene un valor posible y es x, entonces x no es válido para Xi
            dominios[Xi].discard(x)  # Eliminar x del dominio de Xi
            eliminado = True
    return eliminado



def ac3(dominios):
    # Meter todos los arcos en la cola
    cola = deque()
    for f in range(9):
        for c in range(9):
            for vecino in obtener_vecinos(f, c):
                cola.append(((f, c), vecino))

    while cola:
        Xi, Xj = cola.popleft()  # sacar un arco

        if revisar(Xi, Xj, dominios):  # si se eliminó algo de D(Xi)
            if len(dominios[Xi]) == 0:
                return False  # dominio vacío → sin solución

            # Agregar arcos inversos para re-verificar
            for vecino in obtener_vecinos(*Xi):
                if vecino != Xj:  # No agregar el arco que acabamos de revisar
                    cola.append((vecino, Xi))

    return True  # todos los dominios son consistentes

def imprimir_tablero(tablero):
    for f in range(9):
        if f in (3, 6):
            print("─" * 21)
        fila = ""
        for c in range(9):
            if tablero[f][c] == 0:
                fila += "· "
            else:
                fila += str(tablero[f][c]) + " "
            if c in (2, 5):
                fila += "│ "
        print(fila)

def aplicar_dominios(tablero, dominios):
    for (f, c), valores in dominios.items():
        if len(valores) == 1:
            tablero[f][c] = next(iter(valores))  # Asignar el único valor posible

sudoku = [
    [5, 3, 0,  0, 7, 0,  0, 0, 0],
    [6, 0, 0,  1, 9, 5,  0, 0, 0],
    [0, 9, 8,  0, 0, 0,  0, 6, 0],

    [8, 0, 0,  0, 6, 0,  0, 0, 3],
    [4, 0, 0,  8, 0, 3,  0, 0, 1],
    [7, 0, 0,  0, 2, 0,  0, 0, 6],

    [0, 6, 0,  0, 0, 0,  2, 8, 0],
    [0, 0, 0,  4, 1, 9,  0, 0, 5],
    [0, 0, 0,  0, 8, 0,  0, 7, 9],
]
print("─── Puzzle original ───")
imprimir_tablero(sudoku)

contador_sin_mrv = [0]
tablero1 = copy.deepcopy(sudoku)
backtracking(tablero1, contador_sin_mrv)
print("\n─── Solución sin MRV ───")
imprimir_tablero(tablero1)
print(f"\nSin MRV: {contador_sin_mrv[0]} llamadas")

contador_con_mrv = [0]
tablero2 = copy.deepcopy(sudoku)
backtracking_mrv(tablero2, contador_con_mrv)
print("\n─── Solución con MRV ───")
imprimir_tablero(tablero2)
print(f"\nCon MRV: {contador_con_mrv[0]} llamadas")

tablero3 = copy.deepcopy(sudoku)
dominios = construir_dominios(tablero3)
exito = ac3(dominios)

resueltas = sum(1 for (f, c) in dominios
                if tablero3[f][c] == 0 and len(dominios[(f, c)]) == 1)

aplicar_dominios(tablero3, dominios)
print("\n─── Solución con AC-3 ───")
imprimir_tablero(tablero3)
print(f"\nAC-3 exitoso: {exito}")
print(f"Celdas resueltas solo por AC-3: {resueltas}")