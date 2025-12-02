# dashboard/mqtt_client.py
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import threading
import os
from django.conf import settings
import random
import string
from .mqtt_utils import connect_mqtt

# Generar un Client ID único
CLIENT_ID = "Django_Sonora_" + "".join(random.choices(string.ascii_letters + string.digits, k=8))

# Cache
REALTIME_CACHE = {}


def on_connect(client, userdata, flags, rc):
    """Callback que suscribe al tópico después de una conexión exitosa."""
    if rc == 0:
        client.subscribe(settings.MQTT_TOPIC)
        print(f"MQTT: Suscrito al tópico: {settings.MQTT_TOPIC}")


def on_message(client, userdata, msg):
    """Callback para cuando se recibe un mensaje MQTT."""
    try:
        parts = msg.topic.split('/')
        if len(parts) < 3 or parts[0] != 'sonora':
            return

        municipio_raw = parts[1]
        tipo_dato = parts[2].lower()

    
        cleaned_temp = municipio_raw.encode('ascii', 'ignore').decode('ascii')
        municipio_clean = ''.join(c for c in cleaned_temp if c.isalnum() or c.isspace()).lower().strip()
        municipio = municipio_clean

        payload = msg.payload.decode('utf-8')
        value = float(payload)

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

    except ValueError:
        pass
    except Exception as e:
        print(f"Error en on_message: {e}")


def start_mqtt_client():
    """Inicia el cliente MQTT usando la función de utilidad y settings."""

    client = connect_mqtt(
        broker=settings.MQTT_BROKER,
        port=settings.MQTT_PORT,
        client_id=CLIENT_ID,
        username=settings.MQTT_USERNAME,
        password=settings.MQTT_PASSWORD
    )

    if client:
        client.on_message = on_message
        client.on_connect = on_connect

        try:
            thread = threading.Thread(target=client.loop_forever, name='MQTT-Client-Thread')
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"MQTT: Error al iniciar hilo de loop: {e}")