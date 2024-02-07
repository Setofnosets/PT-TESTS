import random
from time import sleep
from lora import LoRa
from machine import Pin, SPI

def screen():
    oled_width = 128
    oled_height = 64
    i2c_rst = Pin(16, Pin.OUT)
    i2c_rst.value(0)
    time.sleep_ms(5)
    i2c_rst.value(1)
    i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
    i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
    i2c = I2C(scl=i2c_scl, sda=i2c_sda)
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    return oled

oled = screen()
oled.fill(0)
SCK = 5
MOSI = 27
MISO = 19
# Chip select
CS = 18
# Receive IRQ
RX = 3
print("Initializing LoRa...")

spi = SPI(
    1,
    baudrate=10000000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP),
)
spi.init()

lora = LoRa(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    frequency=915E6,
    sync_word=0xF3,
)

def handler(x):
    print(x)
    oled.fill(0)
    oled.text(x, 0, 0)

lora.on_recv(handler)
lora.recv()