# Generated by Django 4.0.2 on 2023-11-07 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0029_alter_puc_tipodecuenta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puc',
            name='tipoDeCuenta',
            field=models.CharField(choices=[('CLASES', 'CLASE'), ('SUBCLASE', 'SUBCLASE'), ('GRUPO', 'GRUPO'), ('CUENTA', 'CUENTAS'), ('SUBCUENTA', 'SUBCUENTA'), ('AUXILIAR', 'AUXILIAR')], max_length=15, verbose_name='Tipo de Cuenta:'),
        ),
    ]
