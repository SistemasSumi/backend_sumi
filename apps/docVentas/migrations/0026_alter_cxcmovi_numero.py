# Generated by Django 4.0.2 on 2023-08-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0025_detallenotacreditoventas_valorcompra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cxcmovi',
            name='numero',
            field=models.CharField(max_length=50, unique=True, verbose_name='numero'),
        ),
    ]
