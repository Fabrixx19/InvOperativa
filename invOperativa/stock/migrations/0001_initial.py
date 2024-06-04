# Generated by Django 5.0.6 on 2024-06-04 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('codArticulo', models.AutoField(primary_key=True, serialize=False)),
                ('fechaAltaArticulo', models.DateTimeField(auto_now_add=True)),
                ('fechaBajaArticulo', models.DateTimeField(blank=True, null=True)),
                ('nombreArticulo', models.CharField(max_length=30)),
                ('stockArticulo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('codVenta', models.AutoField(primary_key=True, serialize=False)),
                ('cantVenta', models.IntegerField(blank=True, null=True)),
                ('fechaVenta', models.DateTimeField(auto_now_add=True)),
                ('articulo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock.articulo')),
            ],
        ),
    ]
