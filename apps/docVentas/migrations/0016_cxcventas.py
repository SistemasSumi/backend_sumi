# Generated by Django 4.0.2 on 2023-06-06 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0017_datoscontacto_telefono'),
        ('docVentas', '0015_cxcmovi_numero_nota_credito_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CxcVentas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('factura', models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Factura:')),
                ('fecha', models.DateField(blank=True, db_index=True, null=True, verbose_name='Fecha:')),
                ('fechaVencimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Vencimiento:')),
                ('observacion', models.CharField(blank=True, max_length=120, null=True, verbose_name='Observación:')),
                ('estado', models.BooleanField(default=False)),
                ('notacredito', models.BooleanField(default=False)),
                ('notadebito', models.BooleanField(default=False)),
                ('base', models.FloatField(default=0)),
                ('iva', models.FloatField(default=0)),
                ('valorAbono', models.FloatField(default=0)),
                ('reteFuente', models.FloatField(default=0)),
                ('reteIca', models.FloatField(default=0)),
                ('valorTotal', models.FloatField(default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cxcventas_cliente', to='configuracion.terceros')),
                ('cxc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='CxcVentas_factura', to='docVentas.cxcmovi')),
                ('formaPago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cxcventas_formaPago', to='configuracion.formapago')),
            ],
            options={
                'verbose_name': 'Cuenta por cobrar',
                'verbose_name_plural': 'Cuentas por cobrar',
                'db_table': 'cxc',
            },
        ),
    ]
