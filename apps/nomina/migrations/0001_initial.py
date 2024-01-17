# Generated by Django 4.0.2 on 2023-03-23 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contabilidad', '0011_alter_puc_tipodecuenta'),
    ]

    operations = [
        migrations.CreateModel(
            name='tiposDeConcepto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150, verbose_name='Tipo de concepto:')),
            ],
            options={
                'verbose_name': 'tiposDeConcepto',
                'verbose_name_plural': 'tiposDeConceptos',
            },
        ),
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Concepto:')),
                ('valor', models.FloatField(default=0)),
                ('empleado', models.FloatField(default=0)),
                ('empleador', models.FloatField(default=0)),
                ('cuenta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contabilidad.puc')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomina.tiposdeconcepto')),
            ],
            options={
                'verbose_name': 'Concepto',
                'verbose_name_plural': 'Conceptos',
            },
        ),
    ]
