"""
# Diagnostico médico básico

from sympy import symbols, And, Implies
from sympy.logic.boolalg import truth_table

F, T, G, D = symbols('F T G D')
"""
"""
F = FIEBRE
T = TOS
G = GRIPA
D = DESCANSO
"""
"""

# Si tengo fiebre y tos, entonces tengo gripe
expr = Implies(And(F, T), G )  
# Si tengo gripe, entonces debo descansar
expr2 = Implies(G, D)  
# Si tengo fiebre y tos, entonces debo descansar
conclusion = Implies(And(F, T), D)  
# Junto las premisas o las expr
premisas = And(expr, expr2) 
# Argumento: si (F ∧ T) → G y G → D, entonces (F ∧ T) → D
argumento = Implies(premisas, conclusion)

print("\n── Pruebas con booleanos ──")
print("\nFiebre=true Tos=true →", Implies(And(True, True), True))
print("Fiebre=true Tos=false →", Implies(And(True, False), False))
print("Fiebre=false Tos=false →", Implies(And(False, False), False  ))
print("Fiebre=false Tos=true →", Implies(And(False, True), False))  

print("\n── Tabla de verdad del argumento ──")
for inputs, value in truth_table(argumento, [F, T, G, D]):
    print(dict(zip(['F','T','G','D'], inputs)), value)
"""

# Motor de inferencia: encadenamiento hacia adelante
# Reglas y hechos iniciales
rules = [(['fiebre', 'tos'], 'gripe'),
         (['gripe'], 'descanso')]

facts = {'fiebre': True, 'tos': True}

# Encadenamiento hacia adelante (una pasada)
for condiciones, conclusiones in rules:
    if all(c in facts for c in condiciones):
        facts[conclusiones] = True

print(facts)

print("¿Necesita descanso?", facts.get('descanso', False))