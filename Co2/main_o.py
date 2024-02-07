from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import time, utime

RXD = 3
TXD = 1
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

oled = screen()

CO2 = UART(1, baudrate=9600, tx=Pin(TXD), rx=Pin(RXD), timeout=30000, stop=1, parity=None, flow=0)

buffer = bytearray(4)

#CM1107N
def read_co2():
    CO2.write(b'\x11\x01\x01\xED')
    print("Sent: 0x11 0x01 0x01 0xED")
    time.sleep(3)
    oled.fill(0)
    oled.text("Sent: 0x11 0x01 0x01 0xED", 0, 0)
    oled.show()
    time.sleep(0.1)
    status = CO2.readinto(buffer)
    print("buffer: " + str(buffer))
    oled.text("buffer: " + str(buffer), 0, 10)
    oled.text("buffer[0]: " + str(buffer[0]), 0, 20)
    oled.text("buffer[1]: " + str(buffer[1]), 0, 30)
    oled.text("status: " + str(status), 0, 40)
    oled.show()
    if (buffer[0] == 0x16 ):
        return buffer[2] * 256 + buffer[3]
    return -1

while True:
    oled.fill(0)
    oled.text("CO2: " + str(read_co2()) + " ppm", 0, 0)
    #print(read_co2())
    oled.show()
    time.sleep(1)
