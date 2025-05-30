from django.urls import path
from . import views

urlpatterns = [
    path('trafico-tiempo-real/', views.trafico_tiempo_real, name='trafico_tiempo_real'),
    path('estadisticas-seguimiento/', views.estadisticas_seguimiento, name='estadisticas_seguimiento'),
]