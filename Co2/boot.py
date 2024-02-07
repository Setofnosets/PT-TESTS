import machine
import time
import ssd1306
from machine import Pin, I2C, ADC, SoftI2C
import network

SCL = 22
SDA = 21

#def screen():
 #   oled_width = 128
  #  oled_height = 64
   # i2c = SoftI2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
    #oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    #oled.fill(0)
    #oled.text('Connecting...', 0, 0)
    #return oled

#oled = screen()
#oled.fill(0)
#oled.text('Starting', 0, 0)
#oled.show()
print('Starting')

