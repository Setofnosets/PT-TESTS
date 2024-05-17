from umqtt.simple import MQTTClient
from machine import Pin, I2C, ADC, SoftI2C
import ssd1306
import random
import time

def sub_cb(topic, msg):
    print((topic, msg))
    oled = screen()
    oled.fill(0)
    oled.text('Topic: ' + topic.decode('utf-8'), 0, 0)
    msg = msg.decode('utf-8')
    #Split
    msg = msg.split(',')
    oled.text('Msg: ' + msg[0], 0, 20)
    oled.text(msg[1], 0, 30)
    #oled.text('Msg: ' + msg.decode('utf-8'), 0, 10)
    oled.show()
def screen():
    oled_width = 128
    oled_height = 64
    i2c = SoftI2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    return oled

client_name = "LoRa 32"
server = "192.168.1.72"
mqttc = MQTTClient(client_name, server, keepalive=60)
mqttc.connect()
mqttc.set_callback(sub_cb)
mqttc.subscribe("demo")
oled = screen()
oled.fill(0)
oled.text('Subscribed to demo', 0, 0)
oled.show()
while True:
    try:
        mqttc.wait_msg()
    except OSError as e:
        print("Failed to connect, return code %d\n", e)
        time.sleep(5)
        machine.reset()
    except KeyboardInterrupt:
        print("Interrupted")
        break

mqttc.publish("demo", str(random.randint(15, 30)))