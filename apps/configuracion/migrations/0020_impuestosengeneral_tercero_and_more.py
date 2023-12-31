# Generated by Django 4.0.2 on 2023-06-14 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0019_retencionesengeneral_impuestosengeneral'),
    ]

    operations = [
        migrations.AddField(
            model_name='impuestosengeneral',
            name='tercero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='impuesto_general_tercero', to='configuracion.terceros'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='retencionesengeneral',
            name='tercero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='retencion_general_tercero', to='configuracion.terceros'),
            preserve_default=False,
        ),
    ]
