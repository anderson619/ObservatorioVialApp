from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('agente/', views.panel_agente, name='panel_agente'),
    path('jefe/', views.panel_jefe, name='panel_jefe'),
    path('adminlocal/', views.panel_adminlocal, name='panel_adminlocal'),
    path('agente/registrar_accidente/', views.registrar_accidente, name='registrar_accidente'),
    path('adminlocal/camaras/nueva/', views.crear_camara, name='crear_camara'),
    path('adminlocal/camaras/editar/<int:camara_id>/', views.editar_camara, name='editar_camara'),
    path('adminlocal/camaras/eliminar/<int:camara_id>/', views.eliminar_camara, name='eliminar_camara'),
    path('adminlocal/zonas/nueva/', views.crear_zona, name='crear_zona'),
    path('adminlocal/zonas/editar/<int:zona_id>/', views.editar_zona, name='editar_zona'),
    path('adminlocal/zonas/eliminar/<int:zona_id>/', views.eliminar_zona, name='eliminar_zona'),
    path('jefe/trafico-tiempo-real/', views.trafico_tiempo_real, name='trafico_tiempo_real'),
    path('jefe/velocidades-detectadas/', views.velocidades_detectadas, name='velocidades_detectadas'),
]