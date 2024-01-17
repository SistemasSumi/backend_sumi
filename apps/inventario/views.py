from django.shortcuts import render

from .models import *
from .serializers import *


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
# Create your views here.



# class ProductosApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         = ProductosCreateSerializer

#     def get(self, request, format=None):
#         productos = Productos.objects.select_related('unidad','empresa','marca','bodega','usuario').all()
#         return Response(ProductosCreateSerializer(productos, many = True).data)

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def put(self, request, format=None):
#         pass

#     def delete(self, request, format=None):
#         pass



# class MarcaApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         = MarcaCreateSerializer

#     def get(self, request, format=None):
#         marca = Marca.objects.all()
#         return Response(MarcaCreateSerializer(marca, many = True).data)

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def put(self, request, format=None):
#         pass

#     def delete(self, request, format=None):
#         pass

# class UnidadApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         = UnidadCreateSerializer

#     def get(self, request, format=None):
#         und = Unidad.objects.all()
#         return Response(UnidadCreateSerializer(und, many = True).data)

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def put(self, request, format=None):
#         pass

#     def delete(self, request, format=None):
#         pass

# class BodegaApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         =  BodegaCreateSerializer

#     def get(self, request, format=None):
#         bodega = Bodega.objects.all()
#         return Response(BodegaCreateSerializer(bodega, many = True).data)

#     def post(self, request, format=None):
#         print(self.request.data)
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def put(self, request, format=None):
#         pass

#     def delete(self, request, format=None):
#         pass

# class OrdenDeCompraApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         = OrdenDeCompraCreateSerializer

#     def get(self, request, format=None):
#         orden = OrdenDeCompra.objects.getOrdenes()
#         return Response(OrdenDeCompraListSerializer(orden, many = True).data)

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         print(self.request.data)
#         serializer.is_valid(raise_exception=True)
#         import copy
#         orden = serializer.validated_data.copy()
#         print(orden)
#         productos = orden.pop('orden_detalle')

#         newOrden = OrdenDeCompra(**orden)
#         newOrden.save()

#         for p in productos:
#             newOrdenDetalle = OrdenDeCompraDetalle(orden = newOrden, **p)
#             newOrdenDetalle.save()

#         ordenGuardada = OrdenDeCompra.objects.getOrden(newOrden.id)
#         return Response(OrdenDeCompraListSerializer(ordenGuardada).data)

#     def put(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         print(self.request.data)
#         serializer.is_valid(raise_exception=True)
#         import copy
#         orden = serializer.validated_data.copy()
#         print(orden)
#         productos = orden.pop('orden_detalle')

#         updateOrden = OrdenDeCompra.objects.get(id=self.request.data['id'])
#         updateOrdenSerializer = OrdenDeCompraUpdateSerializer(updateOrden,self.request.data)
#         updateOrdenSerializer.is_valid(raise_exception=True)
#         updateOrdenSerializer.save()

#         detalleBorrar = OrdenDeCompraDetalle.objects.filter(orden = self.request.data['id'])
#         detalleBorrar.delete()

#         for p in productos:
#             newOrdenDetalle = OrdenDeCompraDetalle(orden = updateOrden, **p)
#             newOrdenDetalle.save()

#         ordenGuardada = OrdenDeCompra.objects.getOrden(self.request.data['id'])
#         return Response(OrdenDeCompraListSerializer(ordenGuardada).data)

#     def delete(self, request, format=None):
#         pass