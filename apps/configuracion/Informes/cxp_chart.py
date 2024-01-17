from django.db.models import Sum, Case, When, Value, FloatField,F
from apps.stock.models import CxPCompras
from django.db import models
from django.db.models.functions import Coalesce

def calcular_deuda():
    # Realiza una consulta para obtener la deuda por forma de pago
    deuda = CxPCompras.objects.filter(estado=False).values('formaPago__nombre').annotate(
        total_deuda=Coalesce(Sum(F('valorTotal') - F('valorAbono'), output_field=models.CharField()), Value('0'))
    ).filter(total_deuda__gt=Value('0'))

    # Mapea los resultados en el formato deseado
    resultado = [
        {
            'name': item['formaPago__nombre'],
            'value': float(item['total_deuda']),
        }
        for item in deuda
    ]

    return resultado