# Generated by Django 4.0.2 on 2023-09-14 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0028_conciliacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puc',
            name='tipoDeCuenta',
            field=models.CharField(choices=[('GRUPO', 'GRUPO'), ('CUENTA', 'CUENTAS'), ('SUBCUENTA', 'SUBCUENTA'), ('CLASE', 'CLASE'), ('AUXILIAR', 'AUXILIAR')], max_length=15, verbose_name='Tipo de Cuenta:'),
        ),
    ]
