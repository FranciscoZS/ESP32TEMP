
import machine
import time

led = machine.Pin(2, machine.Pin.OUT)

while True:
    led.on()
    time.sleep_ms(100)
    led.off()
    time.sleep_ms(100)
    print("Running")