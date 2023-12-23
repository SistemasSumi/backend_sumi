# Generated by Django 4.0.2 on 2023-04-20 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0012_asientodetalle_concepto_asientodetalle_tipo'),
        ('configuracion', '0013_numeracion_fecha_inicio_numeracion_textoresolucion_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docVentas', '0011_cxcmovi_iselectronica'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagosVentas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:')),
                ('consecutivo', models.IntegerField(blank=True, null=True)),
                ('prefijo', models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:')),
                ('fecha', models.DateField(verbose_name='Fecha:')),
                ('concepto', models.TextField(blank=True, null=True, verbose_name='Concepto:')),
                ('observacion', models.TextField(blank=True, null=True, verbose_name='Observacion:')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pagos_cliente', to='configuracion.terceros')),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contabilidad.puc')),
                ('numeracion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pagos_numeracion_ingreso', to='configuracion.numeracion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pagos_usuario_ingreso', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'pagosVentas',
                'verbose_name_plural': 'pagosVentas',
                'db_table': 'pagosVentas',
            },
        ),
        migrations.CreateModel(
            name='DetailPaymentInvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('factura', models.CharField(max_length=50, verbose_name='Factura:')),
                ('descuento', models.FloatField(default=0)),
                ('saldoAFavor', models.FloatField(default=0)),
                ('saldo', models.FloatField(default=0)),
                ('totalAbono', models.FloatField(default=0)),
                ('retefuente', models.FloatField(default=0)),
                ('reteica', models.FloatField(default=0)),
                ('cxc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalle_factura_pago', to='docVentas.cxcmovi')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalle_pago', to='docVentas.pagosventas')),
            ],
            options={
                'verbose_name': 'DetailPaymentInvoice',
                'verbose_name_plural': 'DetailPaymentInvoice',
            },
        ),
    ]
