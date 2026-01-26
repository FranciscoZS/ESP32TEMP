import time
import machine
from mlx90614 import MLX90614

# SOLUCIÓN CLAVE 1: Inicializar I2C con frecuencia explícita
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)

# SOLUCIÓN CLAVE 2: Escanear bus para diagnóstico
print("Escaneando bus I2C...")
devices = i2c.scan()
if devices:
    print("Dispositivos encontrados en HEX:", [hex(d) for d in devices])
    print("Dispositivos encontrados en DEC:", devices)
else:
    print("¡No se encontró ningún dispositivo! Revisa conexiones y alimentación.")
    # Detiene la ejecución si no hay dispositivos
    raise SystemExit("Error de comunicación I2C.")

# Inicializar el sensor
sensor = MLX90614(i2c)

print("\n--- Leyendo sensor MLX90614 ---")
try:
    while True:
        print(f"Ambiente: {sensor.ambient_temp:.2f} °C, Objeto: {sensor.object_temp:.2f} °C")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nPrograma detenido.")