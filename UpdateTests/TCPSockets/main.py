from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import time, utime
import socket
import select
import network

SCL = 22
SDA = 21
I2CBUS = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
x = 1

def screen():
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, I2CBUS)
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    return oled

oled = screen()

s = socket.socket()
port = 49152
s.connect(('192.168.1.72', port))
print('Connected to server')

poller = select.poll()
poller.register(s, select.POLLIN)

while True:

    y = poller.poll(1000) #Espera 1 segundo
    if not y:
        print(x)
        oled.fill(0)
        oled.text('x: ' + str(x), 0, 0)
        oled.show()
        continue
    else:
        x = s.recv(1024).decode()
        print(x)
        oled.fill(0)
        oled.text('x: ' + str(x), 0, 0)
        oled.show()
        continue

