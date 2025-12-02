# monitoreo/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SensorData
from dashboard.mqtt_client import REALTIME_CACHE
from datetime import datetime
import json


def dashboard_view(request):
    """
    Vista principal del dashboard. Obtiene la lista de municipios únicos.
    """
    try:
        municipios = SensorData.objects.values_list('municipio', flat=True).distinct().order_by('municipio')

    except Exception as e:
        print(f"Error al obtener municipios de la BD: {e}")
        municipios = []

    context = {
        'municipios': municipios
    }
    return render(request, 'monitoreo/dashboard.html', context)


def municipio_view(request, municipio_name):
    """
    Vista detallada por municipio, separa datos para la tabla (objetos datetime)
    y para la gráfica (strings JSON).
    """

    historial_base_queryset = SensorData.objects.filter(municipio__iexact=municipio_name).order_by('-timestamp')[:100]
    historial_tabla = historial_base_queryset
    historial_json = list(historial_base_queryset.values('topic', 'municipio', 'tipo_dato', 'value', 'timestamp'))

    for item in historial_json:
        if isinstance(item['timestamp'], datetime):
            item['timestamp'] = item['timestamp'].isoformat()

    context = {
        'municipio_name': municipio_name.capitalize(),
        'historial_tabla': historial_tabla,
        'historial_json': historial_json
    }
    return render(request, 'monitoreo/municipios.html', context)


def realtime_data_api(request):
    """
    API que sirve los datos en tiempo real desde el cache MQTT.
    """
    return JsonResponse(REALTIME_CACHE, safe=False)