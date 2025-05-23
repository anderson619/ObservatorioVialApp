from django.contrib import admin
from .models import ZonaCritica, CamaraSeguridad, Vehiculo, SeguimientoVehiculo, TraficoTiempoReal, Semaforo, Accidente

admin.site.register(ZonaCritica)
admin.site.register(CamaraSeguridad)
admin.site.register(Vehiculo)
admin.site.register(SeguimientoVehiculo)
admin.site.register(TraficoTiempoReal)
admin.site.register(Semaforo)
admin.site.register(Accidente)
