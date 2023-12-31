# Generated by Django 4.0.2 on 2023-06-09 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0018_numeracion_producccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetencionesEnGeneral',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('MC', 'Movimiento Contable'), ('NTC', 'Nota Contable'), ('COM', 'Compras'), ('FAC', 'Ventas')], max_length=50, verbose_name='Tipo:')),
                ('docReferencia', models.CharField(max_length=100, verbose_name='Documento referencia:')),
                ('base', models.FloatField()),
                ('porcentaje', models.FloatField(verbose_name='porcentaje')),
                ('fecha', models.DateField(verbose_name='Fecha:')),
                ('ventas', models.BooleanField(default=False)),
                ('compras', models.BooleanField(default=False)),
                ('total', models.FloatField()),
                ('retencion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reteciones_generales', to='configuracion.retenciones')),
            ],
            options={
                'verbose_name': 'Retencion en general',
                'verbose_name_plural': 'Retenciones en general',
            },
        ),
        migrations.CreateModel(
            name='ImpuestosEnGeneral',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('MC', 'Movimiento Contable'), ('NTC', 'Nota Contable'), ('COM', 'Compras'), ('FAC', 'Ventas'), ('DEV', 'Devolución')], max_length=50, verbose_name='Tipo:')),
                ('docReferencia', models.CharField(max_length=100, verbose_name='Documento referencia:')),
                ('base', models.FloatField()),
                ('porcentaje', models.FloatField(verbose_name='porcentaje')),
                ('fecha', models.DateField(verbose_name='Fecha:')),
                ('ventas', models.BooleanField(default=False)),
                ('compras', models.BooleanField(default=False)),
                ('total', models.FloatField()),
                ('Impuesto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reteciones_generales', to='configuracion.impuestos')),
            ],
            options={
                'verbose_name': 'Impuestos en general',
                'verbose_name_plural': 'Impuestos en general',
            },
        ),
    ]
