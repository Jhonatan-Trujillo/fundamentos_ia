# un sistema de seguridad en una boveda
from sympy import symbols, Or, And, Implies
from sympy.logic.boolalg import truth_table

# Definir símbolos
C, R, E = symbols('C R E')  

def boveda_abierta(C, R, E):
    return Or(And(C, R), E)  # B = (C ∧ R) ∨ E

expr = boveda_abierta(C, R, E)

print("\n── Pruebas con booleanos ──")
print("Clave=True Retina=True Emergencia=False →", boveda_abierta(True, True, False))
print("Clave=True Retina=False Emergencia=False →", boveda_abierta(True, False, False))
print("Clave=False Retina=False Emergencia=True →", boveda_abierta(False, False, True))
print("Clave=False Retina=False Emergencia=False →", boveda_abierta(False, False, False))


for inputs, value in truth_table(expr, [C, R, E]):
    print(dict(zip(['C','R','E'], inputs)), value)

# Verificar argumento: Si (C ∧ R) ∨ E entonces B
premises = And(Implies(And(C, R), expr), Implies(E, expr))
result = all(val for _, val in truth_table(Implies(premises, expr), [C, R, E ]))
print("\nArgumento valido:", result)