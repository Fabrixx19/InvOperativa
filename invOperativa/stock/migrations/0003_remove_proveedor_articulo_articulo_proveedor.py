# Generated by Django 5.0.6 on 2024-06-20 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_remove_proveedor_tiempodedemora_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='articulo',
        ),
        migrations.AddField(
            model_name='articulo',
            name='proveedor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='stock.proveedor'),
        ),
    ]
