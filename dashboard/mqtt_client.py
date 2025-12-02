import paho.mqtt.client as mqtt
import json
from datetime import datetime
import threading
import time
import os

# Cache
REALTIME_CACHE = {}

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "sonora/#"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        parts = msg.topic.split('/')
        if len(parts) < 3 or parts[0] != 'sonora':
            return

        municipio = parts[1].lower()
        tipo_dato = parts[2].lower()

        value = float(msg.payload.decode('utf-8'))
        cache_key = f"{municipio}/{tipo_dato}"

        REALTIME_CACHE[cache_key] = {
            'topic': msg.topic,
            'municipio': municipio,
            'tipo_dato': tipo_dato,
            'value': value,
            'timestamp': datetime.now().isoformat(),
        }

        from monitoreo.models import SensorData
        SensorData.objects.create(
            topic=msg.topic,
            municipio=municipio,
            tipo_dato=tipo_dato,
            value=value
        )

    except Exception:
        pass


def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        thread = threading.Thread(target=client.loop_forever, name='MQTT-Client-Thread')
        thread.daemon = True
        thread.start()
    except Exception:
        pass
