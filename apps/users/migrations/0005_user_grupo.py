# Generated by Django 4.0.2 on 2023-06-27 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_vendedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='grupo',
            field=models.CharField(blank=True, choices=[('CONTABLIDAD', 'CONTABILIDAD'), ('FACTURACION', 'FACTURACIÓN'), ('LOGISTICA', 'LOGÍSTICA'), ('GENERAL', 'GENERAL')], max_length=50),
        ),
    ]
