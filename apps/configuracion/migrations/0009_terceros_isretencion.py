# Generated by Django 4.0.2 on 2023-01-25 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0008_alter_retencionesclientes_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='terceros',
            name='isRetencion',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
