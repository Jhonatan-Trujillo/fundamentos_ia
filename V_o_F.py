# V_o_F.py
# Lógica proposicional: tablas de verdad y verificación de argumentos
from sympy import symbols, Or, And, Implies
# Definir símbolos
P, Q, R = symbols('P Q R')
# Expresión: (P ∨ Q) → R
expr = Implies(Or(P, Q), R)
# Generar tabla de verdad
from sympy.logic.boolalg import truth_table
for inputs, value in truth_table(expr, [P, Q, R]):
    print(dict(zip(['P','Q','R'], inputs)), value)
# Verificar argumento: si P→Q y Q→R, entonces P→R

premises = And(Implies(P, Q), Implies(Q, R))
result = all(val for _, val in truth_table(Implies(premises, Implies(P, R)), [P,Q,R]))
print('Argumento válido:', result)