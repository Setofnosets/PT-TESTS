from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import dht
import machine
import time
import socket
import select

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
    oled.text('Connecting...', 0, 0)
    return oled

def measure_temp():
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    print(str(temp) + ' ' + str(hum))
    oled.fill(0)
    oled.text('Temp: ' + str(temp) + ' C', 0, 0)
    oled.text('Hum: ' + str(hum) + ' %', 0, 10)
    oled.show()

oled = screen()

measure_interval = 1 #default interval
temp = 0
hum = 0

d = dht.DHT11(machine.Pin(4))

#Create server socket
serversocket = socket.socket()

#Bind to port
port = 49152
serversocket.bind(('', port))

#Start listening
serversocket.listen(0)

#Accept a connection
serversocket.setblocking(False)
#c, addr = serversocket.accept()
#print('Got connection from', addr)

poller = select.poll()
#poller.register(c, select.POLLIN)
c = None
#Main loop
while True:
    try:
        #If connection is lost, try to accept a new one
        if not c:
            measure_temp()

            c, addr = serversocket.accept()
            print('Got connection from', addr)
            poller.register(c, select.POLLIN)

            time.sleep(measure_interval)
            continue
        else:
            # Poll and wait for specified time
            y = poller.poll(measure_interval * 1000)

            # If no data is received, measure temperature and humidity
            if not y:
                measure_temp()
                continue
            else:
                # If data is received, print it
                x = c.recv(1024).decode()
                print(x)
                oled.fill(0)
                oled.text('Interval: ' + str(x), 0, 0)
                oled.show()
                measure_interval = int(x)

                measure_temp()
                continue
    except OSError as e:
        c = None
        if e.args[0] == 11:
            print('No connection available')
            continue
