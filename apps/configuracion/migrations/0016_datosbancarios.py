# Generated by Django 4.0.2 on 2023-04-26 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0015_datoscontacto'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosBancarios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('CORRIENTE', 'CORRIENTE'), ('AHORROS', 'AHORROS')], max_length=50, verbose_name='Tipo:')),
                ('banco', models.CharField(max_length=50, verbose_name='Banco:')),
                ('cuenta', models.CharField(max_length=50, verbose_name='cuenta:')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='datos_bancarios', to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'Dato bancario',
                'verbose_name_plural': 'Datos  bancarios',
                'db_table': 'DatosBancarios',
            },
        ),
    ]
