from django.db.models import Sum, ExpressionWrapper, F, FloatField
from django.db.models.functions import Coalesce
from apps.docVentas.models import CxcVentas  # Asegúrate de importar tu modelo

def calcular_deuda_ventas():
    # Consulta para sumar el valor total de ventas pendientes de pago por cada forma de pago
    deuda_ventas = CxcVentas.objects.filter(
        estado=False,  # Ventas pendientes de pago
    ).values(
        'formaPago__nombre'  # Agrupar por nombre de forma de pago
    ).annotate(
        deuda=ExpressionWrapper(
            Coalesce(Sum(F('valorTotal') - F('valorAbono'), output_field=FloatField()), 0),
            output_field=FloatField()
        )
    ).filter(
        deuda__gt=0  # Solo las formas de pago con deuda mayor a 0
    )

    # Mapea los resultados en el formato deseado
    resultado = [
        {
            'name': item['formaPago__nombre'],
            'value': float(item['deuda']),
        }
        for item in deuda_ventas
    ]

    return resultado
