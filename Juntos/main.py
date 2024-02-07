from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import dht
import machine
import time, utime
from AXP2101 import *
from CO2 import *

RX = 34
TX = 12
SCL = 22
SDA = 21
I2CBUS = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
gps = UART(1, baudrate=9600, rx=RX, tx=TX)
p0 = Pin(0, Pin.OUT)
p0.value(0)
buffer = bytearray(255)
TIMEOUT = False
FIX_STATUS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""

CO2SENSOR = CO2(I2CBUS)

def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime

    timeout = time.time() + 8
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
        """if (parts[0] == "b'$GPGGA"):
            oled.fill(0)
            oled.text("GPS found", 0, 0)
            oled.text(parts[0], 0, 10)
            oled.text(parts[1], 0, 20)
            oled.text(parts[2], 0, 30)
            oled.text(parts[3], 0, 40)
            oled.text(parts[4], 0, 50)
            print(parts)
            oled.show()"""

        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)

                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = "-"+longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break

        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)

def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat / 100)
    nexttwodigits = RawAsFloat - float(firstdigits * 100)

    Converted = float(firstdigits + nexttwodigits / 60.0)
    Converted = '{0:.6f}'.format(Converted)
    return str(Converted)

def screen():
    oled_width = 128
    oled_height = 64
    i2c = SoftI2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    return oled

oled = screen()

temp = 0
hum = 0

d = dht.DHT11(machine.Pin(4))
PMU = AXP2101(I2CBUS, addr=AXP2101_SLAVE_ADDRESS)
PMU.enableBattDetection()
PMU.enableVbusVoltageMeasure()
PMU.enableBattVoltageMeasure()
PMU.enableSystemVoltageMeasure()

while True:
    try:
        #Measure the temperature and the humidity of the room
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

    #Measure Battery
    voltage = PMU.getBattVoltage()
    print('Battery voltage: ', voltage, 'V')
    percent = PMU.getBatteryPercent()
    print('Battery percent: ', percent, '%')
    charge = percent * 3000 / 100
    oled.fill(0)
    oled.text('Voltage: ' + str(voltage) + 'mV', 0, 0)
    oled.text('Percent: ' + str(percent) + '%', 0, 10)
    oled.text('Charge: ' + str(charge) + 'mA', 0, 20)
    oled.show()

    #Measure CO2
    oled.fill(0)
    oled.text("CO2: " + str(CO2SENSOR.read_co2()) + " ppm", 0, 0)
    oled.show()

    #Measure GPS

    getGPS(gps)

    if (FIX_STATUS == True):
        print("Printing GPS data...")
        print(" ")
        print("Latitude: " + latitude)
        print("Longitude: " + longitude)
        print("Satellites: " + satellites)
        print("Time: " + GPStime)
        print("----------------------")

        oled.fill(0)
        oled.text("Lat: " + latitude, 0, 0)
        oled.text("Lng: " + longitude, 0, 10)
        oled.text("Satellites: " + satellites, 0, 20)
        oled.text("Time: " + GPStime, 0, 30)
        oled.show()

        FIX_STATUS = False

    if (TIMEOUT == True):
        print("No GPS data is found.")
        TIMEOUT = False

    time.sleep(2)
