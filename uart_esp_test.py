from machine import Pin, PWM, UART
import time

# Configuración UART
uart = UART(2, 115200)
uart.init(115200, 8, None, 1, timeout= 100, rx=16, tx=17)

# Configurar pines PWM
pwm_objects = {}
pins = [2, 4, 5, 12, 13, 14, 15, 18, 19, 21, 22, 23]

for pin in pins:
    try:
        pwm = PWM(Pin(pin))
        pwm.duty(0)
        pwm.freq(1000)
        pwm_objects[pin] = pwm
        print(f"Pin {pin} listo para PWM")
    except Exception as e:
        print(f"Error en pin {pin}: {e}")

print("ESP32 PWM Simple Controller listo")
print("Esperando comandos...")

def set_pwm(pin, freq, duty):
    try:
        if pin in pwm_objects:
            pwm_objects[pin].freq(freq)
            pwm_objects[pin].duty(duty)
            print(f"PWM configurado: Pin {pin}, {freq}Hz, duty {duty}")
            return f"OK:Pin{pin}_{freq}Hz_{duty}duty"
        return f"ERROR:Pin_{pin}_not_found"
    except Exception as e:
        return f"ERROR: {e}"

def process_command(command):
    try:
        command = command.strip()
        print(f"Procesando comando: '{command}'")
        
        parts = command.split(',')
        cmd = parts[0].upper()
        
        if cmd == "SET" and len(parts) == 4:
            return set_pwm(int(parts[1]), int(parts[2]), int(parts[3]))
        elif cmd == "STATUS":
            active = [str(p) for p, pw in pwm_objects.items() if pw.duty() > 0]
            return f"STATUS:Active:{','.join(active)}" if active else "STATUS:No_active"
        elif cmd == "STOP_ALL":
            for pwm in pwm_objects.values():
                pwm.duty(0)
            print("Todos los PWM detenidos")
            return "OK:All_stopped"
        else:
            return f"ERROR:Unknown_command: {cmd}"
    except Exception as e:
        return f"ERROR:Exception: {str(e)}"

# Bucle principal MEJORADO
buffer = ""
print("Iniciando bucle principal...")

while True:
    try:
        # Leer todos los datos disponibles
        if uart.any():
            data = uart.read(uart.any())
            if data:
                # Decodificar y reemplazar \r por nada
                data_str = data.decode('utf-8').replace('\r', '')
                print(f"Datos recibidos: '{data_str}'")
                buffer += data_str
                
                # Procesar TODAS las líneas completas
                lines = buffer.split('\n')
                print(f"Líneas encontradas: {len(lines)}")
                
                # Procesar todas las líneas excepto la última (incompleta)
                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        print(f"Procesando línea: '{line}'")
                        response = process_command(line)
                        print(f"Enviando respuesta: {response}")
                        uart.write(response + '\n')
                        time.sleep(0.1)  # Pequeña pausa entre respuestas
                
                # Mantener la última línea (incompleta) en el buffer
                buffer = lines[-1] if lines else ""
                
        time.sleep(0.01)
        
    except Exception as e:
        print(f"Error en bucle principal: {e}")
        buffer = ""  # Reset buffer on error
        time.sleep(0.1)