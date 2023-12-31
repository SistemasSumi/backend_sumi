# Generated by Django 4.0.2 on 2023-03-07 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0010_alter_numeracion_tipodocumento_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaDePrecios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('LOCAL', 'LOCAL'), ('REGIONAL', 'REGIONAL'), ('NACIONAL', 'NACIONAL'), ('INTERNACIONAL', 'INTERNACIONAL')], max_length=50, verbose_name='Tipo')),
                ('precio1', models.FloatField(verbose_name='precio 1')),
                ('precio2', models.FloatField(verbose_name='precio 2')),
                ('precio3', models.FloatField(verbose_name='precio 3')),
                ('precioMinimo', models.FloatField(verbose_name='Precio minimo')),
            ],
            options={
                'verbose_name': 'Lista de precio',
                'verbose_name_plural': 'Listas de Precios',
                'db_table': 'listaDePrecios',
            },
        ),
        migrations.AddField(
            model_name='terceros',
            name='listaPrecios',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.listadeprecios'),
        ),
    ]
