# Generated by Django 5.0.6 on 2024-06-20 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='tiempoDeDemora',
        ),
        migrations.AddField(
            model_name='proveedor',
            name='diasDeDemora',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
