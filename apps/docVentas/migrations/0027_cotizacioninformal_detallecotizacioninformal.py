# Generated by Django 4.0.2 on 2023-09-14 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0026_alter_numeracion_tipodocumento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docVentas', '0026_alter_cxcmovi_numero'),
    ]

    operations = [
        migrations.CreateModel(
            name='CotizacionInformal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('consecutivo', models.IntegerField()),
                ('numero', models.CharField(max_length=50, unique=True, verbose_name='numero')),
                ('prefijo', models.CharField(max_length=50, verbose_name='prefijo')),
                ('cliente', models.CharField(max_length=250, verbose_name='cliente')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('hora', models.TimeField(auto_now=True, verbose_name='Hora')),
                ('valor', models.FloatField()),
                ('descuento', models.FloatField(default=0)),
                ('valorLetras', models.CharField(max_length=250, verbose_name='Valor en letras')),
                ('observacion', models.CharField(blank=True, max_length=350, null=True, verbose_name='Observacion')),
                ('formaPago', models.CharField(max_length=100, verbose_name='formaPago')),
                ('valorIva', models.FloatField(default=0)),
                ('valorReteFuente', models.FloatField(default=0)),
                ('subtotal', models.FloatField(default=0)),
                ('numeracion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='numeracion_cotizacion', to='configuracion.numeracion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CotizacionInformal',
                'verbose_name_plural': 'CotizacionInformal',
            },
        ),
        migrations.CreateModel(
            name='DetalleCotizacionInformal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('producto', models.CharField(max_length=250, verbose_name='producto')),
                ('valorCompra', models.FloatField()),
                ('valor', models.FloatField()),
                ('cantidad', models.IntegerField()),
                ('vence', models.DateField(verbose_name='vencimiento:')),
                ('subtotal', models.FloatField()),
                ('descuento', models.FloatField(default=0)),
                ('iva', models.FloatField(default=0)),
                ('total', models.FloatField()),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalle_cotizacion_informal', to='docVentas.cotizacioninformal')),
            ],
            options={
                'verbose_name': 'DetalleCotizacionInformal',
                'verbose_name_plural': 'DetalleCotizacionInformal',
            },
        ),
    ]
