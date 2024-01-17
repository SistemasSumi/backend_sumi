from django.db.models import F, Sum,Subquery,OuterRef, Case,Count, When, Q,Value ,ExpressionWrapper,CharField, FloatField,Func,DateTimeField,IntegerField
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from datetime import date, timedelta
from django.db import models
from django.db.models.functions import Coalesce
from datetime import date
from datetime import datetime
from apps.stock.models import Inventario,IngresoDetalle,Ingreso,Productos,CxPCompras
from apps.docVentas.models import CxcMovi,CxcVentas
from apps.configuracion.models import Terceros
from rest_framework import serializers
from django.db import transaction

import json


def ventas(cliente_id,tipo,fecha_inicio,fecha_fin):
    inicio  = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
    fin     = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    fecha_inicio = inicio.strftime("%Y-%m-%d")
    fecha_fin  = fin.strftime("%Y-%m-%d")

    query  = None
    if cliente_id == 0:
        if tipo == 'ELECTRONICA':
            query  = CxcVentas.objects.filter(fecha__range=[fecha_inicio,fecha_fin],cxc__isElectronica = True).prefetch_related(
                'cxc',
                'formaPago',
                'cliente'
            ).values(
                n_factura=F('factura'),
                documento=F('cliente__documento'),
                tercero=F('cliente__nombreComercial'),
                vendedor=F('cliente__vendedor__nombre'),
                fecha_venta=F('fecha'),
                fecha_vence=F('fechaVencimiento'),
                mes=F('fecha__month'),
                convenio=F('formaPago__nombre'),
                subtotal=F('base'),
                Iva=F('iva'),
                tipo=Case(
                    When(cxc__isElectronica=True, then=Value('ELECTRÓNICA')),
                    default=Value('POS'),
                    output_field=CharField(),
                ),
                notaC=Case(
                    When(notacredito=True, then=Value('SI')),
                    default=Value('NO'),
                    output_field=CharField(),
                ),
                notaD=Case(
                    When(notadebito=True, then=Value('SI')),
                    default=Value('NO'),
                    output_field=CharField(),
                ),
                pagada=Case(
                    When(estado=True, then=Value('PAGADA')),
                    default=Value('PENDIENTE'),
                    output_field=CharField(),
                ),
                descuento=F('valorDescuento'),
                retencion=F('reteFuente'),
                reteica=F('reteIca'),
                valorFactura=F('valorTotal'),
                abono=F('valorAbono'),
                saldo= F('valorTotal') - F('valorAbono'),
            ).order_by('fecha')
        elif tipo == 'POS':
           
            query  = CxcVentas.objects.filter(fecha__range=[fecha_inicio,fecha_fin],cxc__isElectronica = False).prefetch_related(
                    'cxc',
                    'formaPago',
                    'cliente'
                ).values(
                    n_factura=F('factura'),
                    documento=F('cliente__documento'),
                    tercero=F('cliente__nombreComercial'),
                    vendedor=F('cliente__vendedor__nombre'),
                    fecha_venta=F('fecha'),
                    fecha_vence=F('fechaVencimiento'),
                    mes=F('fecha__month'),
                    convenio=F('formaPago__nombre'),
                    subtotal=F('base'),
                    Iva=F('iva'),
                    tipo=Case(
                        When(cxc__isElectronica=True, then=Value('ELECTRÓNICA')),
                        default=Value('POS'),
                        output_field=CharField(),
                    ),
                    notaC=Case(
                        When(notacredito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    notaD=Case(
                        When(notadebito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    pagada=Case(
                        When(estado=True, then=Value('PAGADA')),
                        default=Value('PENDIENTE'),
                        output_field=CharField(),
                    ),
                    descuento=F('valorDescuento'),
                    retencion=F('reteFuente'),
                    reteica=F('reteIca'),
                    valorFactura=F('valorTotal'),
                    abono=F('valorAbono'),
                    saldo= F('valorTotal') - F('valorAbono'),
                ).order_by('fecha')
        else:
            query  = CxcVentas.objects.filter(fecha__range=[fecha_inicio,fecha_fin]).prefetch_related(
                    'cxc',
                    'formaPago',
                    'cliente'
                ).values(
                    n_factura=F('factura'),
                    documento=F('cliente__documento'),
                    tercero=F('cliente__nombreComercial'),
                    vendedor=F('cliente__vendedor__nombre'),
                    fecha_venta=F('fecha'),
                    fecha_vence=F('fechaVencimiento'),
                    mes=F('fecha__month'),
                    convenio=F('formaPago__nombre'),
                    subtotal=F('base'),
                    Iva=F('iva'),
                    tipo=Case(
                        When(cxc__isElectronica=True, then=Value('ELECTRÓNICA')),
                        default=Value('POS'),
                        output_field=CharField(),
                    ),
                    notaC=Case(
                        When(notacredito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    notaD=Case(
                        When(notadebito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    pagada=Case(
                        When(estado=True, then=Value('PAGADA')),
                        default=Value('PENDIENTE'),
                        output_field=CharField(),
                    ),
                    descuento=F('valorDescuento'),
                    retencion=F('reteFuente'),
                    reteica=F('reteIca'),
                    valorFactura=F('valorTotal'),
                    abono=F('valorAbono'),
                    saldo= F('valorTotal') - F('valorAbono'),
                ).order_by('fecha')


    else:
      
        if tipo == 'ELECTRONICA':
            query  = CxcVentas.objects.filter(cliente__id = cliente_id, fecha__range=[fecha_inicio,fecha_fin],cxc__isElectronica = True).prefetch_related(
                'cxc',
                'formaPago',
                'cliente'
            ).values(
                n_factura=F('factura'),
                documento=F('cliente__documento'),
                tercero=F('cliente__nombreComercial'),
                vendedor=F('cliente__vendedor__nombre'),
                fecha_venta=F('fecha'),
                fecha_vence=F('fechaVencimiento'),
                mes=F('fecha__month'),
                convenio=F('formaPago__nombre'),
                subtotal=F('base'),
                Iva=F('iva'),
                tipo=Case(
                    When(cxc__isElectronica=True, then=Value('ELECTRÓNICA')),
                    default=Value('POS'),
                    output_field=CharField(),
                ),
                notaC=Case(
                    When(notacredito=True, then=Value('SI')),
                    default=Value('NO'),
                    output_field=CharField(),
                ),
                notaD=Case(
                    When(notadebito=True, then=Value('SI')),
                    default=Value('NO'),
                    output_field=CharField(),
                ),
                pagada=Case(
                    When(estado=True, then=Value('PAGADA')),
                    default=Value('PENDIENTE'),
                    output_field=CharField(),
                ),
                descuento=F('valorDescuento'),
                retencion=F('reteFuente'),
                reteica=F('reteIca'),
                valorFactura=F('valorTotal'),
                abono=F('valorAbono'),
                saldo= F('valorTotal') - F('valorAbono'),
            ).order_by('fecha')
        elif tipo == 'POS':
            query  = CxcVentas.objects.filter(cliente__id = cliente_id,fecha__range=[fecha_inicio,fecha_fin],cxc__isElectronica = False).prefetch_related(
                    'cxc',
                    'formaPago',
                    'cliente'
                ).values(
                    n_factura=F('factura'),
                    documento=F('cliente__documento'),
                    tercero=F('cliente__nombreComercial'),
                    vendedor=F('cliente__vendedor__nombre'),
                    fecha_venta=F('fecha'),
                    fecha_vence=F('fechaVencimiento'),
                    mes=F('fecha__month'),
                    convenio=F('formaPago__nombre'),
                    subtotal=F('base'),
                    Iva=F('iva'),
                    tipo=Case(
                        When(cxc__isElectronica=True, then=Value('ELECTRÓNICA')),
                        default=Value('POS'),
                        output_field=CharField(),
                    ),
                    notaC=Case(
                        When(notacredito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    notaD=Case(
                        When(notadebito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    pagada=Case(
                        When(estado=True, then=Value('PAGADA')),
                        default=Value('PENDIENTE'),
                        output_field=CharField(),
                    ),
                    descuento=F('valorDescuento'),
                    retencion=F('reteFuente'),
                    reteica=F('reteIca'),
                    valorFactura=F('valorTotal'),
                    abono=F('valorAbono'),
                    saldo= F('valorTotal') - F('valorAbono'),
                ).order_by('fecha')
        else:
            query  = CxcVentas.objects.filter(cliente__id = cliente_id,fecha__range=[fecha_inicio,fecha_fin]).prefetch_related(
                    'cxc',
                    'formaPago',
                    'cliente'
                ).values(
                    n_factura=F('factura'),
                    documento=F('cliente__documento'),
                    tercero=F('cliente__nombreComercial'),
                    vendedor=F('cliente__vendedor__nombre'),
                    fecha_venta=F('fecha'),
                    fecha_vence=F('fechaVencimiento'),
                    mes=F('fecha__month'),
                    convenio=F('formaPago__nombre'),
                    subtotal=F('base'),
                    Iva=F('iva'),
                    tipo=Case(
                        When(cxc__isElectronica=True, then=Value('ELECTRÓNICA')),
                        default=Value('POS'),
                        output_field=CharField(),
                    ),
                    notaC=Case(
                        When(notacredito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    notaD=Case(
                        When(notadebito=True, then=Value('SI')),
                        default=Value('NO'),
                        output_field=CharField(),
                    ),
                    pagada=Case(
                        When(estado=True, then=Value('PAGADA')),
                        default=Value('PENDIENTE'),
                        output_field=CharField(),
                    ),
                    descuento=F('valorDescuento'),
                    retencion=F('reteFuente'),
                    reteica=F('reteIca'),
                    valorFactura=F('valorTotal'),
                    abono=F('valorAbono'),
                    saldo= F('valorTotal') - F('valorAbono'),
                ).order_by('fecha')

    return query
   

def obtener_resumen_vendedores(nombres_vendedores,fecha_inicio,fecha_final):
    
    inicio  = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
    fin     = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    fecha_inicio = inicio.strftime("%Y-%m-%d")
    fecha_final  = fin.strftime("%Y-%m-%d")
    # Calcular el monto total por vendedor y obtener el avatar del usuario asociado
    try:
        with transaction.atomic():
            resumen = (
                CxcVentas.objects.filter(cliente__vendedor__nombre__in=nombres_vendedores, fecha__range=[fecha_inicio, fecha_final])
                .exclude(cliente__vendedor__meta=0)
                .values('cliente__vendedor__nombre')
                .annotate(
                    monto_total=Sum('valorTotal')+Sum('reteFuente')+Sum('reteIca')+Sum('valorDescuento'),
                    meta_vendedor=F('cliente__vendedor__meta'),
                    avatar=F('cliente__vendedor__usuario__avatar_url'),
                    porcentaje=(Sum('valorTotal') / F('cliente__vendedor__meta')) * 100
                )
                .order_by('cliente__vendedor__nombre')
            )
    except ZeroDivisionError:
        raise serializers.ValidationError(f'Lamentablemente, no es posible calcular el porcentaje de cumplimiento de la meta cuando la meta de un usuario es igual a cero. La división por cero es una operación matemáticamente indefinida y no tiene un resultado válido. Por lo tanto, si la meta de un usuario es cero, no se puede realizar el cálculo del porcentaje de cumplimiento de la meta.')
    return resumen  


def obtener_resumen_ventas_por_vendedor(vendedor_id, fecha_inicial, fecha_final):
    fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    fecha_final = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    
    # Obtener todos los clientes del vendedor
    clientes = Terceros.objects.filter(vendedor__id=vendedor_id).order_by('nombreComercial')

    resumen_ventas = []

    for cliente in clientes:
        # Obtener las ventas del cliente en el rango de fechas especificado
        ventas_cliente = CxcVentas.objects.filter(
            cliente__id=cliente.id,
            fecha__range=[fecha_inicial, fecha_final]
        ).aggregate(
            total_venta=Coalesce(
                Sum(F('valorTotal') + F('reteFuente') + F('reteIca') + F('valorDescuento')),
                Value(0, output_field=FloatField())
            ),
            num_ventas=Count('id')
        )

        # Agregar el resumen de ventas del cliente a la lista de resultados
        resumen_ventas.append({
            'cliente__nombreComercial': cliente.nombreComercial,
            'total_venta': ventas_cliente['total_venta'],
            'num_ventas': ventas_cliente['num_ventas']
        })

    return resumen_ventas

    return list(ventas)