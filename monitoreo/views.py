# monitoreo/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SensorData
from dashboard.mqtt_client import REALTIME_CACHE
import json


def dashboard_view(request):
    """Vista principal del dashboard."""
    municipios = SensorData.objects.values_list('municipio', flat=True).distinct()
    context = {'municipios': sorted(list(municipios))}
    return render(request, 'monitoreo/dashboard.html', context)


def municipio_view(request, municipio_name):
    """Vista con historial de datos para un municipio."""
    historial_data = (
        SensorData.objects
        .filter(municipio__iexact=municipio_name)
        .order_by('-timestamp')[:100]
    )
    context = {
        'municipio_name': municipio_name.capitalize(),
        'historial_data': historial_data
    }
    return render(request, 'monitoreo/municipios.html', context)


def realtime_data_api(request):
    """API que devuelve datos en tiempo real desde el cache MQTT."""
    return JsonResponse(REALTIME_CACHE, safe=False)
