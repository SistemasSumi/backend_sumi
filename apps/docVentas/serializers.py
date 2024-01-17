from rest_framework import serializers 

from .models import *

from apps.configuracion.models import Terceros
from apps.users.serializers import UserListSerializers
from apps.stock.serializers import ProductosSerializer
from apps.configuracion.serializers import NumeracionSerializer,FormaPagoCreateSerializer,TercerosCreateSerializer,RetencionesSerializer,ImpuestosSerializer





class ventas_x_vendedor(serializers.Serializer):
    cliente__nombreComercial = serializers.CharField()
    total   = serializers.FloatField()
    

class proformaSerializer(serializers.ModelSerializer):
    
    formaPago = FormaPagoCreateSerializer()
    cliente   = TercerosCreateSerializer()

    class Meta:
        model  = CxcMovi
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        v = dict()
        v['id'] = instance.vendedor.id
        v['nombre'] = instance.vendedor.nombre
        response['vendedor'] = v
        response['usuario'] = instance.usuario.username
        return response



class FacturasSerializer(serializers.ModelSerializer):
    
    formaPago = FormaPagoCreateSerializer()
    cliente   = TercerosCreateSerializer()

    class Meta:
        model  = CxcMovi
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['usuario'] = instance.usuario.username
        return response
class CotizacionesSerializer(serializers.ModelSerializer):
    
    formaPago = FormaPagoCreateSerializer()
    cliente   = TercerosCreateSerializer()

    class Meta:
        model  = NuevaCotizacion
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['usuario'] = instance.usuario.username
        return response
    
class DetalleCotizacionSerializer(serializers.ModelSerializer):
    
    producto  =   ProductosSerializer()


    class Meta:
        model  = NuevaCotizacionDetalle
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        return response

class DetalleFacturasSerializer(serializers.ModelSerializer):
    
    producto  =   ProductosSerializer()


    class Meta:
        model  = CxcMoviDetalle
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        return response
    

class CxcMoviSerializer(serializers.ModelSerializer):
    
    formaPago = FormaPagoCreateSerializer()
    cliente   = TercerosCreateSerializer()
    productos = DetalleFacturasSerializer(source = "detalle_factura", many = True)


    class Meta:
        model  = CxcMovi
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['usuario'] = instance.usuario.username
        return response
    




class CxcVentasSerializer(serializers.ModelSerializer):
    
    cxc       = FacturasSerializer()
    formaPago = FormaPagoCreateSerializer()
    cliente   = TercerosCreateSerializer()


    class Meta:
        model  = CxcVentas
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        return response
    



class ImpuestosCxcMoviSerializer(serializers.ModelSerializer):
    
    impuesto = ImpuestosSerializer()


    class Meta:
        model  = ImpuestoCxc
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        return response


class RetencionCxcMoviSerializer(serializers.ModelSerializer):
    
    retencion = RetencionesSerializer()


    class Meta:
        model  = RetencionCxc
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        return response



class InvoceSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    formaPago   = FormaPagoCreateSerializer()
    cliente     = TercerosCreateSerializer()
    productos   = DetalleFacturasSerializer(source  = "detalle_factura", many = True)
    retenciones = RetencionCxcMoviSerializer(source = "retencion_cxc", many = True)
    impuestos   = ImpuestosCxcMoviSerializer(source = "impuesto_cxc", many = True)

    class Meta:
        model  = CxcMovi
        fields = ('__all__')

    def to_representation(self, instance):
        v = dict()
        response = super().to_representation(instance)
        v['id']= instance.vendedor.id
        v['nombre']= instance.vendedor.nombre
        response['usuario'] = instance.usuario.username
        response['vendedor'] = v
        return response
    
class CotizacionSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    formaPago   = FormaPagoCreateSerializer()
    cliente     = TercerosCreateSerializer()
    productos   = DetalleCotizacionSerializer(source  = "factura_cotizacion", many = True)
    # retenciones = RetencionCxcMoviSerializer(source = "retencion_cxc", many = True)
    # impuestos   = ImpuestosCxcMoviSerializer(source = "impuesto_cxc", many = True)

    class Meta:
        model  = NuevaCotizacion
        fields = ('__all__')

    def to_representation(self, instance):
        v = dict()
        response = super().to_representation(instance)
        v['id']= instance.vendedor.id
        v['nombre']= instance.vendedor.nombre
        response['usuario'] = instance.usuario.username
        response['vendedor'] = v
        print(response)
        return response
    



class DetailPaymentInvoiceVentasSerializer(serializers.ModelSerializer):
    cxc  = CxcMoviSerializer()
  

    class Meta:
        model = DetailPaymentInvoiceVentas
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class PagoVentasInvoceSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    cuenta      = FormaPagoCreateSerializer()
    cliente     = TercerosCreateSerializer()
    usuario     = UserListSerializers()
    facturas    = DetailPaymentInvoiceVentasSerializer(source = "detalle_pago", many = True)

    class Meta:
        model = PagosVentas
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
    

class PagoVentasSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    cuenta      = FormaPagoCreateSerializer()
    cliente     = TercerosCreateSerializer()
    usuario     = UserListSerializers()
    

    class Meta:
        model = PagosVentas
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
    

class DetalleNotaCreditoSerializer(serializers.ModelSerializer):
    producto    = ProductosSerializer()

    class Meta:
        model = DetalleNotaCreditoVentas
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response



class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class NotaCreditoSerializer(serializers.ModelSerializer):
    tipoNota    = ChoiceField(choices=NotaCreditoVentas.TIPO_DE_NOTAS_CHOICES)
    numeracion  = NumeracionSerializer()
    cxc         = CxcMoviSerializer()
    cliente     = TercerosCreateSerializer()
    productos   = DetalleNotaCreditoSerializer(source = 'detalle_NotaCredito_venta', many = True)

    class Meta:
        model = NotaCreditoVentas
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['usuario'] = instance.usuario.username
        # response['tipoNota'] = instance.tipoNota.get_gender_display()
        return response

    
