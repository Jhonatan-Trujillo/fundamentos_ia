#  Ejemplo 1 — Backtracking para colorear mapa

# Coloreado de mapa con Backtracking simple

# Grafo de adyacencia
vecinos = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q':  ['NT', 'SA', 'NSW'],
    'NSW':['Q', 'SA', 'V'],
    'V':  ['NSW', 'SA'],
    'T':  []
}
colores = ['Rojo', 'Verde', 'Azul']
variables = list(vecinos.keys())

def es_consistente(region, color, asignacion):
    """Verifica que ningún vecino tenga el mismo color."""
    return all(
        asignacion.get(v) != color
        for v in vecinos[region]
    )

def backtrack(asignacion):
    if len(asignacion) == len(variables):
        return asignacion  # ✓ Solución encontrada
    
    # Seleccionar variable sin asignar
    region = next(v for v in variables if v not in asignacion)
    
    for color in colores:
        if es_consistente(region, color, asignacion):
            asignacion[region] = color
            resultado = backtrack(asignacion)
            if resultado:
                return resultado
            del asignacion[region]  # ← backtrack
    
    return None  # Sin solución en este camino

solucion = backtrack({})
print("Solución:", solucion)
# → {'WA': 'Rojo', 'NT': 'Verde', 'SA': 'Azul', 'Q': 'Rojo', ...}