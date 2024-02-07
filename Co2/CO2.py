from machine import I2C
import time

HW_ADDRESS = const(0x31)
READCO2 = const(0x01)
SETABC = const(0x10)
CALIBRATE = const(0x03)
SENSORSV   = const(0x1E)
SENSORSN   = const(0x1F)

SVLENGTH   = const(0x0A)
SNLENGTH   = const(0x0A)

DATAFRAMELENGTH = const(0x05)
SNFRAMELENGTH = const(0x0C)
SVFRAMELENGTH = const(0x0C)
CALIBRATIONFRAMELENGTH = const(0x04)

class CO2:
    def __init__(self, i2c):
        self.i2c = i2c
        self.buffer = bytearray(12)
        self.status = 0
        self.co2 = 0
        self.abc = 0
        self.sn = bytearray(12)
        self.sv = bytearray(12)

    def read_co2(self):
        print(self.i2c.scan())
        self.i2c.writeto_mem(HW_ADDRESS, READCO2, bytearray([0x01, 0x01, 0xED]))
        time.sleep(3)
        self.status = self.i2c.readfrom_into(HW_ADDRESS, self.buffer)
        print("buffer: " + str(self.buffer))
        if (self.buffer[0] == 0x01 ):
            self.co2 = self.buffer[1] * 256 + self.buffer[2]
        else:
            self.co2 = -1
        return self.co2

    def read_abc(self):
        self.i2c.writeto(HW_ADDRESS, bytearray([SETABC, 0x01, 0x01, 0xED]))