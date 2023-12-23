from rest_framework import serializers
# from apps.users.serializers import UserListSerializers 

from apps.users.serializers import UserListSerializers
from apps.configuracion.serializers import *

# from .models import (
#    Marca,
#    Unidad,
#    Bodega,
#    Productos,
#    Inventario,
#    OrdenDeCompra,
#    OrdenDeCompraDetalle
# )

# class MarcaCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model  = Marca
#         fields = ('__all__')


# class BodegaCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model  = Bodega
#         fields = ('__all__')

# class UnidadCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model  = Unidad
#         fields = ('__all__')


# class ProductosCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model  = Productos
#         fields = ('__all__')

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['unidad'] = UnidadCreateSerializer(instance.unidad).data
#         response['marca'] = MarcaCreateSerializer(instance.marca).data
#         response['bodega'] = BodegaCreateSerializer(instance.bodega).data
#         response['usuario'] = UserListSerializers(instance.usuario).data
#         response['empresa'] = EmpresaListSerializer(instance.empresa).data
#         return response



# class OrdenDeCompraDetalleListSerializer(serializers.ModelSerializer):
#     producto = ProductosCreateSerializer()
#     class Meta:
#         model  = OrdenDeCompraDetalle
#         fields = ('__all__')

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         return response


# class OrdenDeCompraDetalleCreateSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model  = OrdenDeCompraDetalle
#         fields = ['producto','cantidad','descuento','valorUnidad','iva','total']

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         return response


# class OrdenDeCompraCreateSerializer(serializers.ModelSerializer):
#     productos = OrdenDeCompraDetalleCreateSerializer(source="orden_detalle", many = True)
#     class Meta:
#         model  = OrdenDeCompra
#         fields = ['id','factura','empresa','usuario','tercero','iva','descuento','retencion','total','observaciones','productos']

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         return response



# class OrdenDeCompraUpdateSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model  = OrdenDeCompra
#         fields =('__all__')

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         return response

# class OrdenDeCompraListSerializer(serializers.ModelSerializer):
#     productos = OrdenDeCompraDetalleListSerializer(source="orden_detalle", many = True)
#     tercero   = TercerosListSerializer()
#     usuario   = UserListSerializers()
#     empresa   = EmpresaCreateSerializer()
    
#     class Meta:
#         model  = OrdenDeCompra
#         fields = ('__all__')

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['id'] = str(instance.id).rjust(4, '0')
#         response['factura'] = str(instance.factura).rjust(5, '0')

#         return response


