# Generated by Django 5.0.6 on 2024-06-20 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_alter_articulo_loteoptimo_alter_articulo_puntopedido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='loteOptimo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='puntoPedido',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='stockSeguridad',
            field=models.IntegerField(null=True),
        ),
    ]
