from machine import Pin, I2C, ADC, SoftI2C

SCL = 22
SDA = 21
IRQ = 35
I2CBUS = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)


print('Starting')

