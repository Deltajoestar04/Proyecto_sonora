# monitoreo/admin.py

from django.contrib import admin
from .models import Lectura

class LecturaAdmin(admin.ModelAdmin):

    list_display = ('id', 'municipio', 'tipo', 'valor', 'timestamp')
    list_filter = ('municipio', 'tipo', 'timestamp')
    search_fields = ('municipio', 'tipo')
    ordering = ('-timestamp',)


admin.site.register(Lectura, LecturaAdmin)