import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def escalon(net):
    return 1 if net >= 0 else 0

np.random.seed(42)

X = np.random.rand(60, 2)

y = np.array([
    1 if (nota >= 0.6 and asistencia >= 0.5) else 0
    for nota, asistencia in X
])
"""
y = np.array([
    1 if (nota + asistencia >= 1.2) else 0
    for nota, asistencia in X
])
"""
print("Aprueban:", np.sum(y == 1))
print("No aprueban:", np.sum(y == 0))

pesos = np.random.uniform(-0.5, 0.5, size=2)  # w1, w2
bias  = np.random.uniform(-0.5, 0.5)

tasa_aprendizaje = 0.1
epocas = 100

print("       \nENTRENAMIENTO DEL PERCEPTRÓN")

#    w ← w + α · (y - ŷ) · x
#    b ← b + α · (y - ŷ)

historial_errores = []

for epoca in range(epocas):
    errores = 0

    for i in range(len(X)):
        # Suma ponderada
        net = np.dot(pesos, X[i]) + bias

        # Predicción
        y_pred = escalon(net)

        # Error
        error = y[i] - y_pred

        # Actualización de pesos solo si hubo error
        if error != 0:
            pesos += tasa_aprendizaje * error * X[i]
            bias  += tasa_aprendizaje * error
            errores += 1

    historial_errores.append(errores)
    print(f"\nÉpoca {epoca+1:2d} | Errores: {errores} | Pesos: {pesos.round(4)} | Bias: {round(bias, 4)}")

print("         \nPREDICCIONES FINALES")

print(f"\n{'Nota':>6} {'Asistencia':>12} {'Real':>6} {'Predicción':>12} {'Resultado':>10}")

nombres = [
    (f"{x[0]*10:.1f}", f"{x[1]*100:.0f}%")
    for x in X
]

for i in range(len(X)):
    net    = np.dot(pesos, X[i]) + bias
    y_pred = escalon(net)
    ok     = "✅" if y_pred == y[i] else "❌"
    etiq   = "Aprueba" if y_pred == 1 else "No aprueba"
    print(f"\n{nombres[i][0]:>6} {nombres[i][1]:>12} {y[i]:>6} {etiq:>12} {ok:>10}")

print("     \nPRUEBA CON ESTUDIANTE NUEVO")

nota_nueva       = 6.0
asistencia_nueva = 75.0

entrada_nueva = np.array([nota_nueva / 10, asistencia_nueva / 100])
net_nueva     = np.dot(pesos, entrada_nueva) + bias
resultado     = escalon(net_nueva)

print(f"\nNota: {nota_nueva}  |  Asistencia: {asistencia_nueva}%")
print(f"Suma ponderada (net): {round(net_nueva, 4)}")
print(f"Predicción: {'✅ APRUEBA' if resultado == 1 else '❌ NO APRUEBA'}")

# ----------------------------------------------------------
# 7. GRÁFICAS
# ----------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Perceptrón — ¿El estudiante aprueba?", fontsize=14, fontweight="bold")
 
# ── Gráfica 1: Línea de decisión ──────────────────────────
# Separamos los puntos por clase para colorearlos distinto
aprueba     = X[y == 1]
no_aprueba  = X[y == 0]
 
ax1.scatter(aprueba[:, 0],    aprueba[:, 1],    color="green",  marker="o", s=100, label="Aprueba (y=1)",    zorder=3)
ax1.scatter(no_aprueba[:, 0], no_aprueba[:, 1], color="red",    marker="x", s=100, label="No aprueba (y=0)", zorder=3)
 
# Estudiante nuevo
ax1.scatter(entrada_nueva[0], entrada_nueva[1], color="blue", marker="*", s=200, label="Estudiante nuevo", zorder=4)
 
# Línea de decisión: net = 0  →  w1·x1 + w2·x2 + b = 0
# Despejamos x2: x2 = -(w1·x1 + b) / w2
x1_vals = np.linspace(0, 1, 100)
if pesos[1] != 0:
    x2_vals = -(pesos[0] * x1_vals + bias) / pesos[1]
    ax1.plot(x1_vals, x2_vals, "k--", linewidth=1.5, label="Línea de decisión")
 
ax1.set_xlabel("Nota normalizada (nota / 10)")
ax1.set_ylabel("Asistencia normalizada (asistencia / 100)")
ax1.set_title("Frontera de decisión aprendida")
ax1.legend(fontsize=8)
ax1.set_xlim(0, 1.05)
ax1.set_ylim(0, 1.05)
ax1.grid(True, linestyle="--", alpha=0.4)
 
# ── Gráfica 2: Errores por época ──────────────────────────
epocas_reales = list(range(1, len(historial_errores) + 1))
ax2.bar(epocas_reales, historial_errores, color="steelblue", edgecolor="white")
ax2.set_xlabel("Época")
ax2.set_ylabel("Número de errores")
ax2.set_title("Errores de clasificación por época")
ax2.set_xticks(epocas_reales)
ax2.grid(True, axis="y", linestyle="--", alpha=0.4)
 
# Línea en 0 errores
ax2.axhline(y=0, color="green", linewidth=1.5, linestyle="--", label="0 errores (convergencia)")
ax2.legend(fontsize=8)
 
plt.tight_layout()
plt.savefig("perceptron_graficas.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n📊 Gráficas guardadas en: perceptron_graficas.png")