# Generated by Django 4.0.2 on 2023-09-27 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0029_notacreditoventas_contabilizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='notacreditoventas',
            name='transaccionID',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
