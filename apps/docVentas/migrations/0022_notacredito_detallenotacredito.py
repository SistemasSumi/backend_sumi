# Generated by Django 4.0.2 on 2023-08-17 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0024_alter_numeracion_tipodocumento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0033_cxpcompras_notacredito'),
        ('docVentas', '0021_alter_cxcmovi_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotaCredito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:')),
                ('consecutivo', models.IntegerField(blank=True, null=True)),
                ('prefijo', models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:')),
                ('tipoNota', models.CharField(choices=[('1', 'Devoluciones'), ('2', 'Rebajas o disminución de precio'), ('3', 'Anulación total')], max_length=50, verbose_name='Tipo de nota:')),
                ('fecha', models.DateField(verbose_name='fecha:')),
                ('observacion', models.TextField(blank=True, default='', null=True)),
                ('subtotal', models.FloatField(default=0)),
                ('iva', models.FloatField(default=0)),
                ('retencion', models.FloatField(default=0)),
                ('total', models.FloatField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='NotaCreditoV_proveedor', to='configuracion.terceros')),
                ('cxc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='NotaCredito_venta', to='docVentas.cxcmovi')),
                ('numeracion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='NotaCreditoV_numeracion', to='configuracion.numeracion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='notaCreditoV_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Nota credito venta',
                'verbose_name_plural': 'nota creditos ventas',
                'db_table': 'notacreditoventas',
            },
        ),
        migrations.CreateModel(
            name='DetalleNotaCredito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lote', models.CharField(max_length=50, verbose_name='Lote:')),
                ('cantidad', models.IntegerField()),
                ('valorUnidad', models.FloatField()),
                ('iva', models.FloatField(default=0)),
                ('subtotal', models.FloatField()),
                ('nota', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalle_NotaCredito_venta', to='docVentas.notacredito')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prdoucto_notaCreditoDetalleVenta', to='stock.productos')),
            ],
            options={
                'verbose_name': 'Detalle Nota Credito venta',
                'verbose_name_plural': 'Detalles Notas Creditos Ventas',
                'db_table': 'notacreditodetalleVenta',
            },
        ),
    ]
