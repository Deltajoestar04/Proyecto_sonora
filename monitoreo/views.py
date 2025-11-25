from django.shortcuts import render
from django.http import JsonResponse
from .models import Lectura

def dashboard(request):
    return render(request, 'monitoreo/dashboard.html')

def latest_data(request):
    municipio = request.GET.get('municipio')
    tipo = request.GET.get('tipo')
    limit = int(request.GET.get('limit', '50'))
    qs = Lectura.objects.all()
    if municipio:
        qs = qs.filter(municipio__iexact=municipio)
    if tipo:
        qs = qs.filter(tipo__iexact=tipo)
    qs = qs.order_by('-timestamp')[:limit]
    data = [
        {'municipio': d.municipio, 'tipo': d.tipo, 'valor': d.valor, 'timestamp': d.recibido_en.isoformat()}
        for d in reversed(qs)
    ]
    return JsonResponse({'data': data})
