from django.shortcuts import render

from django.shortcuts import render
from yolo.models import TraficoTiempoReal

def trafico_tiempo_real(request):
    datos = TraficoTiempoReal.objects.all().order_by('-fecha_hora')[:20]
    return render(request, 'yolo/trafico_tiempo_real.html', {'datos': datos})