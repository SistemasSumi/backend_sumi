# Generated by Django 4.0.2 on 2023-03-13 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0009_alter_puc_tipodecuenta'),
    ]

    operations = [
        migrations.AddField(
            model_name='puc',
            name='formaPago',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
