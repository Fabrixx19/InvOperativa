# Generated by Django 5.0.6 on 2024-06-08 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demanda',
            name='valorDemanda',
        ),
        migrations.AddField(
            model_name='demanda',
            name='anioDemanda',
            field=models.IntegerField(default=2024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demanda',
            name='demandaPredecida',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='demanda',
            name='demandaReal',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='demanda',
            name='mesDemanda',
            field=models.IntegerField(),
        ),
    ]
