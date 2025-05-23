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

class Vehiculo(models.Model):
    tipo = models.CharField(max_length=50)
    camara_id = models.IntegerField()

    class Meta:
        app_label = 'yolo'
        db_table = 'movilidad_vehiculo'
        managed = False

class SeguimientoVehiculo(models.Model):
    fecha_hora = models.DateTimeField()
    velocidad_detectada = models.DecimalField(max_digits=5, decimal_places=2)
    camara_id = models.IntegerField()
    vehiculo_id = models.IntegerField()

    class Meta:
        app_label = 'yolo'
        db_table = 'movilidad_seguimientovehiculo'
        managed = False