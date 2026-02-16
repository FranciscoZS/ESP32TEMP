from machine import I2C, Pin
import struct

class MPU9250:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.addr = address
        # Despertar el sensor (salir de sleep mode)
        self.write_reg(0x6B, 0x00)
        
    def write_reg(self, reg, data):
        self.i2c.writeto_mem(self.addr, reg, bytes([data]))

    def read_regs(self, reg, count):
        return self.i2c.readfrom_mem(self.addr, reg, count)

    def get_accel(self):
        """Retorna (x, y, z) del acelerómetro en Gs."""
        data = self.read_regs(0x3B, 6)
        # 'h' significa signed short (16 bits)
        # '>' significa Big Endian (formato del MPU9250)
        ax, ay, az = struct.unpack('>hhh', data)
        # Escala por defecto: 2G -> 16384 LSB/g
        return ax / 16384.0, ay / 16384.0, az / 16384.0

    def get_gyro(self):
        """Retorna (x, y, z) del giroscopio en grados/seg."""
        data = self.read_regs(0x43, 6)
        gx, gy, gz = struct.unpack('>hhh', data)
        # Escala por defecto: 250 dps -> 131 LSB/dps
        return gx / 131.0, gy / 131.0, gz / 131.0

    def get_temp(self):
        """Retorna la temperatura interna en grados Celsius."""
        data = self.read_regs(0x41, 2)
        temp = struct.unpack('>h', data)[0]
        return (temp / 333.87) + 21.0