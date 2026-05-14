# Ejemplo 2 — Algoritmo AC-3

from collections import deque

def ac3(variables, dominios, vecinos, restriccion):
    """
    Aplica consistencia de arcos AC-3.
    restriccion(Xi, xi, Xj, xj) → True si los valores son compatibles.
    """
    # Inicializar cola con todos los arcos
    cola = deque(
        (Xi, Xj)
        for Xi in variables
        for Xj in vecinos[Xi]
    )
    
    while cola:
        Xi, Xj = cola.popleft()
        if revisar(Xi, Xj, dominios, restriccion):
            if len(dominios[Xi]) == 0:
                return False  # ✗ Dominio vacío → sin solución
            for Xk in vecinos[Xi]:
                if Xk != Xj:
                    cola.append((Xk, Xi))
    return True  # ✓ Todos los arcos son consistentes

def revisar(Xi, Xj, dominios, restriccion):
    """Elimina valores de D(Xi) sin soporte en D(Xj)."""
    eliminado = False
    for xi in list(dominios[Xi]):
        # ¿Existe algún xj en D(Xj) que satisfaga la restricción?
        if not any(
            restriccion(Xi, xi, Xj, xj)
            for xj in dominios[Xj]
        ):
            dominios[Xi].remove(xi)
            eliminado = True
    return eliminado

# ──────────────────────────────────────
# Aplicar al problema de coloreado
# ──────────────────────────────────────
variables = ['WA', 'NT', 'SA', 'Q']
dominios = {v: {'R', 'G', 'B'} for v in variables}
vecinos = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q'],
    'Q':  ['NT', 'SA'],
}

def restriccion(Xi, xi, Xj, xj):
    return xi != xj  # Regiones adyacentes ≠ mismo color

resultado = ac3(variables, dominios, vecinos, restriccion)
print("Éxito:", resultado)
print("Dominios reducidos:", dominios)