# Generated by Django 4.0.2 on 2023-07-25 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0024_alter_numeracion_tipodocumento'),
        ('contabilidad', '0023_traslado'),
    ]

    operations = [
        migrations.CreateModel(
            name='CajaMenor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.IntegerField()),
                ('fecha_apertura', models.DateField(verbose_name='fecha apertura:')),
                ('fecha_cierre', models.DateField(verbose_name='fecha apertura:')),
                ('estado', models.BooleanField(default=False)),
                ('saldo_inicial', models.FloatField()),
                ('saldo_cierre', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'Caja Menor',
                'verbose_name_plural': 'Cajas Menores',
            },
        ),
        migrations.CreateModel(
            name='PagoCajaMenor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_gasto', models.CharField(choices=[('512010', '(ARRIENDOS) CONSTRUCCIONES Y EDIFICACIONES'), ('513040', '(ARRIENDOS) FLOTA Y EQUIPO DE TRANSPORTE'), ('513095', '(ARRIENDOS) OTROS'), ('510518', '(GASTO DEL PERSONAL) COMISIONES'), ('510548', '(GASTO DEL PERSONAL) BONIFICACIONES'), ('510551', '(GASTO DEL PERSONAL) DOTACION Y SUMINISTRO A TRABAJADORES'), ('519525', '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) ELEMENTOS DE ASEO Y CAFETERIA'), ('519530', '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) UTILES DE PAPELERIA Y FOTOCOPIA'), ('519535', '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) COMBUSTIBLES Y LUBRICANTES'), ('519545', '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) TAXIS Y BUSES'), ('519565', '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) AGAZAJOS Y EVENTOS'), ('519595', '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) OTROS'), ('515505', '(GASTOS DE VIAJES) ALOJAMIENTO Y MANUTENCION'), ('515515', '(GASTOS DE VIAJES) PASAJES AEREOS'), ('515520', '(GASTOS DE VIAJES) PASAJES TERRESTRES'), ('515595', '(GASTOS DE VIAJES) OTROS'), ('511025', '(HONORARIOS) ASESORIA JURIDICA'), ('511030', '(HONORARIOS) ASESORIA FINANCIERA'), ('511035', '(HONORARIOS) ASESORIA TECNICA'), ('511055', '(HONORARIOS) ASESORIA LABORAL'), ('511095', '(HONORARIOS) OTROS'), ('514520', '(MANTENIMIENTO Y REPARACION) EQUIPOS DE OFICINA'), ('514525', '(MANTENIMIENTO Y REPARACION) EQUIPOS DE COMPUTACION Y COMUNICACION'), ('220501', '(PAGO A PROVEEDORES) PROVEEDORES'), ('513515', '(SERVICIOS) ASISTENCIA TECNICA'), ('513525', '(SERVICIOS) ACUEDUCTO Y ALCANTARILLADO'), ('513530', '(SERVICIOS) ENERGIA ELECTRICA'), ('513535', '(SERVICIOS) TELEFONOS'), ('513550', '(SERVICIOS) TRASPORTE, FLETES Y ACARREOS'), ('513595', '(SERVICIOS) OTROS')], max_length=50, verbose_name='TIPOS DE GASTOS:')),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField(verbose_name='fecha:')),
                ('docReferencia', models.CharField(max_length=80, verbose_name='Doc referencia:')),
                ('concepto', models.TextField()),
                ('valor', models.FloatField()),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='caja_menor_pago', to='contabilidad.cajamenor')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pago_caja_tercero', to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'Pago Caja Menor',
                'verbose_name_plural': 'Pagos Cajas Menores',
            },
        ),
    ]
