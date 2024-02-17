from django.db.models import F, Sum,Subquery,OuterRef, Case,Count, When, Q,Value ,ExpressionWrapper,CharField, FloatField,Func,DateTimeField,IntegerField
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from datetime import date, timedelta
from django.db import models
from django.db.models.functions import Coalesce
from datetime import date
from datetime import datetime
from apps.stock.models import Ingreso,Productos,IngresoDetalle
from apps.docVentas.models import CxcMovi,CxcMoviDetalle
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
        
             
        
        # Consulta para calcular la rotación de ventas
    
        
        query = Productos.objects.filter(
                producto_detalle_factura__factura__fecha__range=[fecha_inicio, fecha_fin]
        ).annotate(
        
                tipoDeProducto=F('tipoProducto__nombre')
        ).annotate(
                
                existencia=Coalesce(
                        F('producto_detalle_factura__producto__stock_inicial'),  # Campo de modelo relacionado
                        Value(0),  # Valor predeterminado en caso de que sea nulo
                        output_field=IntegerField()  # Especifica el tipo de campo
                ),
                num_lotes=Coalesce(Count('inventario_producto__lote',filter=Q(inventario_producto__lote__gt=0), output_field=IntegerField()), 0),
                ultima_compra=Subquery(ultima_compra_subquery),
                proveedor=Subquery(proveedor_subquery),
                ultima_venta=Subquery(ultima_venta_subquery),
                cliente=Subquery(cliente_subquery),  # Reemplaza con el valor deseado
        ).values(
                'id',
                'codigoDeBarra',
                'nombreymarcaunico',
                'laboratorio',
                'tipoDeProducto',
                'existencia',
                'num_lotes',
                'ultima_compra',
                'proveedor',
                'ultima_venta',
                'cliente',
        ).order_by('nombreymarcaunico')

        productos = []
        for x in query:
                
                rotacion_x_ventas = 0
                rotacion_x_compras = 0
                
                query_ventas = CxcMoviDetalle.objects.filter(
                        producto__id = x['id'],
                        factura__fecha__range=[fecha_inicio, fecha_fin],
                        ).exclude(factura__numeracion__tipoDocumento = '9')
                
                
                for i in query_ventas:
                        rotacion_x_ventas += i.cantidad
                        
                # query_compras = IngresoDetalle.objects.filter(producto__id = x['id'], ingreso__fecha__range=[fecha_inicio, fecha_fin])
                # for j in query_compras:
                #         rotacion_x_compras += j.cantidad
                        
                
                productos_rotados = dict()
                productos_rotados['codigoDeBarra'] = x['codigoDeBarra']
                productos_rotados['nombreymarcaunico'] = x['nombreymarcaunico']
                productos_rotados['laboratorio'] = x['laboratorio']
                productos_rotados['tipoDeProducto'] = x['tipoDeProducto']
                productos_rotados['rotacion_compras'] = rotacion_x_compras
                productos_rotados['rotacion_x_ventas'] = rotacion_x_ventas
                productos_rotados['existencia'] = x['existencia']
                productos_rotados['num_lotes'] = x['num_lotes']
                productos_rotados['ultima_compra'] = x['ultima_compra']
                productos_rotados['proveedor'] = x['proveedor']
                productos_rotados['ultima_venta'] = x['ultima_venta']
                productos_rotados['cliente'] = x['cliente']

                productos.append(productos_rotados)
        return productos
