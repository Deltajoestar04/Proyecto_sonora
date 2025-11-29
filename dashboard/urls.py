from django.contrib import admin
from django.urls import path, include
from monitoreo import views as monitoreo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', monitoreo_views.dashboard_index),
    path('dashboard/', monitoreo_views.dashboard_index, name='dashboard'),
    path('api/lecturas/', monitoreo_views.api_lecturas, name='api_lecturas'),
]
