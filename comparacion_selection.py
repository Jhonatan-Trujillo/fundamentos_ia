"""
Enunciado: Un estudiante es elegible para una beca si cumple una de estas dos condiciones:

- Su promedio es mayor o igual a 9.0.

- Su promedio es mayor a 8.0 y su nivel socioeconómico es bajo (1 o 2).

- Reto en Python: Escribe un script que compare los datos de un estudiante contra estas reglas de comparación lógica.
"""
# Filtro de becas universitarias

candidatos = [{"nombre": "Maria", "promedio": 9.7, "nivel_socioeconomico": 1}, 
            {"nombre": "Pedro", "promedio": 6, "nivel_socioeconomico": 3},
            {"nombre": "Juan", "promedio": 7.9, "nivel_socioeconomico": 2},
            {"nombre": "Jhon", "promedio": 8, "nivel_socioeconomico": 3},
            {"nombre": "Alexandra", "promedio": 8.5, "nivel_socioeconomico": 1},
            {"nombre": "Veronica", "promedio": 8.9, "nivel_socioeconomico": 2}]

def beca_elegible(promedio, nivel_socioeconomico):
    return promedio >= 9.0 or (promedio > 8.0 and nivel_socioeconomico in [1, 2])

# Para Universal
todos_elegibles = all(beca_elegible(c["promedio"], c["nivel_socioeconomico"]) for c in candidatos)
print("¿Todos los candidatos son elegibles para la beca?", todos_elegibles)

# Para Existencial
algunos_elegibles = any(beca_elegible(c["promedio"], c["nivel_socioeconomico"]) for c in candidatos)
print("¿Hay candidatos elegibles para la beca?", algunos_elegibles)