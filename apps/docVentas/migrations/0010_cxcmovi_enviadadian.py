# Generated by Django 4.0.2 on 2023-03-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0009_alter_cxcmovi_qr'),
    ]

    operations = [
        migrations.AddField(
            model_name='cxcmovi',
            name='enviadaDian',
            field=models.BooleanField(default=False),
        ),
    ]
