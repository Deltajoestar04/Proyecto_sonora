# monitoreo/views.py
from django.http import JsonResponse
from django.shortcuts import render
from .models import Lectura
from django.views.decorators.http import require_GET
import datetime

@require_GET
def api_lecturas(request):

    qs = Lectura.objects.all().order_by('id')  # cambia ordering si prefieres por fecha
    data = []
    for obj in qs:

        item = {}
        for field in obj._meta.get_fields():
            if hasattr(field, 'attname'):
                name = field.attname
                try:
                    value = getattr(obj, name)
                except Exception:
                    value = None
                if isinstance(value, datetime.datetime):
                    value = value.isoformat()
                item[name] = value
        data.append(item)
    return JsonResponse(data, safe=False)


def dashboard_index(request):

    return render(request, "dashboard/index.html")
