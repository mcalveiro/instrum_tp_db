import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Datos de voltaje (en volts) y temperatura (en grados Celsius)
voltages = np.array([3.212, 3.195, 3.100, 3.004, 2.848, 2.735, 2.579, 2.441, 2.260, 2.082,
                     1.880, 1.678, 1.422, 1.210, 0.983, 0.751, 0.592, 0.418, 0.266, 0.158, 0.01]).reshape(-1, 1)
temperatures = np.array([115, 110, 105, 100, 94.9, 89.9, 84.9, 80, 74.9, 70.1, 65, 60, 55, 50,
                         44.9, 40, 35, 29.9, 25.2, 21.7, 15])

# Ajuste de la regresión lineal
model = LinearRegression()
model.fit(voltages, temperatures)

# Coeficientes de la regresión
slope = model.coef_[0]
intercept = model.intercept_

print(f"Pendiente (slope): {slope}")
print(f"Intercepto (intercept): {intercept}")

# Generar valores para la línea de regresión
voltages_fit = np.linspace(min(voltages), max(voltages), 100).reshape(-1, 1)
temperatures_fit = model.predict(voltages_fit)

# Graficar los puntos de datos y la línea de regresión
plt.figure(figsize=(8, 6))
plt.scatter(voltages, temperatures, color='blue', label='Datos de referencia')
plt.plot(voltages_fit, temperatures_fit, color='red', linestyle='--', label='Regresión lineal')
plt.xlabel("Voltaje (V)")
plt.ylabel("Temperatura (°C)")
plt.title("Curva de Temperatura vs. Voltaje")
plt.legend()
plt.grid(True)
plt.show()
