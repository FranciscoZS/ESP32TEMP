from machine import Pin, I2C, ADC
from utime import sleep_ms
from ssd1306 import SSD1306_I2C

def plot_time(yp, t, x, y, var = [0.0,3.3], vpts=[25,16,40], hpts=[25,55,112]):
   oled.vline(vpts[0], vpts[1], vpts[2],1)
   oled.hline(hpts[0], hpts[1], hpts[2],1)
   oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
   oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
   
   y[1] = int((yp-var[0])/(var[1]-var[0])*(vpts[1]-hpts[1])+hpts[1])
   if t<hpts[2]-hpts[0]:
       x[1]=x[0]+1
   else: 
        x[1] = hpts[2]
    
   oled.line(x[0],y[0],x[1],y[1],1)
   oled.show()
    
   y[0] = y[1]
   x[0] = x[1]
    
   if t > hpts[2]-hpts[0]:
        oled.fill_rect(vpts[0],vpts[1],2,vpts[2],0)
        oled.fill_rect(vpts[0]-25,vpts[1],vpts[0],vpts[2]+5,0)
        oled.scroll(-1,0)
        oled.vline(vpts[0], vpts[1], vpts[2], 1)
        oled.hline(hpts[0], hpts[1], hpts[2], 1)
        oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
        oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
   else:
        t += 1
   return t,x,y

if __name__ == '__main__':
    WIDTH = 128
    HEIGHT = 64
    FACTOR = 3.3/(4095)
    
    i2c = I2C(scl=Pin(22), sda=Pin(21))
    pot = ADC(Pin(2))
    
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    
    t=0
    y = [55,55]
    x = [25,25]
    
    
    oled.fill(0)
    
    while True:

        volts = pot.read()*FACTOR
        t,x,y = plot_time(volts,t,x,y)
        oled.fill_rect(0,0,120,15,0)
        oled.text("volts: ",0,0)
        oled.text(str(round(volts,1)),52,0)
        oled.show()
        sleep_ms(100)
       
        
   

