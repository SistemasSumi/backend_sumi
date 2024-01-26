from rest_framework import serializers 


from apps.contabilidad.serializers import pucSerializer
from .models import *
from apps.configuracion.serializers import NumeracionSerializer,FormaPagoCreateSerializer,TercerosCreateSerializer,RetencionesSerializer,ImpuestosSerializer
from Sigban.metodos import convertir_choice_diccionario



class EpsSerializer(serializers.ModelSerializer):
    
   

    class Meta:
        model  = Eps
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['tercero'] = instance.tercero.nombreComercial
    
        return response
    

class PensionSerializer(serializers.ModelSerializer):
    
   

    class Meta:
        model  = FondoPension
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['tercero'] = instance.tercero.nombreComercial
    
        return response
    
class ArlSerializer(serializers.ModelSerializer):
    
   

    class Meta:
        model  = Arl
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['tercero'] = instance.tercero.nombreComercial
    
        return response

class CajaSerializer(serializers.ModelSerializer):
    
   

    class Meta:
        model  = CajaCompensacion
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['tercero'] = instance.tercero.nombreComercial
    
        return response

class CesantiaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = FondoCesantias
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['tercero'] = instance.tercero.nombreComercial
    
        return response
    
class DeduccionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = DeduccionRecurrente
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['concepto'] = instance.concepto.nombre
        return response

class IngresoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = IngresoRecurrente
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response['concepto'] = instance.concepto.nombre
        return response




class ConceptoSerializer(serializers.ModelSerializer):


    cuenta        = pucSerializer()
    contrapartida = pucSerializer()

    class Meta:
        model  = Concepto
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        c = dict()
        return response
    


class tiposConceptoSerializer(serializers.ModelSerializer):

    
    conceptos =  ConceptoSerializer(source = "tipos_concepto", many = True)

    class Meta:
        model  = tiposDeConcepto
        fields = ('__all__')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)


        return response

class ContratoSerializer(serializers.ModelSerializer):
    eps = EpsSerializer()
    arl = ArlSerializer()
    fondoPension = PensionSerializer()
    fondoCesantias = CesantiaSerializer()
    cajaCompensacion = CajaSerializer()
   
 

    class Meta:
        model = Contrato
        fields = ('__all__')
        depth = 2

    def to_representation(self, instance):
            response = super().to_representation(instance)
            

            response['riesgo']         = convertir_choice_diccionario(instance.riesgo,Contrato.RIESGOS_CHOICES)
            response['tipoTrabajador'] = convertir_choice_diccionario(instance.tipoTrabajador,Contrato.TIPO_TRABAJADOR_CHOICES)
            response['tipoContrato']   = convertir_choice_diccionario(instance.tipoContrato,Contrato.TIPOCONTRATO_CHOICES)
            
            return response

class EmpleadoSerializer(serializers.ModelSerializer):
    
    tercero = TercerosCreateSerializer()
    contrato = ContratoSerializer() 
 

    class Meta:
        model = Empleado
        fields = ('__all__')
        depth = 2

        

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['formaDepago'] =  convertir_choice_diccionario(instance.formaDepago,Empleado.FORMADEAPGO_CHOICES)
        response['tipoDocumento'] =  convertir_choice_diccionario(instance.tipoDocumento,Empleado.TIPOSDOCUMENTOS_CHOICES)
        return response

class NominaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nomina
        fields = '__all__'

class NominaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NominaDetalle
        fields = '__all__'