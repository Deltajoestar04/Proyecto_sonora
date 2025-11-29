import os
import django
import json
import time
import paho.mqtt.client as mqtt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from monitoreo.models import Lectura
import logging
logger = logging.getLogger(__name__)

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "sonora/#"

def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT, rc=", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8', errors='ignore')
    print("Mensaje:", msg.topic, payload)
    try:
        data = json.loads(payload)
    except Exception:
        data = {"raw": payload}

    lect = Lectura()
    # mapea campos como en run_mqtt.py
    if hasattr(lect, 'valor'):
        val = None
        if isinstance(data, dict):
            val = data.get('valor') or data.get('value') or data.get('reading')
        if val is None and 'raw' in data:
            try:
                val = float(data['raw'])
            except:
                val = None
        try:
            lect.valor = float(val) if val is not None else None
        except:
            pass
    if hasattr(lect, 'topic'):
        lect.topic = msg.topic
    if hasattr(lect, 'raw'):
        lect.raw = payload
    lect.save()
    print("Guardado lectura id=", lect.pk)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
