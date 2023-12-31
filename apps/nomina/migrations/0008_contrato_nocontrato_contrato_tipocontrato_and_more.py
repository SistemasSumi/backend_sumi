# Generated by Django 4.0.2 on 2023-07-28 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0007_contrato_fechafinalcontrato_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='noContrato',
            field=models.CharField(default=1, max_length=50, verbose_name='N° Contrato'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contrato',
            name='tipoContrato',
            field=models.CharField(choices=[('1', 'Termino Fijo'), ('2', 'Término Indefinido'), ('3', 'Obra o Labor'), ('4', 'Aprendizaje'), ('5', 'Prácticas')], default=1, max_length=80, verbose_name='tipo Contrato'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contrato',
            name='tipoTrabajador',
            field=models.CharField(choices=[('1', 'Dependiente'), ('2', 'Servicio domestico'), ('3', 'Independiente'), ('4', 'Madre comunitaria'), ('12', 'Aprendices del Sena en etapa lectiva'), ('16', 'Independiente agremiado o asociado'), ('19', 'Aprendices del SENA en etapa productiva'), ('20', 'Estudiantes (régimen especial ley 789 de 2002)'), ('21', 'Estudiantes de postgrado en salud'), ('23', 'Estudiantes aportes solo riesgos laborales'), ('59', 'Independiente con contrato de prestación de servicios superior a 1 mes')], default=1, max_length=80, verbose_name='tipo Trabajador'),
            preserve_default=False,
        ),
    ]
