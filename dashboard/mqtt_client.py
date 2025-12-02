# dashboard/mqtt_client.py
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import threading
import time
import os

# Usaremos un diccionario simple para cachear el último valor de cada sensor.
# Formato: {'municipio/tipo_dato': {'value': 25.5, 'timestamp': '...'}, ...}
REALTIME_CACHE = {}
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "sonora/#"


def on_connect(client, userdata, flags, rc):
    """Callback para cuando el cliente recibe una respuesta CONNACK del broker."""
    if rc == 0:
        print("MQTT: Conectado al broker.")
        # Suscribirse al tópico con wildcard 'sonora/#'
        client.subscribe(MQTT_TOPIC)
        print(f"MQTT: Suscrito al tópico: {MQTT_TOPIC}")
    else:
        print(f"MQTT: Falló la conexión, código de retorno {rc}")


def on_message(client, userdata, msg):
    """Callback para cuando un mensaje es recibido."""
    try:
        # El tópico viene como: sonora/municipio/tipo_dato
        parts = msg.topic.split('/')
        if len(parts) < 3 or parts[0] != 'sonora':
            # Ignorar tópicos que no sigan el formato esperado
            return

        municipio = parts[1].lower()
        tipo_dato = parts[2].lower()

        # El payload es el valor (asumimos un número simple)
        payload = msg.payload.decode('utf-8')
        value = float(payload)

        cache_key = f"{municipio}/{tipo_dato}"

        # Actualizar el cache en tiempo real
        REALTIME_CACHE[cache_key] = {
            'topic': msg.topic,
            'municipio': municipio,
            'tipo_dato': tipo_dato,
            'value': value,
            'timestamp': datetime.now().isoformat(),
        }

        # Almacenar en la BD para el historial
        # Se importa localmente para asegurar que Django ya ha cargado sus modelos.
        from monitoreo.models import SensorData
        SensorData.objects.create(
            topic=msg.topic,
            municipio=municipio,
            tipo_dato=tipo_dato,
            value=value
        )

        # print(f"MQTT: Recibido {msg.topic}: {value} | Cache actualizado.")

    except ValueError:
        # print(f"MQTT: Error al convertir el payload a float: {msg.payload.decode()}")
        pass  # Ignorar datos no numéricos
    except Exception as e:
        # print(f"MQTT: Error general al procesar mensaje: {e}")
        pass  # Ignorar errores de BD/otros para mantener el cliente activo


def start_mqtt_client():
    """Inicia el cliente MQTT en un hilo separado."""
    # Intentamos obtener la configuración del broker del settings de Django si existe
    # from django.conf import settings

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # Conexión al broker público de prueba
        client.connect(MQTT_BROKER, MQTT_PORT, 60)

        # Bucle de red en un hilo separado
        thread = threading.Thread(target=client.loop_forever, name='MQTT-Client-Thread')
        thread.daemon = True  # Permite que el hilo muera cuando el programa principal lo haga
        thread.start()

    except Exception as e:
        print(f"MQTT: Error al conectar: {e}")

# NOTA: La llamada a start_mqtt_client() se ha eliminado de aquí y se ha movido
# a monitoreo/apps.py para una inicialización segura.