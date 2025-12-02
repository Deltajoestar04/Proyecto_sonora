from django.contrib import admin
from .models import SensorData

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'municipio', 'tipo_dato', 'value', 'topic')
    list_filter = ('municipio', 'tipo_dato')
    search_fields = ('municipio', 'topic')
    readonly_fields = ('timestamp', 'topic', 'municipio', 'tipo_dato', 'value')