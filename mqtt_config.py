MQTT_BROKER = "1270.0.1"
MQTT_PORT = 1883

# MQTT_SENSOR_TOPIC = "house/1/room/kitchen/sensor/gas"
MQTT_SENSOR_TOPIC = "house/+/room/+/sensor/+"  #dynamic topic type "+" can be replaced with any word or number


MQTT_SYS_TOPIC_CONNECTED = "$SYS/broker/clients/+/connected"
MQTT_SYS_TOPIC_DISCONNECTED = "$SYS/broker/clients/+/disconnected"