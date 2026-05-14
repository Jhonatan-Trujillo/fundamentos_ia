# Ejemplo 3 — N-Reinas con Backtracking + heurística MRV

def n_reinas(n):
    """Resuelve N-Reinas usando backtracking.
    Retorna lista de filas: solucion[col] = fila."""
    
    def es_valido(tablero, col, fila):
        for c in range(col):
            f = tablero[c]
            # Misma fila o diagonal
            if f == fila or abs(f - fila) == abs(c - col):
                return False
        return True
    
    def resolver(tablero, col):
        if col == n:
            return tablero[:]  # ✓ Solución
        for fila in range(n):
            if es_valido(tablero, col, fila):
                tablero[col] = fila
                resultado = resolver(tablero, col + 1)
                if resultado:
                    return resultado
                tablero[col] = -1  # Backtrack
        return None
    
    return resolver([-1] * n, 0)

sol = n_reinas(8)
print(f"Solución 8-Reinas: {sol}")
# → [0, 4, 7, 5, 2, 6, 1, 3]

# Visualizar tablero
def mostrar_tablero(solucion):
    n = len(solucion)
    for fila in range(n):
        linea = []
        for col in range(n):
            linea.append('♛' if solucion[col] == fila else '·')
        print(' '.join(linea))

mostrar_tablero(sol)