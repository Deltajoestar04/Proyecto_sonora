# mqtt_client.py
import os
import time
import json
try:
    import paho.mqtt.client as mqtt
except Exception as e:
    print('paho-mqtt not installed. Install with pip install paho-mqtt')
    raise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
import django
django.setup()

from monitoreo.models import Lectura

BROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'sonora/#'

client_id = f'django-mqtt-{int(time.time())%10000}'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Conectado al broker MQTT')
        client.subscribe(TOPIC)
        print('Suscrito a', TOPIC)
    else:
        print('Error de conexión, rc=', rc)

def on_message(client, userdata, msg):
    try:
        topic = msg.topic  # e.g., 'sonora/Hermosillo/temperatura'
        payload = msg.payload.decode('utf-8').strip()
        parts = topic.split('/')
        municipio = parts[1] if len(parts) > 1 else 'unknown'
        tipo = parts[2] if len(parts) > 2 else 'valor'
        try:
            valor = float(payload)
        except:
            try:
                data = json.loads(payload)
                valor = float(data.get('valor', 0))
            except:
                print('No se pudo parsear payload:', payload)
                return
        dp = Lectura(municipio=municipio, tipo=tipo, valor=valor)
        dp.save()
        print('Guardado:', dp)
    except Exception as e:
        print('Error procesando mensaje:', e)

def start():
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print('Error conectando al broker:', e)
        return
    client.loop_forever()

if __name__ == '__main__':
    start()
