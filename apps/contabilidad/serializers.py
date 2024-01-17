from rest_framework import serializers 

from Sigban.metodos import convertir_choice_diccionario
from .models import *
from apps.configuracion.serializers import TercerosCreateSerializer,NumeracionSerializer

class pucSerializer(serializers.ModelSerializer):

    class Meta:
        model  = puc
        fields = ('__all__')

class cajaSerializerConGastos(serializers.ModelSerializer):

    total_gastos = serializers.SerializerMethodField()
    class Meta:
        model  = CajaMenor
        fields = ('__all__')
    
    def get_total_gastos(self, caja_menor):
        return caja_menor.caja_menor_pago.aggregate(total_gastos=Sum('valor'))['total_gastos'] or 0
class cajaSerializer(serializers.ModelSerializer):

    class Meta:
        model  = CajaMenor
        fields = ('__all__')


class PagoCmSerializer(serializers.ModelSerializer):
    tercero = TercerosCreateSerializer()
    caja = cajaSerializer()
    class Meta:
        model  = PagoCajaMenor
        fields = ('__all__')


class TrasladoSerializer(serializers.ModelSerializer):

    numeracion     = NumeracionSerializer()
    cuenta_origen  = pucSerializer()
    cuenta_destino = pucSerializer()

    class Meta:
        model  = Traslado
        fields = ('__all__')

    def to_representation(self, instance):
            
            response = super().to_representation(instance)
            
            response['usuario'] = instance.usuario.username
            return response
class pucBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model  = puc
        fields = ('__all__')

    def to_representation(self, instance):
            
            response = super().to_representation(instance)
            if instance.naturaleza == 'DEUDORA':
                response['naturaleza'] = 'D'
            else:
                response['naturaleza'] = 'C'
            return response



class BalanceSerializer(serializers.ModelSerializer):
    cuenta = pucBalanceSerializer()
    class Meta:
        model  = BalancePrueba
        fields = ('__all__')

        
class EstadoFinancieroSerializer(serializers.ModelSerializer):
    cuenta = pucBalanceSerializer()
    class Meta:
        model  = EstadoFinanciero
        fields = ('__all__')









class asientoDetalleSerializer(serializers.ModelSerializer):
    cuenta = pucSerializer()
    class Meta:
        model  = asientoDetalle
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)

        p = dict()
        p['id'] = instance.tercero.id
        p['nombreComercial'] = instance.tercero.nombreComercial
        response['tercero'] = p
        return response


class asientoSerializer(serializers.ModelSerializer):

    detalle = asientoDetalleSerializer(source = "asiento_detalle", many = True)
    class Meta:
        model  = asiento
        fields = ('__all__')  
    


class ConciliacionSerializer(serializers.ModelSerializer):
    cuenta  = pucSerializer()

    class Meta:
        model = Conciliacion
        fields = '__all__'  # Incluye todos los campos del modelo en el serializador







class DetalleComprobanteSerializer(serializers.ModelSerializer):

    tercero = TercerosCreateSerializer()
    cuenta  =  pucSerializer()
    class Meta:
        model  = CombrobantesDetalleContable
        fields = ('__all__')  



class ComprobanteSerializerList(serializers.ModelSerializer):

    numeracion = NumeracionSerializer()
   
    class Meta:
        model  = ComprobantesContable
        fields = ('__all__')  
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tipo'] = convertir_choice_diccionario(instance.tipo,ComprobantesContable.TIPOS_CHOICES)
        response['usuario'] = instance.usuario.username
        return response



class ComprobanteSerializer(serializers.ModelSerializer):

    numeracion = NumeracionSerializer()
    detalle = DetalleComprobanteSerializer(source = 'comprobante_detalle', many = True)
    class Meta:
        model  = ComprobantesContable
        fields = ('__all__')  
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tipo'] = convertir_choice_diccionario(instance.tipo,ComprobantesContable.TIPOS_CHOICES)
        response['usuario'] = instance.usuario.username
        return response


class libroAuxiliarSerializer(serializers.ModelSerializer):
    # saldo   = serializers.IntegerField() 
    cuenta  = pucSerializer()
    asiento = asientoSerializer()
    class Meta:
        model  = asientoDetalle
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)

        p = dict()
        p['id'] = instance.tercero.id
        p['nombreComercial'] = instance.tercero.nombreComercial
        response['tercero'] = p
        return response