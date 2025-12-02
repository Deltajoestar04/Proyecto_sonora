# publisher.py 
import paho.mqtt.publish as publish
import time
import random


MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_USERNAME = None
MQTT_PASSWORD = None

NOMBRES_MUNICIPIOS = ["hermosillo", "cajeme", "nogales"]
TIPOS_DATO = ["temperatura", "humedad", "iluminacion"]

TOPICS = [
    f"sonora/{NOMBRES_MUNICIPIOS[0]}/{TIPOS_DATO[0]}",
    f"sonora/{NOMBRES_MUNICIPIOS[1]}/{TIPOS_DATO[1]}",
    f"sonora/{NOMBRES_MUNICIPIOS[2]}/{TIPOS_DATO[2]}"
]

print(f"Publicando datos (con nombres limpios) en {MQTT_BROKER}:{MQTT_PORT}...")

auth = None
if MQTT_USERNAME and MQTT_PASSWORD:
    auth = {'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}

while True:
    try:
        temp = random.uniform(20.0, 40.0)
        hum = random.uniform(30.0, 70.0)
        lux = random.uniform(500, 1500)

      
        publish.single(TOPICS[0], payload=str(round(temp, 2)), hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth)

        publish.single(TOPICS[1], payload=str(round(hum, 2)), hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth)

        publish.single(TOPICS[2], payload=str(round(lux, 2)), hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth)

        print(f"-> Publicados nuevos valores. Temp HLL: {round(temp, 2)} °C")

    except Exception as e:
        print(f"🚨 ERROR PUBLICANDO: {e}")

    time.sleep(5)