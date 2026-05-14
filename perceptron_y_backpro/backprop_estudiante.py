# ============================================================
#  BACKPROPAGATION — ¿El estudiante aprueba o no?
#  Red: 2 entradas → 3 neuronas ocultas → 1 salida
#  Mismas entradas que el perceptrón, pero ahora con una
#  capa oculta que permite aprender patrones más complejos.
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# 1. FUNCIONES DE ACTIVACIÓN Y SUS DERIVADAS
#    Usamos Sigmoide: suave, diferenciable, rango (0,1)
#    Necesitamos la derivada para el backward pass

def sigmoide(z):
    return 1 / (1 + np.exp(-z))

def sigmoide_derivada(z):
    s = sigmoide(z)
    return s * (1 - s)   # Propiedad de la sigmoide

np.random.seed(42)

X = np.random.rand(60, 2)

y = np.array([
    [1] if (nota >= 0.5 and asistencia >= 0.5) else [0]
    for nota, asistencia in X
])

print("Aprueban:", np.sum(y == 1))
print("No aprueban:", np.sum(y == 0))

#    Capa de entrada : 2 neuronas
#    Capa oculta     : 3 neuronas
#    Capa de salida  : 1 neurona

# Pesos capa entrada → oculta  (2 entradas × 3 neuronas)
W1 = np.random.uniform(-0.5, 0.5, (2, 3))
b1 = np.zeros((1, 3))

# Pesos capa oculta → salida  (3 neuronas × 1 salida)
W2 = np.random.uniform(-0.5, 0.5, (3, 1))
b2 = np.zeros((1, 1))

tasa_aprendizaje = 0.5
epocas           = 8000

# 4. ENTRENAMIENTO — Forward + Backward pass

print("         \nENTRENAMIENTO — BACKPROPAGATION")

historial_perdida = []

for epoca in range(epocas):

    # ── FORWARD PASS ──────────────────────────────────────
    # Capa oculta
    Z1 = X @ W1 + b1          # Suma ponderada capa oculta
    A1 = sigmoide(Z1)          # Activación capa oculta

    # Capa de salida
    Z2 = A1 @ W2 + b2          # Suma ponderada capa salida
    A2 = sigmoide(Z2)          # Predicción final ŷ

    # Función de pérdida — MSE
    perdida = np.mean((y - A2) ** 2)
    historial_perdida.append(perdida)

    # ── BACKWARD PASS ─────────────────────────────────────
    # Gradiente en la salida: dL/dA2
    dA2 = -2 * (y - A2) / len(X)

    # Gradiente respecto a Z2 (regla de la cadena)
    dZ2 = dA2 * sigmoide_derivada(Z2)

    # Gradientes de W2 y b2
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0, keepdims=True)

    # Propagamos el error hacia la capa oculta
    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * sigmoide_derivada(Z1)

    # Gradientes de W1 y b1
    dW1 = X.T @ dZ1
    db1 = np.sum(dZ1, axis=0, keepdims=True)

    # ── ACTUALIZACIÓN DE PESOS (Gradient Descent) ─────────
    W2 -= tasa_aprendizaje * dW2
    b2 -= tasa_aprendizaje * db2
    W1 -= tasa_aprendizaje * dW1
    b1 -= tasa_aprendizaje * db1

    # Mostrar pérdida cada 1000 épocas
    if (epoca + 1) % 1000 == 0:
        print(f"\nÉpoca {epoca+1:5d} | Pérdida (MSE): {perdida:.6f}")


# 5. PREDICCIONES FINALES

print("            \nPREDICCIONES FINALES")

print(f"\n{'Nota':>6} {'Asistencia':>12} {'Real':>6} {'Prob.':>8} {'Predicción':>12} {'OK':>4}")
print("-" * 55)

nombres = [
    (f"{x[0]*10:.1f}", f"{x[1]*100:.0f}%")
    for x in X
]

# Forward pass final con los pesos aprendidos
Z1_f = X @ W1 + b1
A1_f = sigmoide(Z1_f)
Z2_f = A1_f @ W2 + b2
A2_f = sigmoide(Z2_f)

for i in range(len(X)):
    prob   = A2_f[i][0]
    pred   = 1 if prob >= 0.5 else 0
    etiq   = "Aprueba" if pred == 1 else "No aprueba"
    ok     = "✅" if pred == y[i][0] else "❌"
    print(f"\n{nombres[i][0]:>6} {nombres[i][1]:>12} {int(y[i][0]):>6} {prob:>8.4f} {etiq:>12} {ok:>4}")


# 6. PRUEBA CON UN ESTUDIANTE NUEVO

print("        \nPRUEBA CON ESTUDIANTE NUEVO")

nota_nueva       = 6.0
asistencia_nueva = 75.0

entrada_nueva = np.array([[nota_nueva / 10, asistencia_nueva / 100]])
z1n = entrada_nueva @ W1 + b1
a1n = sigmoide(z1n)
z2n = a1n @ W2 + b2
prob_nueva = sigmoide(z2n)[0][0]

print(f"\nNota: {nota_nueva}  |  Asistencia: {asistencia_nueva}%")
print(f"Probabilidad de aprobar: {prob_nueva:.4f} ({prob_nueva*100:.1f}%)")
print(f"Predicción: {'✅ APRUEBA' if prob_nueva >= 0.5 else '❌ NO APRUEBA'}")

# 7. GRÁFICAS

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Backpropagation — ¿El estudiante aprueba?", fontsize=14, fontweight="bold")

# ── Gráfica 1: Curva de pérdida ───────────────────────────
ax1.plot(historial_perdida, color="steelblue", linewidth=1.5)
ax1.set_xlabel("Época")
ax1.set_ylabel("Pérdida (MSE)")
ax1.set_title("Curva de aprendizaje\n(cómo bajó el error con cada época)")
ax1.grid(True, linestyle="--", alpha=0.4)

# Anotamos el valor inicial y final
ax1.annotate(f"Inicio: {historial_perdida[0]:.4f}",
             xy=(0, historial_perdida[0]),
             xytext=(400, historial_perdida[0] + 0.01),
             fontsize=8, color="red",
             arrowprops=dict(arrowstyle="->", color="red"))
ax1.annotate(f"Final: {historial_perdida[-1]:.6f}",
             xy=(len(historial_perdida)-1, historial_perdida[-1]),
             xytext=(3000, historial_perdida[-1] + 0.02),
             fontsize=8, color="green",
             arrowprops=dict(arrowstyle="->", color="green"))

# ── Gráfica 2: Probabilidades predichas por estudiante ────
etiquetas_estudiantes = [f"{x[0]*10:.1f}/{x[1]*100:.0f}%" for x in X]
probabilidades = [A2_f[i][0] for i in range(len(X))]
colores = ["green" if p >= 0.5 else "red" for p in probabilidades]

barras = ax2.bar(etiquetas_estudiantes, probabilidades, color=colores, edgecolor="white", width=0.5)
ax2.axhline(y=0.5, color="black", linewidth=1.5, linestyle="--", label="Umbral (0.5)")
ax2.set_xlabel("Estudiante (nota / asistencia)")
ax2.set_ylabel("Probabilidad de aprobar")
ax2.set_title("Probabilidad predicha por estudiante\n(verde = aprueba, rojo = no aprueba)")
ax2.set_ylim(0, 1.1)
ax2.legend(fontsize=8)
ax2.grid(True, axis="y", linestyle="--", alpha=0.4)

# Etiqueta encima de cada barra con el valor
for barra, prob in zip(barras, probabilidades):
    ax2.text(barra.get_x() + barra.get_width() / 2,
             barra.get_height() + 0.02,
             f"{prob:.2f}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("backprop_graficas.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n📊 Gráficas guardadas en: backprop_graficas.png")