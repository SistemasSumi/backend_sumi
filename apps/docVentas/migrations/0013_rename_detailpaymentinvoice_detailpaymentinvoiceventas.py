# Generated by Django 4.0.2 on 2023-04-20 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0012_pagosventas_detailpaymentinvoice'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DetailPaymentInvoice',
            new_name='DetailPaymentInvoiceVentas',
        ),
    ]
