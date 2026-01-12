import threading

import paho.mqtt.client as mqtt
from flask import Flask, jsonify

import mqtt_config

app = Flask(__name__)


alerts = []

# Thresholds for sensor alerts
THRESHOLDS = {
    "gas": 400,
    "temp": 50,
    "smoke": 1
}

# -------------------------------
# Existing sensor alert handler
# -------------------------------
def on_message(client, userdata, msg):
    topic_parts = msg.topic.split("/")
    house_id = topic_parts[1]
    room = topic_parts[3]
    sensor = topic_parts[5]

    try:
        value = int(msg.payload.decode())
    except ValueError:
        print(f"⚠ Invalid payload for {msg.topic}: {msg.payload}")
        return

    if sensor in THRESHOLDS and value > THRESHOLDS[sensor]:
        alert = {
            "house": house_id,
            "room": room,
            "sensor": sensor,
            "value": value,
            "message": f"{sensor.upper()} ALERT in {room}"
        }
        alerts.append(alert)
        print("🚨 ALERT:", alert)

# -------------------------------
# Worker to handle sensor messages
# -------------------------------
def mqtt_worker():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(mqtt_config.MQTT_BROKER, mqtt_config.MQTT_PORT)
    client.subscribe(mqtt_config.MQTT_SENSOR_TOPIC)
    client.loop_forever()

# -------------------------------
# Worker to log client connections (human-readable)
# -------------------------------
def on_sys_message(client, userdata, msg):
    # Example topic: $SYS/broker/clients/expo_1/connected
    topic_parts = msg.topic.split("/")
    if len(topic_parts) >= 5:
        client_id = topic_parts[3]
        action = topic_parts[4]  # connected or disconnected
        print(f"📡 Client {client_id} has {action} the broker")
    else:
        print(f"📡 SYS EVENT: {msg.topic} → {msg.payload.decode()}")

def sys_worker():
    sys_client = mqtt.Client()
    sys_client.on_message = on_sys_message
    sys_client.connect(mqtt_config.MQTT_BROKER, mqtt_config.MQTT_PORT)
    # Subscribe to all client events
    sys_client.subscribe(mqtt_config.MQTT_SYS_TOPIC_CONNECTED)
    sys_client.subscribe(mqtt_config.MQTT_SYS_TOPIC_DISCONNECTED)
    sys_client.loop_forever()

# -------------------------------
# Flask endpoint for alerts
# -------------------------------
@app.route("/alerts")
def get_alerts():
    return jsonify(alerts)

# -------------------------------
# Start everything
# -------------------------------
if __name__ == "__main__":
    # Start MQTT worker for sensor messages
    threading.Thread(target=mqtt_worker, daemon=True).start()
    # Start MQTT worker for client connection logs
    threading.Thread(target=sys_worker, daemon=True).start()
    # Start Flask server
    app.run(host="0.0.0.0", port=5000)
  
