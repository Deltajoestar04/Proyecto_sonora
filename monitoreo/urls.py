from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/realtime_data/', views.realtime_data_api, name='realtime_data_api'),
    path('municipio/<str:municipio_name>/', views.municipio_view, name='municipio_detail'),
]