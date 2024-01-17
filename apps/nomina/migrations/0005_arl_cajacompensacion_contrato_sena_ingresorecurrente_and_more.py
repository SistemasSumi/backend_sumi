# Generated by Django 4.0.2 on 2023-04-11 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0013_numeracion_fecha_inicio_numeracion_textoresolucion_and_more'),
        ('nomina', '0004_concepto_contrapartida'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arl',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomina.concepto')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'Arl',
                'verbose_name_plural': 'Arls',
            },
        ),
        migrations.CreateModel(
            name='CajaCompensacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomina.concepto')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'Caja de compensación',
                'verbose_name_plural': 'Caja de compensaciones',
            },
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salarioBase', models.FloatField(default=0)),
                ('valorDia', models.FloatField(default=0)),
                ('riesgo', models.FloatField(choices=[(0.522, 'Minimo - Riesgo 1'), (1.044, 'Bajo - Riesgo 2'), (2.436, 'Medio - Riesgo 3'), (4.35, 'Alto - Riesgo 4'), (6.96, 'Máximo - Riesgo 5')], verbose_name='Riegos:')),
                ('arl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='arl_empleado', to='nomina.arl')),
                ('cajaCompensacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='caja_empleado', to='nomina.cajacompensacion')),
            ],
            options={
                'verbose_name': 'Contrato',
                'verbose_name_plural': 'Contratos',
            },
        ),
        migrations.CreateModel(
            name='Sena',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomina.concepto')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'Sena',
                'verbose_name_plural': 'Sena',
            },
        ),
        migrations.CreateModel(
            name='IngresoRecurrente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(1, 'Salarial'), (2, 'No Salarial')], default=1, verbose_name='tipo: ')),
                ('valorMensual', models.FloatField(verbose_name='Valor Mensual:')),
                ('valorQuincenal', models.FloatField(verbose_name='Valor Quincena:')),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ingresoRecurrente_conceptos', to='nomina.concepto')),
            ],
            options={
                'verbose_name': 'IngresoRecurrente',
                'verbose_name_plural': 'IngresoRecurrentes',
            },
        ),
        migrations.CreateModel(
            name='ICBF',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomina.concepto')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'ICBF',
                'verbose_name_plural': 'ICBF',
            },
        ),
        migrations.CreateModel(
            name='FondoPension',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomina.concepto')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'FondoPension',
                'verbose_name_plural': 'FondoPensiones',
            },
        ),
        migrations.CreateModel(
            name='FondoCesantias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomina.concepto')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'FondoCesantias',
                'verbose_name_plural': 'FondoCesantias',
            },
        ),
        migrations.CreateModel(
            name='Eps',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomina.concepto')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'Empresa Prestadora De Servicio',
                'verbose_name_plural': 'Empresa Prestadora De Servicios',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('primerNombre', models.CharField(max_length=150, verbose_name='Primer nombre:')),
                ('segundoNombre', models.CharField(max_length=150, verbose_name='Segundo nombre:')),
                ('primerApellido', models.CharField(max_length=150, verbose_name='Primer apellido:')),
                ('segundoApellido', models.CharField(max_length=150, verbose_name='Segundo apellido:')),
                ('tipoDocumento', models.CharField(choices=[('1', 'Cédula de ciudadanía'), ('2', 'Cédula de extranjería'), ('3', 'Tarjeta de identidad'), ('4', 'Pasaporte')], default='1', max_length=5, verbose_name='Tipo de documento:')),
                ('documento', models.CharField(max_length=60, verbose_name='Documento:')),
                ('fechaNacimiento', models.DateField(verbose_name='nacimiento:')),
                ('correo', models.EmailField(blank=True, max_length=254, null=True, verbose_name='correo:')),
                ('telefono', models.CharField(blank=True, max_length=150, null=True, verbose_name='Telefono')),
                ('direccion', models.CharField(blank=True, max_length=150, null=True, verbose_name='Dirección:')),
                ('Cargo', models.CharField(blank=True, max_length=150, null=True, verbose_name='Cargo')),
                ('banco', models.CharField(blank=True, max_length=150, null=True, verbose_name='Banco:')),
                ('formaDepago', models.CharField(blank=True, choices=[('1', 'Instrumento no definido'), ('10', 'Efectivo'), ('42', 'Consignación bancaria')], default='42', max_length=50, null=True, verbose_name='Forma de pago:')),
                ('noCuenta', models.CharField(blank=True, max_length=150, null=True, verbose_name='N° de cuenta:')),
                ('activo', models.BooleanField(default=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contrato_empleado', to='nomina.contrato')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='empleado_Tercero', to='configuracion.terceros')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
            },
        ),
        migrations.AddField(
            model_name='contrato',
            name='eps',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eps_empleado', to='nomina.eps'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='fondoCesantias',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fondoPension_empleado', to='nomina.fondocesantias'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='fondoPension',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fondoPension_empleado', to='nomina.fondopension'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='icbf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='icbf_empleado', to='nomina.icbf'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='sena',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sena_empleado', to='nomina.sena'),
        ),
    ]
