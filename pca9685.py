# pca9685_esp32.py
from machine import Pin, I2C
import time

class SimpleRGBPCA9685:
    def __init__(self, sda_pin=21, scl_pin=22, freq=100000, address=0x40):
        """
        Inicializa el controlador PCA9685 para ESP32
        
        Args:
            sda_pin: Pin SDA (por defecto GPIO21)
            scl_pin: Pin SCL (por defecto GPIO22)
            freq: Frecuencia I2C (100kHz por defecto, suficiente para PCA9685)
            address: Dirección I2C del PCA9685 (0x40 por defecto)
        """
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=freq)
        self.address = address
        
        # Verificar comunicación
        devices = self.i2c.scan()
        if self.address not in devices:
            raise IOError(f"PCA9685 no encontrado en dirección 0x{self.address:02X}")
        
        # Configurar PCA9685 a 1000Hz para LEDs
        self._write_reg(0x00, 0x10)  # Modo sleep (permite cambiar prescaler)
        time.sleep(0.005)
        
        # Cálculo correcto del prescaler para 1000Hz
        # Fórmula: prescale = round(osc_clock / (4096 * update_rate)) - 1
        # osc_clock = 25MHz, update_rate = 1000Hz
        prescale = int(25000000 / (4096 * 1000) - 1 + 0.5)  # +0.5 para redondeo
        if prescale < 3:
            prescale = 3  # Mínimo según datasheet
        elif prescale > 255:
            prescale = 255  # Máximo según datasheet
            
        self._write_reg(0xFE, prescale)  # Prescaler
        time.sleep(0.005)
        
        # Salir del modo sleep y configurar modo normal
        self._write_reg(0x00, 0x80)  # Auto-incremento habilitado
        time.sleep(0.005)
        
        # Configurar todos los LEDs para que se enciendan en ON=0, OFF=pwm_value
        for channel in range(16):
            self._set_channel_pwm(channel, 0)

    def _write_reg(self, reg, value):
        """Escribe un valor de 8 bits en un registro"""
        self.i2c.writeto_mem(self.address, reg, bytes([value]))

    def _read_reg(self, reg):
        """Lee un valor de 8 bits de un registro"""
        return self.i2c.readfrom_mem(self.address, reg, 1)[0]

    def _write_reg_16(self, reg, value):
        """Escribe un valor de 16 bits en un registro (little endian)"""
        self.i2c.writeto_mem(self.address, reg, bytes([value & 0xFF, value >> 8]))

    def _set_channel_pwm(self, channel, pwm_value):
        """Establece el valor PWM para un canal específico"""
        if pwm_value < 0 or pwm_value > 4095:
            raise ValueError("El valor PWM debe estar entre 0 y 4095")
        
        base = 0x06 + 4 * channel
        # LEDx_ON = 0, LEDx_OFF = pwm_value
        self._write_reg(base, 0x00)         # LEDx_ON_L
        self._write_reg(base + 1, 0x00)     # LEDx_ON_H  
        self._write_reg(base + 2, pwm_value & 0xFF)     # LEDx_OFF_L
        self._write_reg(base + 3, pwm_value >> 8)       # LEDx_OFF_H

    def set_color(self, r_chan, g_chan, b_chan, r, g, b):
        """Establece color RGB (valores 0-100)"""
        def set_chan(chan, val):
            pwm = int(val * 40.95)  # Convertir 0-100 a 0-4095
            self._set_channel_pwm(chan, pwm)

        set_chan(r_chan, r)
        set_chan(g_chan, g)
        set_chan(b_chan, b)

    def clean_color(self, r_chan, g_chan, b_chan):
        """Apaga los canales RGB especificados"""
        self._set_channel_pwm(r_chan, 0)
        self._set_channel_pwm(g_chan, 0)
        self._set_channel_pwm(b_chan, 0)

    def set_pwm(self, channel, value):
        """
        Establece el valor PWM para un canal específico (0-4095)
        
        Args:
            channel: Número de canal (0-15)
            value: Valor PWM (0-4095)
        """
        self._set_channel_pwm(channel, value)

    def set_pwm_percent(self, channel, percent):
        """
        Establece el valor PWM como porcentaje (0-100)
        
        Args:
            channel: Número de canal (0-15)
            percent: Porcentaje (0-100)
        """
        pwm_value = int(percent * 40.95)  # Convertir 0-100 a 0-4095
        self.set_pwm(channel, pwm_value)

    def get_frequency(self):
        """Lee la frecuencia actual configurada del PCA9685"""
        # Entrar en modo sleep para leer prescaler
        old_mode = self._read_reg(0x00)
        self._write_reg(0x00, (old_mode & 0x7F) | 0x10)  # Modo sleep
        time.sleep(0.005)
        
        prescale = self._read_reg(0xFE)
        
        # Restaurar modo anterior
        self._write_reg(0x00, old_mode)
        time.sleep(0.005)
        
        # Calcular frecuencia
        frequency = 25000000.0 / (4096.0 * (prescale + 1))
        return frequency

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del controlador PCA9685
    pca = SimpleRGBPCA9685()
    
    # Verificar frecuencia configurada
    print(f"Frecuencia PCA9685: {pca.get_frequency():.1f} Hz")
    
    # Definir canales RGB (ajustar según tu configuración)
    RED_CHANNEL = 0
    GREEN_CHANNEL = 1
    BLUE_CHANNEL = 2
    
    try:
        # Ejemplo: ciclo de colores RGB a 1000Hz
        while True:
            print("Rojo")
            pca.set_color(RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL, 100, 0, 0)
            time.sleep(1)
            
            print("Verde")
            pca.set_color(RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL, 0, 100, 0)
            time.sleep(1)
            
            print("Azul")
            pca.set_color(RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL, 0, 0, 100)
            time.sleep(1)
            
            print("Blanco")
            pca.set_color(RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL, 100, 100, 100)
            time.sleep(1)
            
            print("Apagar")
            pca.clean_color(RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL)
            time.sleep(1)
            
    except KeyboardInterrupt:
        # Apagar todos los LEDs al salir
        pca.clean_color(RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL)
        print("Programa terminado")