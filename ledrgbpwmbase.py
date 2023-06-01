import time
from machine import PWM, Pin

red = PWM(Pin(22), freq=1000, duty_u16=0)
blue = PWM(Pin(3), freq=1000, duty_u16=0)
green = PWM(Pin(1), freq=1000, duty_u16=0)


# while True:
#     for i in range(257):
#         red.duty_u16(i*255)
#         time.sleep_ms(100)
#     red.duty_u16(0)
#     for j in range(257):
#         blue.duty_u16(j*255)
#         time.sleep_ms(100)
#     blue.duty_u16(0)
#     for k in range(257):
#         green.duty_u16(k*255)
#         time.sleep_ms(100)
#     green.duty_u16(0)
red.duty_u16(127*257)
green.duty_u16(0*257)
blue.duty_u16(87*257)
