from django.db import models
from django.contrib.auth.models import User

class ZonaCritica(models.Model):
    nombre_zona = models.CharField(max_length=100)
    descripcion = models.TextField()
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    tipo_problema = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_zona

class CamaraSeguridad(models.Model):
    ubicacion = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    modelo_ia = models.CharField(max_length=50)

    def __str__(self):
        return self.ubicacion

class Vehiculo(models.Model):
    tipo = models.CharField(max_length=50)
    camara_id = models.IntegerField()

class SeguimientoVehiculo(models.Model):
    fecha_hora = models.DateTimeField()
    velocidad_detectada = models.DecimalField(max_digits=5, decimal_places=2)
    camara_id = models.IntegerField()
    vehiculo_id = models.IntegerField()

class TraficoTiempoReal(models.Model):
    fecha_hora = models.DateTimeField()
    nivel_congestion = models.CharField(max_length=50)
    cantidad_vehiculos = models.IntegerField()
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

class Semaforo(models.Model):
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=10)

class Accidente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    camara = models.ForeignKey(CamaraSeguridad, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_hora = models.DateTimeField()
    descripcion = models.TextField()
    vehiculos_involucrados = models.IntegerField()
    gravedad = models.CharField(max_length=50)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    altitud = models.DecimalField(max_digits=10, decimal_places=6)