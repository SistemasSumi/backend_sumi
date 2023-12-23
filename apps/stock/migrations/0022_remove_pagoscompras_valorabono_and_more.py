# Generated by Django 4.0.2 on 2023-04-19 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0021_alter_tipoproducto_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagoscompras',
            name='ValorAbono',
        ),
        migrations.RemoveField(
            model_name='pagoscompras',
            name='descuento',
        ),
        migrations.RemoveField(
            model_name='pagoscompras',
            name='diferenciaBanco',
        ),
        migrations.RemoveField(
            model_name='pagoscompras',
            name='total',
        ),
        migrations.RemoveField(
            model_name='pagoscompras',
            name='totalSaldoFavor',
        ),
        migrations.AddField(
            model_name='detailpaymentinvoice',
            name='saldoAFavor',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pagoscompras',
            name='observacion',
            field=models.TextField(blank=True, null=True, verbose_name='Observacion:'),
        ),
    ]
