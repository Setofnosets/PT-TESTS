from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import dht
import machine
import time

RX = 34
TX = 12
SCL = 22
SDA = 21

def screen():
    oled_width = 128
    oled_height = 64
    i2c = SoftI2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    return oled

oled = screen()

temp = 0
hum = 0

d = dht.DHT11(machine.Pin(4))

while True:
    try:
        d.measure()
        temp = d.temperature()
        hum = d.humidity()
        print(str(temp) + ' ' + str(hum))
        oled.fill(0)
        oled.text('Temp: ' + str(temp) + ' C', 0, 0)
        oled.text('Hum: ' + str(hum) + ' %', 0, 10)
        oled.show()
    except OSError as e:
        print('Failed to read sensor.')
    time.sleep(2)
