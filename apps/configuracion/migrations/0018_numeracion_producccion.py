# Generated by Django 4.0.2 on 2023-06-07 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0017_datoscontacto_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='numeracion',
            name='producccion',
            field=models.BooleanField(default=False),
        ),
    ]
