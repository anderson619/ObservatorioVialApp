from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AccidenteForm
from movilidad.models import Accidente, CamaraSeguridad, ZonaCritica
from yolo.models import TraficoTiempoReal
from yolo.models import SeguimientoVehiculo
from django import forms
from django.utils.dateparse import parse_date

@login_required
def home(request):
    user = request.user
    if user.groups.filter(name='agente_de_transito').exists():
        return redirect('panel_agente')
    elif user.groups.filter(name='jefe_de_transito').exists():
        return redirect('panel_jefe')
    elif user.groups.filter(name='administrador').exists():
        return redirect('panel_adminlocal')
    else:
        return render(request, 'usuarios/home.html')

# Funciones para verificar roles de usuario
def es_agente(user):
    return user.groups.filter(name='agente_de_transito').exists()

def es_jefe(user):
    return user.groups.filter(name='jefe_de_transito').exists()

def es_adminlocal(user):
    return user.groups.filter(name='administrador').exists()

# Paneles para diferentes roles
@login_required
@user_passes_test(es_agente)
def panel_agente(request):
    accidentes = Accidente.objects.filter(usuario=request.user).order_by('-fecha_hora')
    return render(request, 'usuarios/panel_agente.html', {'accidentes': accidentes})

@login_required
@user_passes_test(es_jefe)
def panel_jefe(request):
    accidentes = Accidente.objects.all().order_by('-fecha_hora')

    gravedad = request.GET.get('gravedad')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    if gravedad:
        accidentes = accidentes.filter(gravedad__icontains=gravedad)
    if desde:
        accidentes = accidentes.filter(fecha_hora__date__gte=parse_date(desde))
    if hasta:
        accidentes = accidentes.filter(fecha_hora__date__lte=parse_date(hasta))

    return render(request, 'usuarios/panel_jefe.html', {
        'accidentes': accidentes,
        'filtros': {
            'gravedad': gravedad,
            'desde': desde,
            'hasta': hasta
        }
    })

@login_required
@user_passes_test(es_jefe)
def trafico_tiempo_real(request):
    datos = TraficoTiempoReal.objects.order_by('-fecha_hora')[:50]  # últimos 50 registros
    return render(request, 'usuarios/trafico_tiempo_real.html', {'datos': datos})

# Formularios para administrador local
class CamaraForm(forms.ModelForm):
    class Meta:
        model = CamaraSeguridad
        fields = ['ubicacion', 'latitud', 'longitud', 'estado', 'modelo_ia']

class ZonaForm(forms.ModelForm):
    class Meta:
        model = ZonaCritica
        fields = ['nombre_zona', 'descripcion', 'latitud', 'longitud', 'tipo_problema']

# Vistas para administrador local
@login_required
@user_passes_test(es_adminlocal)
def panel_adminlocal(request):
    camaras = CamaraSeguridad.objects.all().order_by('ubicacion')
    zonas = ZonaCritica.objects.all().order_by('nombre_zona')
    return render(request, 'usuarios/panel_adminlocal.html', {'camaras': camaras, 'zonas': zonas})

@login_required
@user_passes_test(es_adminlocal)
def crear_camara(request):
    if request.method == 'POST':
        form = CamaraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_adminlocal')
    else:
        form = CamaraForm()
    return render(request, 'usuarios/form_camara.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_adminlocal)
def editar_camara(request, camara_id):
    camara = get_object_or_404(CamaraSeguridad, id=camara_id)
    if request.method == 'POST':
        form = CamaraForm(request.POST, instance=camara)
        if form.is_valid():
            form.save()
            return redirect('panel_adminlocal')
    else:
        form = CamaraForm(instance=camara)
    return render(request, 'usuarios/form_camara.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_adminlocal)
def eliminar_camara(request, camara_id):
    camara = get_object_or_404(CamaraSeguridad, id=camara_id)
    camara.delete()
    return redirect('panel_adminlocal')

@login_required
@user_passes_test(es_adminlocal)
def crear_zona(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_adminlocal')
    else:
        form = ZonaForm()
    return render(request, 'usuarios/form_zona.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_adminlocal)
def editar_zona(request, zona_id):
    zona = get_object_or_404(ZonaCritica, id=zona_id)
    if request.method == 'POST':
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            return redirect('panel_adminlocal')
    else:
        form = ZonaForm(instance=zona)
    return render(request, 'usuarios/form_zona.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_adminlocal)
def eliminar_zona(request, zona_id):
    zona = get_object_or_404(ZonaCritica, id=zona_id)
    zona.delete()
    return redirect('panel_adminlocal')

# Registro de accidente solo para agentes
@login_required
@user_passes_test(es_agente)
def registrar_accidente(request):
    if request.method == 'POST':
        form = AccidenteForm(request.POST)
        if form.is_valid():
            accidente = form.save(commit=False)
            accidente.usuario = request.user
            accidente.save()
            return redirect('panel_agente')
    else:
        form = AccidenteForm()
    return render(request, 'usuarios/registrar_accidente.html', {'form': form})

@login_required
@user_passes_test(es_jefe)
def velocidades_detectadas(request):
    datos = SeguimientoVehiculo.objects.order_by('-fecha_hora')[:50]  # últimos 50 registros
    return render(request, 'usuarios/velocidades_detectadas.html', {'datos': datos})