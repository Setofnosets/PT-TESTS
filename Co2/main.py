from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import time, utime
from CO2 import *

SCL = 22
SDA = 21
I2CBUS = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)

#def screen():
    #oled_width = 128
    #oled_height = 64
    #oled = ssd1306.SSD1306_I2C(oled_width, oled_height, I2CBUS)
   # oled.fill(0)
  #  oled.text('Connecting...', 0, 0)
 #   return oled

#oled = screen()

#set pin 0 to low
p0 = Pin(0, Pin.OUT)
p0.value(0)

CO2SENSOR = CO2(I2CBUS)

#read co2
def read_co2():
    return CO2SENSOR.read_co2()

while True:
    print(read_co2())
    #oled.fill(0)
    #oled.text("CO2: " + str(read_co2()) + " ppm", 0, 0)
    #oled.show()
    time.sleep(1)
