# Generated by Django 4.0.2 on 2023-06-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0018_alter_cxcventas_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='cxcventas',
            name='valorDescuento',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='cxcmovi',
            name='fecha',
            field=models.DateField(verbose_name='Fecha'),
        ),
    ]
