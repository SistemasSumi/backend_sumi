# Generated by Django 4.0.2 on 2023-04-26 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0013_numeracion_fecha_inicio_numeracion_textoresolucion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plazosdecuentosproveedores',
            name='cuarenta',
            field=models.FloatField(default=0),
        ),
    ]
