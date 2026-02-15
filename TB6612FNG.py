from machine import Pin, PWM

class Motor:
    def __init__(self, pin_pwm, pin_in1, pin_in2, freq=2000):
        """
        Controlador para un canal del puente H TB6612FNG.
        Args:
            pin_pwm (int): Número del pin para el PWM.
            pin_in1 (int): Número del pin para IN1 (AI1 o BI1).
            pin_in2 (int): Número del pin para IN2 (AI2 o BI2).
            freq (int): Frecuencia del PWM en Hz (por defecto 2000).
        """
        # Se usan variables de instancia (self) para mantener los objetos vivos
        self.in1 = Pin(pin_in1, Pin.OUT, value=0)
        self.in2 = Pin(pin_in2, Pin.OUT, value=0)
        
        # Inicialización directa del PWM
        self.pwm = PWM(Pin(pin_pwm))
        self.pwm.freq(freq)
        self.pwm.duty_u16(0)

    def set_speed(self, percent):
        """Ajusta la velocidad del motor (0 a 100%)."""
        # Restringe el porcentaje entre 0 y 100 para evitar errores
        percent = max(0, min(100, percent))
        # Cálculo en línea: evita llamar a otra función, ahorrando ciclos de CPU
        self.pwm.duty_u16((percent * 65535) // 100)

    def forward(self, speed=None):
        """Gira hacia adelante. Opcionalmente ajusta la velocidad."""
        self.in1.value(1)
        self.in2.value(0)
        if speed is not None:
            self.set_speed(speed)

    def backward(self, speed=None):
        """Gira hacia atrás. Opcionalmente ajusta la velocidad."""
        self.in1.value(0)
        self.in2.value(1)
        if speed is not None:
            self.set_speed(speed)
            
    def stop(self):
        """Paro libre (Standby / Coast). El motor gira por inercia hasta detenerse."""
        self.in1.value(0)
        self.in2.value(0)
        self.pwm.duty_u16(0)

    def brake(self):
        """Freno corto (Short Brake). Detiene el motor de golpe."""
        self.in1.value(1)
        self.in2.value(1)
        self.pwm.duty_u16(0)