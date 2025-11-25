from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/latest/', views.latest_data, name='api_latest'),
]
