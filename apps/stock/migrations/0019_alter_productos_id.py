# Generated by Django 4.0.2 on 2023-03-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0018_alter_productos_valorventa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
