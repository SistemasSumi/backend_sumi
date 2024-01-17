from django.db.models import F, Sum, Case, When, Q,Value ,ExpressionWrapper,CharField, FloatField,Func,DateTimeField,IntegerField
from django.utils.timezone import now
from django.db import connection
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db import models
from datetime import date
from datetime import datetime
from apps.stock.models import CxPCompras
from apps.configuracion.models import RetencionesEnGeneral
from apps.configuracion.models import RetencionesProveedor
from apps.configuracion.models import Retenciones
from apps.configuracion.models import Terceros
from rest_framework import serializers 
import json




def estado_cartera_proveedor(proveedor_id,fecha_corte):
    # Obtener la fecha final
    fecha_final  = datetime.strptime(fecha_corte, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_final  = fecha_final.strftime("%Y-%m-%d")



    proveedor = Terceros.objects.get(id = proveedor_id)

  
      
 
    # Obtener el informe por cliente
    informe_clientes = CxPCompras.objects.filter(
        proveedor=proveedor_id,
        fecha__lte=fecha_final,
    ).annotate(
    
        saldo=Case(
            When(detailcxp__pago__fecha__gt=fecha_final, then=F('valorTotal') - (F('valorAbono') - Sum('detailcxp__totalAbono', filter=Q(detailcxp__pago__fecha__gt=fecha_final)))),
            default=F('valorTotal') - F('valorAbono')
        )
    ).values('factura', 'fecha', 'fechaVencimiento', 'saldo').order_by('-fecha','-id')

    # Filtrar el informe para mostrar solo las facturas con saldo positivo
    informe_proveedor = informe_clientes.filter(saldo__gt=0)


    totales_por_rango = {
        '0_30'   : 0,
        '31_60'  : 0,
        '61_90'  : 0,
        '91_120' : 0,
        '121_150': 0,
        '151_180': 0,
        '181++'  : 0
    }


    resultados = []
    for informe in informe_proveedor:
        dias_factura = (datetime.now().date() - informe['fecha']).days

        rango_dias = None
        totales_x_rango = {
            '0_30'   : 0,
            '31_60'  : 0,
            '61_90'  : 0,
            '91_120' : 0,
            '121_150': 0,
            '151_180': 0,
            '181++'  : 0
        }

        if 0 <= dias_factura <= 30:
            rango_dias = '0_30'
        elif 31 <= dias_factura <= 60:
            rango_dias = '31_60'
        elif 61 <= dias_factura <= 90:
            rango_dias = '61_90'
        elif 91 <= dias_factura <= 120:
            rango_dias = '91_120'
        elif 121 <= dias_factura <= 150:
            rango_dias = '121_150'
        elif 151 <= dias_factura <= 180:
            rango_dias = '151_180'
        elif dias_factura >= 181:
            rango_dias = '181++'

        if rango_dias is not None:
            totales_por_rango[rango_dias] += informe['saldo']
            totales_x_rango[rango_dias]    = informe['saldo']

        informe['dias_factura']      = dias_factura
        informe['rango_dias']        = rango_dias
        informe['totales_x_rango']   = totales_x_rango
        resultados.append(informe)

    # Obtener el saldo total
    # Calcular el saldo total directamente desde el informe_clientes

    saldo_total = informe_proveedor.aggregate(
        total_saldo=Sum('saldo')
    )['total_saldo']


    data = dict()

    data['proveedor'] = proveedor.nombreComercial
    data['formaPago'] = proveedor.formaPago.nombre
    data['documento'] = proveedor.documento

    data['fecha_corte'] = fecha_final
    data['facturas']    = resultados
    data['total_facturas']    = len(resultados)
    data['saldo_total'] = saldo_total
    data['totales_por_rango'] = totales_por_rango

    return data

def certificado_retencion_proveedor( proveedor_id, fecha_inicio, fecha_fin):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                t."nombreComercial",
                t.documento,
                SUM(cxp."reteFuente") AS valor_retenido,
                SUM(cxp."valorTotal") AS base,
                r."nombre" AS tipo_retencion,
                r."porcentaje" AS porcentaje_retencion
            FROM
                public.cxpcompras cxp
            INNER JOIN
                public.terceros t ON t.id = cxp.proveedor_id
            LEFT JOIN
                public.retenciones_proveedor rp ON t.id = rp.tercero_id
            LEFT JOIN
                public.retenciones r ON rp.retencion_id = r.id
            WHERE
                cxp.fecha BETWEEN %s AND %s AND cxp."reteFuente" > 0
                AND cxp.proveedor_id = %s
            GROUP BY
                cxp.proveedor_id, t."nombreComercial", r."nombre", r."porcentaje",t.documento
        """, [fecha_inicio, fecha_fin, proveedor_id])
        columns = [desc[0] for desc in cursor.description]

        # Obtener los resultados como un diccionario
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # results = cursor.fetchall()

    return results
    # resultados = (
    #     CxPCompras.objects
    #     .filter(
    #         proveedor_id=proveedor_id,
    #         fecha__range=(fecha_inicio, fecha_fin),
    #         reteFuente__gt=0
    #     )
    #     .values(
    #         'proveedor__nombreComercial',
    #         'proveedor_id',
    #         'retenciones__nombre',
    #         'retenciones__porcentaje'
    #     )
    #     .annotate(
    #         valor_retenido=Sum('reteFuente'),
    #         base=Sum('base'),
    #         tipo_retencion=F('retenciones__nombre'),
    #         porcentaje_retencion=F('retenciones__porcentaje')
    #     )
    # )

    # return resultados



def cuentas_x_pagar(proveedor_id,fecha_corte):
    fecha_final  = datetime.strptime(fecha_corte, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_final  = fecha_final.strftime("%Y-%m-%d")


    if proveedor_id == 0:
        reporte = CxPCompras.objects.filter(fecha__lte=fecha_final, estado=False).values(
            'ingreso__orden__numero',
            'base',
            'factura',
            'proveedor__nombreComercial',
            'fecha',
            
            'fechaVencimiento',
            'formaPago__nombre',
            'valorTotal',
            'valorAbono',
            estado_pago=Case(
                When(estado=False, then=Value('pendiente')),
                default=Value('pagada'),
                output_field=CharField(),
            ),
        ).annotate(
            debe=ExpressionWrapper(F('valorTotal') - F('valorAbono'), output_field=FloatField())
        ).order_by('fechaVencimiento')

        data = dict()

        data['proveedor'] = 'TODOS LOS PROVEEDORES'
        data['corte']    =  fecha_corte
        data['facturas'] = reporte

        return data
    else:
        proveedor = Terceros.objects.get(id = proveedor_id)
        reporte = CxPCompras.objects.filter(fecha__lte=fecha_final, estado=False, proveedor__id= proveedor_id).values(
            'ingreso__orden__numero',
            'base',
            'factura',
            'proveedor__nombreComercial',
            'fecha',
            
            'fechaVencimiento',
            'formaPago__nombre',
            'valorTotal',
            'valorAbono',
            estado_pago=Case(
                When(estado=False, then=Value('pendiente')),
                default=Value('pagada'),
                output_field=CharField(),
            ),
        ).annotate(
            debe=ExpressionWrapper(F('valorTotal') - F('valorAbono'), output_field=FloatField())
        ).order_by('fechaVencimiento')

        data = dict()

        data['proveedor'] = proveedor.nombreComercial
        data['corte']    =  fecha_corte
        data['facturas'] = reporte

        return data




def consultar_retenciones(fecha_inicio, fecha_final):
    inicio  = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
    fin     = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    fecha_inicio = inicio.strftime("%Y-%m-%d")
    fecha_final  = fin.strftime("%Y-%m-%d")

    print(fecha_inicio,fecha_final)

    retenciones = RetencionesEnGeneral.objects.filter(
        fecha__range=(fecha_inicio, fecha_final),
        compras=True
    ).exclude(tipo=RetencionesEnGeneral.DEVOLUCION).values(
        'retencion__nombre', 'tercero__nombreComercial'
    ).annotate(
        suma_bases=Sum('base'),
        suma_retenciones=Sum('total')
    )

    devoluciones_rtf = RetencionesEnGeneral.objects.filter(
        fecha__range=(fecha_inicio, fecha_final),
        compras=True,
        tipo=RetencionesEnGeneral.DEVOLUCION
    ).values(
        'retencion__nombre', 'tercero__nombreComercial'
    ).annotate(
        suma_bases=Sum('base'),
        suma_retenciones=Sum('total')
    )

    resultado_dict = {
        "fecha_inicio": fecha_inicio,
        "fecha_final": fecha_final,
        "resultados": {
            "retenciones": []
        },
        "total_bases": 0.0,
        "total_retenciones": 0.0
    }

    total_bases = 0.0
    total_retenciones = 0.0

    for resultado in retenciones:
        retencion_nombre = resultado["retencion__nombre"]
        tercero_nombre = resultado["tercero__nombreComercial"]
        base = resultado["suma_bases"]
        retencion = resultado["suma_retenciones"]

        detalle_retencion = {
            "tercero": tercero_nombre,
            "base": base,
            "retencion": retencion
        }

        retencion_encontrada = False

        # Buscar si la retención ya está en la lista de retenciones
        for retencion_actual in resultado_dict["resultados"]["retenciones"]:
            if retencion_actual["nombre"] == retencion_nombre:
                retencion_actual["detalle"].append(detalle_retencion)
                retencion_encontrada = True
                break

        # Si la retención no está en la lista, se agrega como nueva
        if not retencion_encontrada:
            nueva_retencion = {
                "nombre": retencion_nombre,
                "detalle": [detalle_retencion]
            }
            resultado_dict["resultados"]["retenciones"].append(nueva_retencion)

        total_bases += base
        total_retenciones += retencion

    for resultado in devoluciones_rtf:
        retencion_nombre = "DEV " + resultado["retencion__nombre"]
        tercero_nombre = resultado["tercero__nombreComercial"]
        base = resultado["suma_bases"] * -1  # Valor negativo
        retencion = resultado["suma_retenciones"] * -1  # Valor negativo

        detalle_devolucion = {
            "tercero": tercero_nombre,
            "base": base,
            "retencion": retencion
        }

        devolucion_encontrada = False

        # Buscar si la devolución ya está en la lista de retenciones
        for retencion_actual in resultado_dict["resultados"]["retenciones"]:
            if retencion_actual["nombre"] == retencion_nombre:
                retencion_actual["detalle"].append(detalle_devolucion)
                devolucion_encontrada = True
                break

        # Si la devolución no está en la lista, se agrega como nueva devolución
        if not devolucion_encontrada:
            nueva_devolucion = {
                "nombre": retencion_nombre,
                "detalle": [detalle_devolucion]
            }
            resultado_dict["resultados"]["retenciones"].append(nueva_devolucion)

        total_bases += base
        total_retenciones += retencion

    resultado_dict["total_bases"] = total_bases
    resultado_dict["total_retenciones"] = total_retenciones

    return resultado_dict
