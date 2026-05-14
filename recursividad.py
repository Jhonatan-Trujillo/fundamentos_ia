def retroceder(historial, pasos):
    if pasos == 0:
        return historial
    else:
        return retroceder(historial[:-1], pasos - 1)

historial = ["ado", "oguri", "rem", "subaru", "lol"]

pasos = 2
resultado = retroceder(historial, pasos)
print(resultado)