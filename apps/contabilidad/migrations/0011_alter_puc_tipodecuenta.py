# Generated by Django 4.0.2 on 2023-03-20 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0010_puc_formapago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puc',
            name='tipoDeCuenta',
            field=models.CharField(choices=[('CLASES', 'CLASE'), ('SUBCLASE', 'SUBCLASE'), ('GRUPO', 'GRUPO'), ('CUENTA', 'CUENTAS'), ('SUBCUENTA', 'SUBCUENTA')], max_length=15, verbose_name='Tipo de Cuenta:'),
        ),
    ]
