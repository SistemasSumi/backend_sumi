# Generated by Django 4.0.2 on 2023-09-18 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0028_alter_cxcmovidetalle_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='notacreditoventas',
            name='contabilizado',
            field=models.BooleanField(default=False),
        ),
    ]
