from django.db.models import F, Sum,Subquery,OuterRef, Case,Count, When, Q,Value ,ExpressionWrapper,CharField, FloatField,Func,DateTimeField,IntegerField
from django.utils.timezone import now
from django.utils import timezone
from django.db.models.functions import Now
from datetime import timedelta
from datetime import date, timedelta
from django.db import models
from django.db.models.functions import Coalesce
from datetime import date
from datetime import datetime
from apps.stock.models import Inventario,IngresoDetalle,Ingreso,Productos,CxPCompras,Bodega,tipoProducto
from apps.docVentas.models import CxcMovi
from apps.configuracion.models import Terceros
from rest_framework import serializers 
import json

def inventario_general(bodega_id,tipo_id):

    informe = None
    if bodega_id == 0:
        if tipo_id == 0:
            informe = Inventario.objects.filter(unidades__gt=0).values(
                codigo=F('idProducto__codigoDeBarra'),
                marca=F('idProducto__laboratorio'),
                nombre=F('idProducto__nombre'),
                Lote=F('lote'),
                Vence=F('vencimiento'),
                Existencia=F('unidades'),
                valor_compra=F('valorCompra'),
                valorVenta=F('valorCompra') / 0.70,
                impuesto=F('idProducto__impuesto__nombre'),
                bodega__nombre=F('bodega__nombre'),
                filtro=F('idProducto__Filtro'),
                ubicacion=F('idProducto__tipoProducto__nombre')
            )
        else:
            informe = Inventario.objects.filter(unidades__gt=0,idProducto__tipoProducto__id = tipo_id).values(
                codigo=F('idProducto__codigoDeBarra'),
                marca=F('idProducto__laboratorio'),
                nombre=F('idProducto__nombre'),
                Lote=F('lote'),
                Vence=F('vencimiento'),
                Existencia=F('unidades'),
                valor_compra=F('valorCompra'),
                valorVenta=F('valorCompra') / 0.70,
                impuesto=F('idProducto__impuesto__nombre'),
                bodega__nombre=F('bodega__nombre'),
                filtro=F('idProducto__Filtro'),
                ubicacion=F('idProducto__tipoProducto__nombre')
            )
    else:
        if tipo_id == 0:
            informe = Inventario.objects.filter(unidades__gt=0,bodega__id = bodega_id).values(
                codigo=F('idProducto__codigoDeBarra'),
                marca=F('idProducto__laboratorio'),
                nombre=F('idProducto__nombre'),
                Lote=F('lote'),
                Vence=F('vencimiento'),
                Existencia=F('unidades'),
                valor_compra=F('valorCompra'),
                valorVenta=F('valorCompra') / 0.70,
                impuesto=F('idProducto__impuesto__nombre'),
                bodega__nombre=F('bodega__nombre'),
                filtro=F('idProducto__Filtro'),
                ubicacion=F('idProducto__tipoProducto__nombre')
            )
        else:
            informe = Inventario.objects.filter(unidades__gt=0,bodega__id = bodega_id, idProducto__tipoProducto__id = tipo_id).values(
                codigo=F('idProducto__codigoDeBarra'),
                marca=F('idProducto__laboratorio'),
                nombre=F('idProducto__nombre'),
                Lote=F('lote'),
                Vence=F('vencimiento'),
                Existencia=F('unidades'),
                valor_compra=F('valorCompra'),
                valorVenta=F('valorCompra') / 0.70,
                impuesto=F('idProducto__impuesto__nombre'),
                bodega__nombre=F('bodega__nombre'),
                filtro=F('idProducto__Filtro'),
                ubicacion=F('idProducto__tipoProducto__nombre')
            )

    return informe


def generar_informe_vencimiento(bodega_id,tipo_id):
    fecha_actual = date.today()
    fecha_limite = fecha_actual + timedelta(days=150)

    informe = None
    if bodega_id == 0:
        subconsulta = IngresoDetalle.objects.filter(
            producto_id=OuterRef('idProducto_id'),
            lote=OuterRef('lote')
        ).values(
            proveedor_nombreComercial=Case(
                When(ingreso__proveedor__nombreComercial__isnull=False, then=F('ingreso__proveedor__nombreComercial')),
                default=Value('NO ENCONTRADO'),
                output_field=CharField(),
            ),
            numero_orden=Case(
                When(ingreso__orden__numero__isnull=False, then=F('ingreso__orden__numero')),
                default=Value('NO ENCONTRADO'),
                output_field=CharField(),
            )
        )

        informe = Inventario.objects.filter(
            Q(vencimiento__range=[fecha_actual, fecha_limite],unidades__gt=0) | (Q(vencimiento__lt=fecha_actual ,unidades__gt=0))
        ).annotate(
            proveedor_nombreComercial=Subquery(subconsulta.values('proveedor_nombreComercial')[:1]),
            numero_orden=Subquery(subconsulta.values('numero_orden')[:1])
        ).filter(unidades__gt=0).values(
            codigo=F('idProducto__codigoDeBarra'),
            Lote=F('lote'),
            nombre=F('idProducto__nombre'),
            existencia=F('unidades'),
            vence=F('vencimiento'),
            marca=F('idProducto__laboratorio'),
            Bodega=F('bodega__nombre'),
            costo=F('valorCompra'),

            proveedor=Subquery(subconsulta.values('proveedor_nombreComercial')[:1]),
            numero_orden=Subquery(subconsulta.values('numero_orden')[:1]),
            estado_vencimiento=Case(
                When(vencimiento__lt=fecha_actual, then=Value('VENCIDO')),
                default=Value('POR VENCERSE'),
                output_field=CharField(),
            ),
        ).order_by('vencimiento','idProducto__nombre')


    else:

        if tipo_id == 0:
            subconsulta = IngresoDetalle.objects.filter(
                producto_id=OuterRef('idProducto_id'),
                lote=OuterRef('lote')
            ).values(
                proveedor_nombreComercial=Case(
                    When(ingreso__proveedor__nombreComercial__isnull=False, then=F('ingreso__proveedor__nombreComercial')),
                    default=Value('NO ENCONTRADO'),
                    output_field=CharField(),
                ),
                numero_orden=Case(
                    When(ingreso__orden__numero__isnull=False, then=F('ingreso__orden__numero')),
                    default=Value('NO ENCONTRADO'),
                    output_field=CharField(),
                )
            )

            informe = Inventario.objects.filter(
                Q(vencimiento__range=[fecha_actual, fecha_limite ] ,unidades__gt=0 ,bodega__id = bodega_id) | Q(vencimiento__lt=fecha_actual,unidades__gt=0,bodega__id = bodega_id)
            ).annotate(
                proveedor_nombreComercial=Subquery(subconsulta.values('proveedor_nombreComercial')[:1]),
                numero_orden=Subquery(subconsulta.values('numero_orden')[:1])
            ).filter(unidades__gt=0).values(
                codigo=F('idProducto__codigoDeBarra'),
                Lote=F('lote'),
                nombre=F('idProducto__nombre'),
                existencia=F('unidades'),
                vence=F('vencimiento'),
                costo=F('valorCompra'),
                Bodega=F('bodega__nombre'),
                marca=F('idProducto__laboratorio'),
                proveedor=Subquery(subconsulta.values('proveedor_nombreComercial')[:1]),
                numero_orden=Subquery(subconsulta.values('numero_orden')[:1]),
                estado_vencimiento=Case(
                    When(vencimiento__lt=fecha_actual, then=Value('VENCIDO')),
                    default=Value('POR VENCERSE'),
                    output_field=CharField(),
                ),
            ).order_by('vencimiento','idProducto__nombre')

        
        else:
          
            subconsulta = IngresoDetalle.objects.filter(
                producto_id=OuterRef('idProducto_id'),
                lote=OuterRef('lote')
            ).values(
                proveedor_nombreComercial=Case(
                    When(ingreso__proveedor__nombreComercial__isnull=False, then=F('ingreso__proveedor__nombreComercial')),
                    default=Value('NO ENCONTRADO'),
                    output_field=CharField(),
                ),
                numero_orden=Case(
                    When(ingreso__orden__numero__isnull=False, then=F('ingreso__orden__numero')),
                    default=Value('NO ENCONTRADO'),
                    output_field=CharField(),
                )
            )

            informe = Inventario.objects.filter(
                Q(vencimiento__range=[fecha_actual, fecha_limite ] ,unidades__gt=0,bodega__id = bodega_id,idProducto__tipoProducto = tipo_id) | Q(vencimiento__lt=fecha_actual,unidades__gt=0,idProducto__tipoProducto = tipo_id)
            ).annotate(
                proveedor_nombreComercial=Subquery(subconsulta.values('proveedor_nombreComercial')[:1]),
                numero_orden=Subquery(subconsulta.values('numero_orden')[:1])
            ).filter(unidades__gt=0).values(
                codigo=F('idProducto__codigoDeBarra'),
                Lote=F('lote'),
                nombre=F('idProducto__nombre'),
                Bodega=F('bodega__nombre'),
                existencia=F('unidades'),
                vence=F('vencimiento'),
                costo=F('valorCompra'),
                marca=F('idProducto__laboratorio'),
                proveedor=Subquery(subconsulta.values('proveedor_nombreComercial')[:1]),
                numero_orden=Subquery(subconsulta.values('numero_orden')[:1]),
                estado_vencimiento=Case(
                    When(vencimiento__lt=fecha_actual, then=Value('VENCIDO')),
                    default=Value('POR VENCERSE'),
                    output_field=CharField(),
                ),
            ).order_by('vencimiento','idProducto__nombre')

    return informe


def rotacion_productos_x_compras(fecha_inicio,fecha_fin):

        inicio  = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
        fin     = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        fecha_inicio = inicio.strftime("%Y-%m-%d")
        fecha_fin  = fin.strftime("%Y-%m-%d")


        proveedor_subquery = Terceros.objects.filter(
                ingreso_proveedor__ingreso_detalle__producto__id=OuterRef('id')
        ).order_by('-ingreso_proveedor__fecha').values('nombreComercial')[:1]


        cliente_subquery = Terceros.objects.filter(
                cliente_factura__detalle_factura__producto__id=OuterRef('id')
        ).order_by('-cliente_factura__fecha').values('nombreComercial')[:1]


        
        ultima_compra_subquery = Ingreso.objects.filter(
                ingreso_detalle__producto__id=OuterRef('id')
        ).order_by('-fecha').values('fecha')[:1]


        ultima_venta_subquery = CxcMovi.objects.filter(
                detalle_factura__producto__id=OuterRef('id')
        ).order_by('-fecha').values('fecha')[:1]

        
        rotacion_compras_subquery = Ingreso.objects.filter(
            ingreso_detalle__producto=OuterRef('pk'),  # Usa OuterRef para hacer referencia al producto actual
            fecha__range=[fecha_inicio, fecha_fin]
        ).annotate(
            total_compras=Sum('ingreso_detalle__cantidad')
        ).values('total_compras')[:1]

        # Consulta para calcular la rotación de ventas
        rotacion_ventas_subquery = CxcMovi.objects.filter(
            detalle_factura__producto=OuterRef('pk'),  # Usa OuterRef para hacer referencia al producto actual
            fecha__range=[fecha_inicio, fecha_fin]
        ).annotate(
            total_ventas=Sum('detalle_factura__cantidad')
        ).values('total_ventas')[:1]


        query = Productos.objects.filter(
                ingreso_producto__ingreso__fecha__range=[fecha_inicio, fecha_fin]
        ).annotate(
        
                tipoDeProducto=F('tipoProducto__nombre')
        ).annotate(
                 rotacion_compras=Coalesce(
                Subquery(rotacion_compras_subquery),
                0
                ),
                rotacion_x_ventas=Coalesce(
                    Subquery(rotacion_ventas_subquery),
                    0
                ),
                    existencia=Coalesce(
                    F('ingreso_producto__producto__stock_inicial'),  # Campo de modelo relacionado
                    Value(0),  # Valor predeterminado en caso de que sea nulo
                    output_field=IntegerField()  # Especifica el tipo de campo
                ),
                num_lotes=Coalesce(Count('inventario_producto__lote',filter=Q(inventario_producto__lote__gt=0), output_field=IntegerField()), 0),
                ultima_compra=Subquery(ultima_compra_subquery),
                proveedor=Subquery(proveedor_subquery),
                ultima_venta=Subquery(ultima_venta_subquery),
                cliente=Subquery(cliente_subquery),  # Reemplaza con el valor deseado
        ).values(
                'codigoDeBarra',
                'nombreymarcaunico',
                'laboratorio',
                'tipoDeProducto',
                'rotacion_compras',
                'rotacion_x_ventas',
                'existencia',
                'num_lotes',
                'ultima_compra',
                'proveedor',
                'ultima_venta',
                'cliente',
        ).order_by('nombreymarcaunico')

        return query

def compras_detalladas(proveedor_id,fecha_inicio,fecha_fin):
    inicio  = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
    fin     = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    fecha_inicio = inicio.strftime("%Y-%m-%d")
    fecha_fin  = fin.strftime("%Y-%m-%d")

    query  = None
    if proveedor_id == 0:
        query  = CxPCompras.objects.filter(fecha__range=[fecha_inicio,fecha_fin]).prefetch_related(
            'ingreso',
            'formaPago',
            'proveedor'
        ).values(
            orden=F('ingreso__orden__numero'),
            tercero=F('proveedor__nombreComercial'),
            convenio=F('formaPago__nombre'),
            n_factura=F('factura'),
            fecha_compra=F('fecha'),
            fecha_vence=F('fechaVencimiento'),
            subtotal=F('ingreso__subtotal'),
            Iva=F('iva'),
            nota=Case(
                When(notaCredito=True, then=Value('SI')),
                default=Value('NO'),
                output_field=CharField(),
            ),
            pagada=Case(
                When(estado=True, then=Value('PAGADA')),
                default=Value('PENDIENTE'),
                output_field=CharField(),
            ),
            descuento=F('ingreso__descuento'),
            retencion=F('ingreso__retencion'),
            valorFactura=F('valorTotal'),
            abono=F('valorAbono'),
            saldo= F('valorTotal') - F('valorAbono'),
        ).order_by('fecha')
    else:
        query  = CxPCompras.objects.filter(proveedor__id =  proveedor_id, fecha__range=[fecha_inicio,fecha_fin]).prefetch_related(
            'ingreso',
            'formaPago',
            'proveedor'
        ).values(
            orden=F('ingreso__orden__numero'),
            tercero=F('proveedor__nombreComercial'),
            convenio=F('formaPago__nombre'),
            n_factura=F('factura'),
            fecha_compra=F('fecha'),
            fecha_vence=F('fechaVencimiento'),
            subtotal=F('ingreso__subtotal'),
            Iva=F('iva'),
            nota=Case(
                When(notaCredito=True, then=Value('SI')),
                default=Value('NO'),
                output_field=CharField(),
            ),
            pagada=Case(
                When(estado=True, then=Value('PAGADA')),
                default=Value('PENDIENTE'),
                output_field=CharField(),
            ),
            descuento=F('ingreso__descuento'),
            retencion=F('ingreso__retencion'),
            valorFactura=F('valorTotal'),
            abono=F('valorAbono'),
            saldo= F('valorTotal') - F('valorAbono'),
        ).order_by('fecha')

    return query
   
def cierreInventario():
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()

    # Consulta para calcular los valores y agrupar por bodegas y tipos de producto
    bodegas_query = Bodega.objects.prefetch_related('bodega_tiposP__productos_tipo_producto__inventario_producto')

    informe_dict = {"bodegas": []}

    for bodega in bodegas_query:
        bodega_nombre = bodega.nombre

        tipos_producto_query = bodega.bodega_tiposP.filter(productos_tipo_producto__inventario_producto__unidades__gt=0).annotate(
            valorCompra=Sum(F('productos_tipo_producto__valorCompra') * F('productos_tipo_producto__inventario_producto__unidades')),
            valorVenta=Sum(F('productos_tipo_producto__valorCompra') * F('productos_tipo_producto__inventario_producto__unidades') / 0.70),
            unidades=Sum('productos_tipo_producto__inventario_producto__unidades'),
            valorVencido=Sum(
                Case(
                    When(productos_tipo_producto__inventario_producto__vencimiento__lt=fecha_actual, then=F('productos_tipo_producto__inventario_producto__valorCompra')*F('productos_tipo_producto__inventario_producto__unidades')),
                    default=0,
                    output_field=models.FloatField()
                )
            ),
            valorPorVencer=Sum(
                Case(
                    When(productos_tipo_producto__inventario_producto__vencimiento__lte=fecha_actual + timedelta(days=30), then=F('productos_tipo_producto__inventario_producto__valorCompra')*F('productos_tipo_producto__inventario_producto__unidades')),
                    default=0,
                    output_field=models.FloatField()
                )
            ),
        ).values(
            'nombre',
            'valorCompra',
            'valorVenta',
            'unidades',
            'valorVencido',
            'valorPorVencer',
        )

        bodega_dict = {
            "nombre": bodega_nombre,
            "tiposProducto": []
        }

        for tipo_producto in tipos_producto_query:
            tipo_producto_nombre = tipo_producto['nombre']

            # Crear diccionario para el tipo de producto
            tipo_producto_dict = {
                "nombre": tipo_producto_nombre,
                "valorCompra": tipo_producto['valorCompra'],
                "valorVenta": tipo_producto['valorVenta'],
                "unidades": tipo_producto['unidades'],
                "valorVencido": tipo_producto['valorVencido'],
                "valorPorVencer": tipo_producto['valorPorVencer'],
            }

            bodega_dict["tiposProducto"].append(tipo_producto_dict)

        informe_dict["bodegas"].append(bodega_dict)

    return informe_dict
