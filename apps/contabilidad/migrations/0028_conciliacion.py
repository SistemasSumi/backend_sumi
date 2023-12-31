# Generated by Django 4.0.2 on 2023-09-04 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0026_alter_numeracion_tipodocumento'),
        ('contabilidad', '0027_asientodetalle_conciliado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conciliacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('consecutivo', models.IntegerField()),
                ('prefijo', models.CharField(max_length=50, verbose_name='prefijo')),
                ('numero', models.CharField(max_length=50, verbose_name='numero')),
                ('saldoAnterior', models.FloatField(default=0)),
                ('saldoFinal', models.FloatField(default=0)),
                ('mes', models.CharField(max_length=50, verbose_name='mes')),
                ('year', models.CharField(max_length=50, verbose_name='year')),
                ('fechaCierre', models.DateField(auto_now=True, verbose_name='fecha cierre')),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contabilidad.puc')),
                ('num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.numeracion')),
            ],
            options={
                'verbose_name': 'Conciliacion',
                'verbose_name_plural': 'Conciliaciones',
                'db_table': 'conciliaciones',
            },
        ),
    ]
