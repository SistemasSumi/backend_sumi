# Generated by Django 4.0.2 on 2023-01-20 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_alter_cxpcompras_factura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cxpcompras',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha:'),
        ),
        migrations.AlterField(
            model_name='cxpcompras',
            name='fechaVencimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Vencimiento:'),
        ),
    ]
