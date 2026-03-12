# Gestion de inventarios de una tienda
from sympy import symbols
from sympy.logic.boolalg import truth_table

productos = [{"nombre": "Pan", "stock": 10, "tipo": "Basico"}, 
            {"nombre": "Reloj", "stock": 0, "tipo": "Lujo"}]

def producto_disponible(stock):
    return stock > 0

def producto_lujo(tipo):
    return tipo == "Lujo"

# Para Universal
todos_disponibles = all(producto_disponible(p["stock"]) for p in productos)
print("¿Todos los productos están disponibles?", todos_disponibles)

# Para Existencial
lujos_disponibles = any(producto_lujo(p["tipo"]) for p in productos)
print("¿Hay productos de lujo disponibles?", lujos_disponibles)
