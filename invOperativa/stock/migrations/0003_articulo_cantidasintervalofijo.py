# Generated by Django 5.0.6 on 2024-06-23 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_remove_prediccion_demanda_demandas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='cantidasIntervaloFijo',
            field=models.IntegerField(default=0),
        ),
    ]
