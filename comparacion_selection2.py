from sympy import symbols, Or, And, Equivalent
from sympy.logic.boolalg import truth_table
"""
Enunciado: Un estudiante es elegible para una beca si cumple una de estas dos condiciones:

- Su promedio es mayor o igual a 9.0.

- Su promedio es mayor a 8.0 y su nivel socioeconómico es bajo (1 o 2).

- Reto en Python: Escribe un script que compare los datos de un estudiante contra estas reglas de comparación lógica.
"""
# Filtro de becas universitarias

Pro_Alto, Pro_Medio, Ns_Bajo, B = symbols('Pro_Alto Pro_Medio Ns_Bajo B')

def beca_elegible(Pro_Alto, Pro_Medio, Ns_Bajo, B):
    return Equivalent(B, Or(Pro_Alto, And(Pro_Medio, Ns_Bajo)))