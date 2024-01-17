from django.db.models import Sum, IntegerField
from django.db.models.functions import ExtractMonth
from datetime import datetime
from collections import defaultdict

from apps.docVentas.models import CxcVentas,PagosVentas
from apps.stock.models import CxPCompras,PagosCompras

def obtener_comparacion_ventas_compras_ingresos_por_mes():
    nombres_meses = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }

    # Obtén el año actual
    año_actual = datetime.now().year

    # Consulta para sumar el valor total de ventas por mes en el año actual
    ventas_por_mes = CxcVentas.objects.filter(
        fecha__year=año_actual
    ).annotate(
        mes=ExtractMonth('fecha')
    ).values(
        'mes'
    ).annotate(
        total_ventas=Sum('valorTotal', output_field=IntegerField())
    )

    # Consulta para sumar el valor total de compras por mes en el año actual
    compras_por_mes = CxPCompras.objects.filter(
        fecha__year=año_actual
    ).annotate(
        mes=ExtractMonth('fecha')
    ).values(
        'mes'
    ).annotate(
        total_compras=Sum('valorTotal', output_field=IntegerField())
    )

    # Consulta para sumar los ingresos por mes en el año actual
    ingresos_por_mes = PagosVentas.objects.filter(
        fecha__year=año_actual
    ).annotate(
        mes=ExtractMonth('fecha')
    ).values(
        'mes'
    ).annotate(
        total_ingresos=Sum('total')
    )

    # Consulta para sumar los pagos de compras por mes en el año actual
    pagos_compras_por_mes = PagosCompras.objects.filter(
        fecha__year=año_actual
    ).annotate(
        mes=ExtractMonth('fecha')
    ).values(
        'mes'
    ).annotate(
        total_pagos_compras=Sum('total')
    )

    # Crear un diccionario para almacenar los resultados por mes
    resultados = defaultdict(dict)

    # Llenar el diccionario con los resultados de ventas
    for item in ventas_por_mes:
        mes = item['mes']
        nombre_mes = nombres_meses.get(mes, f'Mes {mes}')
        resultados[mes]['name'] = nombre_mes
        resultados[mes]['ventas'] = item['total_ventas']
        resultados[mes]['compras'] = 0
        resultados[mes]['ingresos'] = 0
        resultados[mes]['egresos'] = 0

    # Llenar el diccionario con los resultados de compras
    for item in compras_por_mes:
        mes = item['mes']
        if mes in resultados:
            resultados[mes]['compras'] = item['total_compras']
        else:
            nombre_mes = nombres_meses.get(mes, f'Mes {mes}')
            resultados[mes] = {
                'name': nombre_mes,
                'ventas': 0,
                'compras': item['total_compras'],
                'ingresos': 0,
                'egresos': 0,
            }

    # Llenar el diccionario con los resultados de ingresos
    for item in ingresos_por_mes:
        mes = item['mes']
        if mes in resultados:
            resultados[mes]['ingresos'] = item['total_ingresos']
        else:
            nombre_mes = nombres_meses.get(mes, f'Mes {mes}')
            resultados[mes] = {
                'name': nombre_mes,
                'ventas': 0,
                'compras': 0,
                'ingresos': item['total_ingresos'],
                'egresos': 0,
            }

    # Llenar el diccionario con los resultados de pagos de compras
    for item in pagos_compras_por_mes:
        mes = item['mes']
        if mes in resultados:
            resultados[mes]['egresos'] = item['total_pagos_compras']
        else:
            nombre_mes = nombres_meses.get(mes, f'Mes {mes}')
            resultados[mes] = {
                'name': nombre_mes,
                'ventas': 0,
                'compras': 0,
                'ingresos': 0,
                'egresos': item['total_pagos_compras'],
            }

    # Convertir el diccionario en una lista de resultados ordenados por mes
    resultados = [value for key, value in sorted(resultados.items())]

    return resultados
