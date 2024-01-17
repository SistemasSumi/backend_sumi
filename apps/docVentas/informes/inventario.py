from django.db.models import F, Sum,Subquery,OuterRef, Case,Count, When, Q,Value ,ExpressionWrapper,CharField, FloatField,Func,DateTimeField,IntegerField
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from datetime import date, timedelta
from django.db import models
from django.db.models.functions import Coalesce
from datetime import date
from datetime import datetime
from apps.stock.models import Ingreso,Productos
from apps.docVentas.models import CxcMovi
from apps.configuracion.models import Terceros
from rest_framework import serializers 
import json









def rotacion_productos_x_ventas(fecha_inicio,fecha_fin):

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

        query = Productos.objects.filter(
                cxcmovidetalle__factura__fecha__range=[fecha_inicio, fecha_fin]
        ).annotate(
        
                tipoDeProducto=F('tipoProducto__nombre')
        ).annotate(
                rotacion_compras=Coalesce(Sum('ingreso_producto__cantidad', filter=Q(ingreso_producto__ingreso__fecha__range=[fecha_inicio, fecha_fin])), 0),
                rotacion_x_ventas=Coalesce(Sum('cxcmovidetalle__cantidad', filter=Q(cxcmovidetalle__factura__fecha__range=[fecha_inicio, fecha_fin])), 0),
                existencia=Coalesce(
                        F('cxcmovidetalle__producto__stock_inicial'),  # Campo de modelo relacionado
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
