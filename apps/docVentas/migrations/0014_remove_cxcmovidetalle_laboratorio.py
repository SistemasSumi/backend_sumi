# Generated by Django 4.0.2 on 2023-04-28 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0013_rename_detailpaymentinvoice_detailpaymentinvoiceventas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cxcmovidetalle',
            name='laboratorio',
        ),
    ]
