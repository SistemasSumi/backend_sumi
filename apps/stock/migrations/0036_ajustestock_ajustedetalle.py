# Generated by Django 4.0.2 on 2023-11-09 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        # ('configuracion', '0028_alter_notificacion_fecha_and_more'),
        ('stock', '0035_alter_productos_cum'),
    ]

    operations = [
        migrations.CreateModel(
            name='AjusteStock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:')),
                ('prefijo', models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:')),
                ('consecutivo', models.IntegerField(blank=True, null=True)),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='fecha')),
                ('observacion', models.TextField(default='')),
                ('numeracion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ajuste_numeracion', to='configuracion.numeracion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ajuste_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ajuste de inventario',
                'verbose_name_plural': 'Ajustes de inventario',
                'db_table': 'ajuste_stock',
            },
        ),
        migrations.CreateModel(
            name='AjusteDetalle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipoAjuste', models.CharField(choices=[('1', 'SOBRANTES'), ('2', 'BONIFICACIÓN'), ('3', 'LOTE TROCADO'), ('4', 'FV ERRADA'), ('5', 'PERDIDA')], max_length=2, verbose_name='Tipo de ajuste:')),
                ('cantidad', models.IntegerField(default=0)),
                ('costo', models.FloatField(default=0)),
                ('lote', models.CharField(max_length=50, verbose_name='Lote')),
                ('fechaVencimiento', models.DateField(verbose_name='Fecha de Vencimiento')),
                ('existencia', models.IntegerField(default=0)),
                ('isEntrada', models.BooleanField(default=False)),
                ('isSalida', models.BooleanField(default=False)),
                ('total', models.FloatField(default=0)),
                ('ajuste', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalle_ajuste', to='stock.ajustestock')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prdoucto_ajuste_stock', to='stock.productos')),
            ],
            options={
                'verbose_name': 'Ajuste Detalle',
                'verbose_name_plural': 'Ajustes Detalles',
                'db_table': 'ajuste_detalle_stock',
            },
        ),
    ]
