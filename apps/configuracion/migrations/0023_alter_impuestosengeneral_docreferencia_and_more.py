# Generated by Django 4.0.2 on 2023-07-19 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0022_alter_retencionesengeneral_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impuestosengeneral',
            name='docReferencia',
            field=models.CharField(max_length=1000, verbose_name='Documento referencia:'),
        ),
        migrations.AlterField(
            model_name='retencionesengeneral',
            name='docReferencia',
            field=models.CharField(max_length=1000, verbose_name='Documento referencia:'),
        ),
    ]
