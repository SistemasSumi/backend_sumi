# Generated by Django 4.0.2 on 2023-05-01 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0016_asientodetalle_saldo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalancePrueba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('padre', models.IntegerField()),
                ('saldoAnterior', models.FloatField(default=0)),
                ('saldoActual', models.FloatField(default=0)),
                ('totalCredito', models.FloatField(default=0)),
                ('totalDebito', models.FloatField(default=0)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contabilidad.puc')),
            ],
            options={
                'verbose_name': 'BalancePrueba',
                'verbose_name_plural': 'BalancePruebas',
                'db_table': 'balancePrueba',
            },
        ),
    ]
