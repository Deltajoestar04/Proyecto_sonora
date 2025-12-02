# monitoreo/apps.py
from django.apps import AppConfig
import os
from dashboard.mqtt_client import start_mqtt_client

class MonitoreoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoreo'

    def ready(self):
        """Inicializa el cliente MQTT cuando la app carga."""
        if os.environ.get('WERKZEUG_RUN_MAIN') is None:
            start_mqtt_client()
