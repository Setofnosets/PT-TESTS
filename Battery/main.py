from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import time, utime
from AXP2101 import *


SCL = 22
SDA = 21
IRQ = 35
I2CBUS = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)

def screen():
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, I2CBUS)
    oled.fill(0)
    return oled

oled = screen()

PMU = AXP2101(I2CBUS, addr=AXP2101_SLAVE_ADDRESS)
PMU.enableBattDetection()
PMU.enableVbusVoltageMeasure()
PMU.enableBattVoltageMeasure()
PMU.enableSystemVoltageMeasure()

while True:
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
    time.sleep(2)

