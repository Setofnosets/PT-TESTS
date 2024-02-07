from paho.mqtt import client as mqtt_client
import random
import time
import threading

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def publish(ID):
    client = connect_mqtt()
    client.loop_start()
    while True:
        time.sleep(1)
        msg = str(random.randint(15, 30))+', from: '+str(ID)
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

broker = '192.168.1.72'
port = 1883
topic = "demo"

for i in range(5):
    client_id = f'{random.randint(0, 100)}'
    print(str(random.randint(15, 30))+', from: '+str(client_id))
    threading.Thread(target=publish, args=(client_id,)).start()

