# Generated by Django 4.0.2 on 2023-07-13 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0022_alter_retencionesengeneral_tipo'),
        ('docVentas', '0020_pagosventas_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cxcmovi',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cliente_factura', to='configuracion.terceros'),
        ),
    ]
