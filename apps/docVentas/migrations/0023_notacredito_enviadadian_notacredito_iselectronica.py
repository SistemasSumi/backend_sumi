# Generated by Django 4.0.2 on 2023-08-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0022_notacredito_detallenotacredito'),
    ]

    operations = [
        migrations.AddField(
            model_name='notacredito',
            name='enviadaDian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notacredito',
            name='isElectronica',
            field=models.BooleanField(default=False),
        ),
    ]
