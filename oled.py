from machine import Pin, SPI, ADC
import ssd1306, time

vspi = SPI(2, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

dc = Pin(16)   # data/command
rst = Pin(17)  # reset
cs = Pin(5)  # chip select, some modules do not have a pin for this

display = ssd1306.SSD1306_SPI(128, 64, vspi, dc, rst, cs)

adc =ADC(Pin(2))
adc.atten(ADC.ATTN_11DB)
#display.text('Hello', 0, 0)
#display.text('World', 0, 10)
#display.fill(1) todos los pixeles encendidos
'''
display.fill(0)
display.fill_rect(0, 0, 32, 32, 1)
display.fill_rect(2, 2, 28, 28, 0)
display.vline(9, 8, 22, 1)
display.vline(16, 2, 22, 1)
display.vline(23, 8, 22, 1)
display.fill_rect(26, 24, 2, 4, 1)
display.text('MicroPython', 40, 0, 1)
display.text('SSD1306', 40, 12, 1)
display.text('OLED 128x64', 40, 24, 1)
'''

'''
display.fill(1)
display.fill_rect(0, 0, 32, 32, 0)
display.fill_rect(2, 2, 28, 28, 1)
display.vline(9, 8, 22, 0)
display.vline(16, 2, 22, 0)
display.vline(23, 8, 22, 0)
display.fill_rect(26, 24, 2, 4, 0)
display.text('MicroPython', 40, 0, 0)
display.text('SSD1306', 40, 12, 0)
display.text('OLED 128x64', 40, 24, 0)
'''
while (True):
    display.fill(0)
    v = adc.read()
    a="holi"
    t="papu"
    display.text(a, 0, 0)
    display.text(t, 0, 10)
    display.text(str(round(v,1)), 0, 20)
    display.show()
    time.sleep_ms(100)
