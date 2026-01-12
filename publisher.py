import random
import time

import paho.mqtt.client as mqtt

broker = "127.0.0.1"
topic = "house/1/room/kitchen/sensor/gas"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker, 1883)

while True:
    gas_value = random.randint(200,600)
    client.publish(topic,gas_value)
    print("gas:",gas_value)
    time.sleep(5)