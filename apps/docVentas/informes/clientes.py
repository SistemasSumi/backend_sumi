from django.db.models import F, Sum, Case, When, Q, ExpressionWrapper, Func,DateTimeField,IntegerField
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from django.db import models
from datetime import date
from datetime import datetime
from apps.docVentas.models import CxcVentas
from apps.configuracion.models import Terceros
from rest_framework import serializers 
import json




def estado_cartera_cliente(cliente_id,fecha_corte,retencion):
    # Obtener la fecha final
    fecha_final  = datetime.strptime(fecha_corte, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_final  = fecha_final.strftime("%Y-%m-%d")



    cliente = Terceros.objects.get(id = cliente_id)

    if retencion:
        # Obtener el informe por cliente
        informe_clientes = CxcVentas.objects.filter(
            cliente=cliente_id,
            fecha__lte=fecha_final,
            estado = False
        ).annotate(
        
            saldo=Case(
                When(cxc__detalle_factura_pago__pago__fecha__gt=fecha_final, then=(F('valorTotal')+F('reteFuente')) - (F('valorAbono') - Sum('cxc__detalle_factura_pago__totalAbono', filter=Q(cxc__detalle_factura_pago__pago__fecha__gt=fecha_final)))),
                default=(F('valorTotal')+F('reteFuente')) - F('valorAbono')
            )
        ).distinct().values('factura', 'fecha', 'fechaVencimiento', 'saldo').order_by('-fecha','-id')

        # Filtrar el informe para mostrar solo las facturas con saldo positivo
        informe_clientes = informe_clientes.filter(saldo__gt=0)


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
        for informe in informe_clientes:
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

        saldo_total = informe_clientes.aggregate(
            total_saldo=Sum('saldo')
        )['total_saldo']


        data = dict()

        data['cliente'] = cliente.nombreComercial
        data['formaPago'] = cliente.formaPago.nombre
        data['documento'] = cliente.documento

        data['fecha_corte'] = fecha_final
        data['facturas']    = resultados
        data['total_facturas']    = len(resultados)
        data['saldo_total'] = saldo_total
        data['totales_por_rango'] = totales_por_rango

        return data
    else:
        # Obtener el informe por cliente
        informe_clientes = CxcVentas.objects.filter(
            cliente=cliente_id,
            fecha__lte=fecha_final,
            estado = False
        ).annotate(
        
            saldo=Case(
                When(cxc__detalle_factura_pago__pago__fecha__gt=fecha_final, then=F('valorTotal') - (F('valorAbono') - Sum('cxc__detalle_factura_pago__totalAbono', filter=Q(cxc__detalle_factura_pago__pago__fecha__gt=fecha_final)))),
                default=F('valorTotal') - F('valorAbono')
            )
        ).distinct().values('factura', 'fecha', 'fechaVencimiento', 'saldo').order_by('-fecha','-id')

        # Filtrar el informe para mostrar solo las facturas con saldo positivo
        informe_clientes = informe_clientes.filter(saldo__gt=0)


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
        for informe in informe_clientes:
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

        saldo_total = informe_clientes.aggregate(
            total_saldo=Sum('saldo')
        )['total_saldo']


        data = dict()

        data['cliente'] = cliente.nombreComercial
        data['formaPago'] = cliente.formaPago.nombre
        data['documento'] = cliente.documento

        data['fecha_corte'] = fecha_final
        data['facturas']    = resultados
        data['total_facturas']    = len(resultados)
        data['saldo_total'] = saldo_total
        data['totales_por_rango'] = totales_por_rango

        return data

def cartera_vencida_cliente(cliente_id):
    fecha_actual = timezone.now().date()
    fecha_limite = fecha_actual + timedelta(days=15)
    from decimal import Decimal
    

    reporte = []

    if cliente_id == 0:
         # Obtener clientes con facturas vencidas o por vencerse
        # Definir la tolerancia
        tolerance = Decimal('0.1')

        # Filtrar facturas con saldo pendiente
        clientes = Terceros.objects.filter(
            cxcventas_cliente__fechaVencimiento__lt=fecha_limite,
            cxcventas_cliente__valorTotal__gt=F('cxcventas_cliente__valorAbono') + tolerance,
            cxcventas_cliente__estado=False,
        ).distinct().order_by('nombreComercial')

        for cliente in clientes:
            detalle = CxcVentas.objects.filter(cliente=cliente,estado = False).filter(
                Q(fechaVencimiento__lt=fecha_actual) | Q(fechaVencimiento__range=[fecha_actual, fecha_limite])
            ).order_by('fecha')
            facturas = []
            saldoTotal = 0
            for factura in detalle:
                if factura.fechaVencimiento < fecha_actual:
                    estado = "Vencida"
                else:
                    estado = "Por vencerse"

                dias_factura = (fecha_actual - factura.fechaVencimiento).days
                saldo = factura.valorTotal-factura.valorAbono
                saldoTotal += saldo


                facturas.append({
                    'factura': factura.factura,
                    'fecha': factura.fecha,
                    'fechaVencimiento': factura.fechaVencimiento,
                    'saldo': saldo,
                    'dias':dias_factura,
                    'estado': estado
                })

            cliente_data = {
                'cliente': cliente.nombreComercial,
                'formaPago': cliente.formaPago.nombre,
                'saldo':saldoTotal,
                'total_facturas': len(facturas),
                'facturas': facturas
            }

            reporte.append(cliente_data)
    else:

        cliente = Terceros.objects.get(id = cliente_id)
        detalle = CxcVentas.objects.filter(cliente=cliente).filter(
            Q(fechaVencimiento__lt=fecha_actual) | Q(fechaVencimiento__range=[fecha_actual, fecha_limite]),
            valorTotal__gt=F('valorAbono')
        ).order_by('-fechaVencimiento')
        facturas = []
        saldoTotal = 0
        for factura in detalle:
            if factura.fechaVencimiento < fecha_actual:
                estado = "Vencida"
            else:
                estado = "Por vencerse"
            dias_factura = (fecha_actual - factura.fechaVencimiento).days
            saldo = factura.valorTotal-factura.valorAbono
            saldoTotal += saldo

            facturas.append({
                'factura': factura.factura,
                'fecha': factura.fecha,
                'fechaVencimiento': factura.fechaVencimiento,
                'saldo': saldo,
                'dias':dias_factura,
                'estado': estado
            })

        cliente_data = {
            'cliente': cliente.nombreComercial,
            'formaPago': cliente.formaPago.nombre,
            'saldo':saldoTotal,
            'total_facturas': len(facturas),
            'facturas': facturas
        }

        reporte.append(cliente_data)

    # Convertir el reporte a JSON
    return reporte






