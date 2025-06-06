# Generated by Django 5.2.1 on 2025-05-17 22:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CamaraSeguridad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', models.CharField(max_length=100)),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], max_length=10)),
                ('modelo_ia', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TraficoTiempoReal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('nivel_congestion', models.CharField(choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')], max_length=10)),
                ('cantidad_vehiculos', models.IntegerField()),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ZonaCritica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_zona', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('tipo_problema', models.CharField(choices=[('accidentes frecuentes', 'Accidentes frecuentes'), ('congestion', 'Congestión'), ('infraestructura deficiente', 'Infraestructura deficiente')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Accidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('descripcion', models.TextField()),
                ('vehiculos_involucrados', models.IntegerField()),
                ('gravedad', models.CharField(max_length=50)),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('altitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('camara', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movilidad.camaraseguridad')),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('carro', 'Carro'), ('moto', 'Moto'), ('bus', 'Bus')], max_length=10)),
                ('camara', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movilidad.camaraseguridad')),
            ],
        ),
        migrations.CreateModel(
            name='SeguimientoVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('velocidad_detectada', models.DecimalField(decimal_places=2, max_digits=6)),
                ('camara', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movilidad.camaraseguridad')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movilidad.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Semaforo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', models.CharField(max_length=100)),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=10)),
                ('tiempo_ciclo', models.IntegerField(help_text='Duración del ciclo en segundos')),
                ('zona_critica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movilidad.zonacritica')),
            ],
        ),
        migrations.AddField(
            model_name='camaraseguridad',
            name='zona_critica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movilidad.zonacritica'),
        ),
    ]
