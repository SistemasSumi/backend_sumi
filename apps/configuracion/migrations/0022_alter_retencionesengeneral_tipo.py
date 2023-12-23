# Generated by Django 4.0.2 on 2023-06-20 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0021_alter_retencionesengeneral_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retencionesengeneral',
            name='tipo',
            field=models.CharField(choices=[('MC', 'Movimiento Contable'), ('NTC', 'Nota Contable'), ('COM', 'Compras'), ('FAC', 'Ventas'), ('DEV', 'Devolución')], max_length=50, verbose_name='Tipo:'),
        ),
    ]
