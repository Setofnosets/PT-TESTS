import machine
import time
import ssd1306
from machine import Pin, I2C, ADC, SoftI2C
import network

SCL = 22
SDA = 21

def screen():
    oled_width = 128
    oled_height = 64
    i2c = SoftI2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    return oled

def do_connect():
    oled = screen()
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        oled.text('connecting to network...', 0, 0)
        oled.show()
        sta_if.active(True)
        sta_if.connect('INFINITUMFE9D_2.4', 'u5YK4Z49Rt')
        while not sta_if.isconnected():
            pass
    oled.fill(0)
    print('network config:', sta_if.ifconfig())
    oled.text('IP: ' + sta_if.ifconfig()[0], 0, 0)
    oled.show()

do_connect()

