# Generated by Django 4.0.2 on 2023-08-28 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0034_alter_ingresodetalle_iva_alter_ordendetalle_iva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='cum',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
    ]
