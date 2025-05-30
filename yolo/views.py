from django.shortcuts import render

from django.shortcuts import render
from yolo.models import TraficoTiempoReal
from django.shortcuts import render
from yolo.models import SeguimientoVehiculo

def trafico_tiempo_real(request):
    datos = TraficoTiempoReal.objects.all().order_by('-fecha_hora')[:20]
    return render(request, 'yolo/trafico_tiempo_real.html', {'datos': datos})

def estadisticas_seguimiento(request):
    datos = SeguimientoVehiculo.objects.order_by('-fecha_hora')[:50]
    return render(request, 'yolo/estadisticas_seguimiento.html', {'datos': datos})