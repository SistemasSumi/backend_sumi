# Generated by Django 4.0.2 on 2023-01-20 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_ordendetalle_remove_detalleorden_orden_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingreso',
            name='consecutivo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='numero',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:'),
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='prefijo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:'),
        ),
        migrations.AlterField(
            model_name='notacredito',
            name='consecutivo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notacredito',
            name='numero',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:'),
        ),
        migrations.AlterField(
            model_name='notacredito',
            name='prefijo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:'),
        ),
        migrations.AlterField(
            model_name='notadebito',
            name='consecutivo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notadebito',
            name='numero',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:'),
        ),
        migrations.AlterField(
            model_name='notadebito',
            name='prefijo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:'),
        ),
        migrations.AlterField(
            model_name='ordendecompra',
            name='consecutivo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordendecompra',
            name='numero',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:'),
        ),
        migrations.AlterField(
            model_name='ordendecompra',
            name='prefijo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:'),
        ),
        migrations.AlterField(
            model_name='pagoscompras',
            name='consecutivo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pagoscompras',
            name='numero',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero:'),
        ),
        migrations.AlterField(
            model_name='pagoscompras',
            name='prefijo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefijo:'),
        ),
    ]
