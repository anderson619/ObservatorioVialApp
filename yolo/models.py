from django.db import models

class TraficoTiempoReal(models.Model):
    fecha_hora = models.DateTimeField()
    nivel_congestion = models.CharField(max_length=50)
    cantidad_vehiculos = models.IntegerField()
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        app_label = 'yolo'
        db_table = 'movilidad_traficotiemporeal'
        managed = False

    def __str__(self):
        return f"{self.fecha_hora} - {self.nivel_congestion}"

class Vehiculo(models.Model):
    tipo = models.CharField(max_length=50)
    camara_id = models.IntegerField()

    class Meta:
        app_label = 'yolo'
        db_table = 'movilidad_vehiculo'
        managed = False

    def __str__(self):
        return self.tipo

class SeguimientoVehiculo(models.Model):
    fecha_hora = models.DateTimeField()
    velocidad_detectada = models.DecimalField(max_digits=5, decimal_places=2)
    camara_id = models.IntegerField()
    vehiculo_id = models.IntegerField()

    class Meta:
        app_label = 'yolo'
        db_table = 'movilidad_seguimientovehiculo'
        managed = False

    def __str__(self):
        return f"{self.fecha_hora} - {self.velocidad_detectada} km/h"