"""
Suma de Dígitos de un Número 
Este es un ejercicio fundamental que enseña a aplicar la lógica recursiva a un solo 
valor numérico, usando operaciones de división y módulo.
Problema
Crea una función recursiva que calcule 
la suma de todos los dígitos de un número entero positivo dado (N).
"""
def suma_digitos(n):
    if n == 0:
        return 0
    else:
        return n + suma_digitos(n-1)
    
n = 9 
print(suma_digitos(n))