"""
==============================================================
SUDOKU COMO PROBLEMA DE SATISFACCIÓN DE RESTRICCIONES (CSP)
==============================================================
Curso: Fundamentos de IA — Sesión 5: CSP
Autor: [Tu nombre]

──────────────────────────────────────────────────────────────
MODELADO DEL PROBLEMA
──────────────────────────────────────────────────────────────

VARIABLES:
    Cada celda vacía del tablero 9*9 es una variable.
    Se identifican como (fila, col) donde fila, col ∈ {0..8}.
    Total: hasta 81 variables (las ya llenas son constantes).

DOMINIOS:
    - Celda vacía (valor 0): D(fila,col) = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    - Celda llena (valor k): D(fila,col) = {k}  ← dominio fijo

RESTRICCIONES (todas del tipo AllDifferent):
    1. Fila: ∀ fila ∈ {0..8}: todas las celdas de esa fila son distintas.
    2. Columna: ∀ col ∈ {0..8}: todas las celdas de esa columna son distintas.
    3. Bloque: ∀ bloque 3*3 ∈ {0..8}: todas las celdas del bloque son distintas.

SOLUCIÓN:
    Asignación completa y consistente: todos los valores asignados
    respetan las tres clases de restricciones.
==============================================================
"""

from collections import deque
import copy
import time


# ──────────────────────────────────────────────────────────────
# PUZZLE DE PRUEBA  (0 = celda vacía)
# ──────────────────────────────────────────────────────────────
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


# ──────────────────────────────────────────────────────────────
# UTILIDADES GENERALES
# ──────────────────────────────────────────────────────────────

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


def vecinos_de(fila, col):
    """
    Retorna el conjunto de coordenadas (f, c) que comparten
    fila, columna o bloque 3×3 con (fila, col).
    Excluye la propia celda.
    """
    vecs = set()
    # Misma fila
    for c in range(9):
        vecs.add((fila, c))
    # Misma columna
    for f in range(9):
        vecs.add((f, col))
    # Mismo bloque 3×3
    bf, bc = (fila // 3) * 3, (col // 3) * 3
    for f in range(bf, bf + 3):
        for c in range(bc, bc + 3):
            vecs.add((f, c))
    vecs.discard((fila, col))
    return vecs


def valores_validos(tablero, fila, col):
    """
    Retorna el conjunto de valores {1..9} que no aparecen
    en la fila, columna ni bloque 3×3 de (fila, col).
    """
    usados = set()
    for (f, c) in vecinos_de(fila, col):
        if tablero[f][c] != 0:
            usados.add(tablero[f][c])
    return set(range(1, 10)) - usados


# ──────────────────────────────────────────────────────────────
# PARTE 2 — BACKTRACKING SIN MRV
# ──────────────────────────────────────────────────────────────

llamadas_sin_mrv = 0  # Contador global para comparación

def siguiente_vacia_simple(tablero):
    """Selección simple: primera celda vacía en orden de lectura."""
    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                return (f, c)
    return None


def backtrack_simple(tablero):
    """
    Backtracking sin heurísticas.
    Retorna el tablero resuelto o None si no hay solución.
    """
    global llamadas_sin_mrv
    llamadas_sin_mrv += 1

    celda = siguiente_vacia_simple(tablero)
    if celda is None:
        return tablero  # ✓ Solución completa

    fila, col = celda
    for valor in range(1, 10):           # Orden fijo 1..9
        if valor in valores_validos(tablero, fila, col):
            tablero[fila][col] = valor
            resultado = backtrack_simple(tablero)
            if resultado:
                return resultado
            tablero[fila][col] = 0       # ← Backtrack

    return None                          # Sin solución en este camino


# ──────────────────────────────────────────────────────────────
# PARTE 3 — BACKTRACKING CON HEURÍSTICA MRV
# ──────────────────────────────────────────────────────────────

llamadas_con_mrv = 0  # Contador global para comparación

def siguiente_vacia_mrv(tablero):
    """
    MRV (Minimum Remaining Values):
    Selecciona la celda vacía con MENOS valores válidos posibles.
    Detecta conflictos antes → poda el árbol de búsqueda más rápido.
    """
    mejor = None
    min_opciones = 10  # Más que cualquier dominio posible (máx 9)

    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                n = len(valores_validos(tablero, f, c))
                if n < min_opciones:
                    min_opciones = n
                    mejor = (f, c)
                    if n == 1:
                        # No puede haber menos → salir ya
                        return mejor

    return mejor


def backtrack_mrv(tablero):
    """
    Backtracking con heurística MRV.
    Retorna el tablero resuelto o None si no hay solución.
    """
    global llamadas_con_mrv
    llamadas_con_mrv += 1

    celda = siguiente_vacia_mrv(tablero)
    if celda is None:
        return tablero  # ✓ Solución completa

    fila, col = celda
    for valor in sorted(valores_validos(tablero, fila, col)):
        tablero[fila][col] = valor
        resultado = backtrack_mrv(tablero)
        if resultado:
            return resultado
        tablero[fila][col] = 0           # ← Backtrack

    return None


# ──────────────────────────────────────────────────────────────
# BONUS — AC-3: PREPROCESAMIENTO DE DOMINIOS
# ──────────────────────────────────────────────────────────────

def construir_dominios(tablero):
    """
    Construye el diccionario de dominios para cada celda.
    - Celdas llenas: dominio = {valor}
    - Celdas vacías: dominio = {1..9} filtrado por vecinos ya llenos
    """
    dominios = {}
    for f in range(9):
        for c in range(9):
            if tablero[f][c] != 0:
                dominios[(f, c)] = {tablero[f][c]}
            else:
                dominios[(f, c)] = valores_validos(tablero, f, c)
    return dominios


def revisar(Xi, Xj, dominios):
    """
    Hace el arco (Xi → Xj) consistente:
    Elimina de D(Xi) los valores sin soporte en D(Xj).
    En Sudoku la restricción es siempre Xi ≠ Xj.
    Retorna True si se eliminó algún valor de D(Xi).
    """
    eliminado = False
    for xi in list(dominios[Xi]):
        # ¿Existe algún xj ≠ xi en D(Xj)?
        if not any(xj != xi for xj in dominios[Xj]):
            dominios[Xi].discard(xi)
            eliminado = True
    return eliminado


def ac3(dominios):
    """
    Algoritmo AC-3 para Sudoku.
    Procesa todos los arcos (Xi, Xj) donde Xi y Xj son vecinos.
    Reduce dominios hasta punto fijo.
    Retorna False si algún dominio queda vacío (sin solución).
    """
    # Construir cola inicial con TODOS los arcos
    cola = deque()
    for f in range(9):
        for c in range(9):
            Xi = (f, c)
            for Xj in vecinos_de(f, c):
                cola.append((Xi, Xj))

    while cola:
        Xi, Xj = cola.popleft()
        if revisar(Xi, Xj, dominios):
            if len(dominios[Xi]) == 0:
                return False  # ✗ Dominio vacío → no hay solución
            # Agregar arcos inversos para re-verificar
            for Xk in vecinos_de(*Xi):
                if Xk != Xj:
                    cola.append((Xk, Xi))

    return True  # ✓ Todos los dominios son consistentes


def aplicar_dominios_al_tablero(tablero, dominios):
    """
    Aplica los dominios reducidos al tablero:
    Si una celda vacía quedó con dominio de tamaño 1, la llena.
    """
    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0 and len(dominios[(f, c)]) == 1:
                tablero[f][c] = next(iter(dominios[(f, c)]))


def backtrack_mrv_con_ac3(tablero, dominios):
    """
    Backtracking con MRV + dominios reducidos por AC-3.
    Usa los dominios pre-calculados en vez de recalcular desde cero.
    """
    global llamadas_con_mrv  # Reutilizamos el mismo contador

    # Buscar celda vacía con menor dominio (MRV sobre dominios AC-3)
    mejor = None
    min_opciones = 10
    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                n = len(dominios[(f, c)])
                if n == 0:
                    return None  # Dominio vacío → retroceder
                if n < min_opciones:
                    min_opciones = n
                    mejor = (f, c)

    if mejor is None:
        return tablero  # ✓ Solución

    fila, col = mejor
    for valor in sorted(dominios[(fila, col)]):
        # Guardar estado anterior
        dom_guardado = {k: set(v) for k, v in dominios.items()}

        tablero[fila][col] = valor
        dominios[(fila, col)] = {valor}

        # Propagar asignación (mini AC-3 local)
        cola = deque()
        for Xk in vecinos_de(fila, col):
            cola.append((Xk, (fila, col)))
        exito = True
        while cola and exito:
            Xi, Xj = cola.popleft()
            if revisar(Xi, Xj, dominios):
                if len(dominios[Xi]) == 0:
                    exito = False
                else:
                    for Xk in vecinos_de(*Xi):
                        if Xk != Xj:
                            cola.append((Xk, Xi))

        if exito:
            resultado = backtrack_mrv_con_ac3(tablero, dominios)
            if resultado:
                return resultado

        # Backtrack: restaurar estado
        tablero[fila][col] = 0
        for k in dominios:
            dominios[k] = dom_guardado[k]

    return None


# ──────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL — EJECUTA LAS 3 VARIANTES Y COMPARA
# ──────────────────────────────────────────────────────────────

def main():
    global llamadas_sin_mrv, llamadas_con_mrv

    imprimir_tablero(sudoku, "Puzzle original")

    # ── Variante 1: Backtracking sin MRV ──────────────────────
    print("=" * 60)
    print("VARIANTE 1 — Backtracking SIN MRV")
    print("=" * 60)
    tablero1 = copy.deepcopy(sudoku)
    llamadas_sin_mrv = 0
    t0 = time.perf_counter()
    sol1 = backtrack_simple(tablero1)
    t1 = time.perf_counter()

    if sol1:
        imprimir_tablero(sol1, "Solución (sin MRV)")
        print(f"  Llamadas recursivas : {llamadas_sin_mrv:,}")
        print(f"  Tiempo              : {(t1-t0)*1000:.2f} ms")
    else:
        print("  Sin solución.")

    # ── Variante 2: Backtracking con MRV ──────────────────────
    print("=" * 60)
    print("VARIANTE 2 — Backtracking CON MRV")
    print("=" * 60)
    tablero2 = copy.deepcopy(sudoku)
    llamadas_con_mrv = 0
    t0 = time.perf_counter()
    sol2 = backtrack_mrv(tablero2)
    t1 = time.perf_counter()

    if sol2:
        imprimir_tablero(sol2, "Solución (con MRV)")
        print(f"  Llamadas recursivas : {llamadas_con_mrv:,}")
        print(f"  Tiempo              : {(t1-t0)*1000:.2f} ms")
    else:
        print("  Sin solución.")

    # ── Bonus: AC-3 + Backtracking ────────────────────────────
    print("=" * 60)
    print("BONUS — AC-3 como preprocesamiento + MRV")
    print("=" * 60)
    tablero3 = copy.deepcopy(sudoku)
    dominios = construir_dominios(tablero3)

    t0 = time.perf_counter()
    exito_ac3 = ac3(dominios)
    t_ac3 = time.perf_counter()

    if not exito_ac3:
        print("  AC-3 detectó que no hay solución.")
    else:
        # Contar celdas resueltas por AC-3
        resueltas_ac3 = sum(
            1 for (f, c) in dominios
            if tablero3[f][c] == 0 and len(dominios[(f, c)]) == 1
        )
        print(f"  Celdas resueltas por AC-3 solo: {resueltas_ac3}")

        # Aplicar valores fijos al tablero
        aplicar_dominios_al_tablero(tablero3, dominios)
        imprimir_tablero(tablero3, "Tablero tras AC-3")

        # Backtracking sobre lo que queda
        llamadas_con_mrv = 0
        sol3 = backtrack_mrv_con_ac3(tablero3, dominios)
        t1 = time.perf_counter()

        if sol3:
            imprimir_tablero(sol3, "Solución (AC-3 + MRV)")
            print(f"  Llamadas recursivas (AC-3+MRV): {llamadas_con_mrv:,}")
            print(f"  Tiempo total (AC-3 + BT)       : {(t1-t0)*1000:.2f} ms")
        else:
            print("  Sin solución tras AC-3 + backtracking.")

    # ── Tabla comparativa ─────────────────────────────────────
    print("\n" + "=" * 60)
    print("COMPARATIVA DE RENDIMIENTO")
    print("=" * 60)
    print(f"  {'Estrategia':<30} {'Llamadas recursivas':>20}")
    print(f"  {'─'*30} {'─'*20}")
    print(f"  {'Backtracking sin MRV':<30} {llamadas_sin_mrv:>20,}")
    print(f"  {'Backtracking con MRV':<30} {llamadas_con_mrv:>20,}")
    print()
    if llamadas_sin_mrv > 0:
        reduccion = (1 - llamadas_con_mrv / llamadas_sin_mrv) * 100
        print(f"  MRV redujo las llamadas en aprox. {reduccion:.1f}%")
    print()


if __name__ == "__main__":
    main()
