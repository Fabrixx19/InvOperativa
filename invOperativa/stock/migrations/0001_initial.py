# Generated by Django 5.0.6 on 2024-06-06 01:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Demanda',
            fields=[
                ('codDemanda', models.IntegerField(primary_key=True, serialize=False)),
                ('valorDemanda', models.IntegerField()),
                ('mesDemanda', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EstadoArticulo',
            fields=[
                ('codEA', models.AutoField(primary_key=True, serialize=False)),
                ('nombreEA', models.CharField(max_length=30)),
                ('fechaHoraBajaEA', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoOrdenCompra',
            fields=[
                ('codEC', models.AutoField(primary_key=True, serialize=False)),
                ('nombreEC', models.CharField(max_length=30)),
                ('fechaHoraBajaEC', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('codProveedor', models.AutoField(primary_key=True, serialize=False)),
                ('fechaBajaProveedor', models.DateField(blank=True, null=True)),
                ('nombreProveedor', models.CharField(max_length=30)),
                ('tiempoDeDemora', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('codArticulo', models.AutoField(primary_key=True, serialize=False)),
                ('fechaAltaArticulo', models.DateField(auto_now_add=True)),
                ('fechaBajaArticulo', models.DateField(blank=True, max_length=30, null=True)),
                ('nombreArticulo', models.CharField(max_length=30)),
                ('stockArticulo', models.IntegerField()),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='stock.estadoarticulo')),
            ],
        ),
        migrations.CreateModel(
            name='Prediccion_Demanda',
            fields=[
                ('codPD', models.IntegerField(primary_key=True, serialize=False)),
                ('cantPeriodos', models.IntegerField()),
                ('errorAceptable', models.IntegerField()),
                ('fechaBajaDemanda', models.DateField()),
                ('resultadoPrediccion', models.IntegerField()),
                ('mesPrimerPeriodo', models.DateField()),
                ('demandas', models.ManyToManyField(related_name='predicciones', to='stock.demanda')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenDeCompra',
            fields=[
                ('codODC', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordenDeCompra', to='stock.estadoordencompra')),
                ('prediccion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock.prediccion_demanda')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordenDeCompra', to='stock.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='ArticuloProveedor',
            fields=[
                ('codAP', models.AutoField(primary_key=True, serialize=False)),
                ('puntoPedido', models.IntegerField()),
                ('stockSeguridad', models.IntegerField()),
                ('loteOptimo', models.IntegerField()),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articuloProveedor', to='stock.articulo')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articuloProveedor', to='stock.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('codVenta', models.AutoField(primary_key=True, serialize=False)),
                ('cantVenta', models.IntegerField()),
                ('fechaVenta', models.DateField(auto_now_add=True)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='stock.articulo')),
                ('demanda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='stock.demanda')),
            ],
        ),
    ]
