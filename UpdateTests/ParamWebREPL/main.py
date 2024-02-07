from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import time, utime

SCL = 22
SDA = 21
I2CBUS = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
x = 1

def screen():
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, I2CBUS)
    oled.fill(0)
    return oled

oled = screen()



