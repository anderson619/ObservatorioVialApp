from django.db import models
from django.contrib.auth.models import User


class ZonaCritica(models.Model):
    nombre_zona = models.CharField(max_length=100)
    descripcion = models.TextField()
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)
    TIPO_PROBLEMA_CHOICES = [
        ('accidentes frecuentes', 'Accidentes frecuentes'),
        ('congestion', 'Congestión'),
        ('infraestructura deficiente', 'Infraestructura deficiente'),
    ]
    tipo_problema = models.CharField(max_length=50, choices=TIPO_PROBLEMA_CHOICES)

    def _str_(self):
        return self.nombre_zona

class CamaraSeguridad(models.Model):
    ubicacion = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    modelo_ia = models.CharField(max_length=50)
    zona_critica = models.ForeignKey(ZonaCritica, on_delete=models.CASCADE)

    def _str_(self):
        return self.ubicacion

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('bus', 'Bus'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    camara = models.ForeignKey(CamaraSeguridad, on_delete=models.SET_NULL, null=True)

class SeguimientoVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    camara = models.ForeignKey(CamaraSeguridad, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    velocidad_detectada = models.DecimalField(max_digits=6, decimal_places=2)

class TraficoTiempoReal(models.Model):
    fecha_hora = models.DateTimeField()
    nivel_congestion = models.CharField(max_length=10, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')])
    cantidad_vehiculos = models.IntegerField()
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)

class Semaforo(models.Model):
    ubicacion = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)
    tiempo_ciclo = models.IntegerField(help_text='Duración del ciclo en segundos')
    zona_critica = models.ForeignKey(ZonaCritica, on_delete=models.CASCADE)

class Accidente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    camara = models.ForeignKey(CamaraSeguridad, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField()
    descripcion = models.TextField()
    vehiculos_involucrados = models.IntegerField()
    gravedad = models.CharField(max_length=50)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    altitud = models.DecimalField(max_digits=10, decimal_places=6)