# Generated by Django 4.0.2 on 2023-03-07 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docVentas', '0003_rename_valorretecree_cxcmovi_subtotal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cxcmovi',
            name='numero',
            field=models.CharField(default=1, max_length=50, verbose_name='numero'),
            preserve_default=False,
        ),
    ]
