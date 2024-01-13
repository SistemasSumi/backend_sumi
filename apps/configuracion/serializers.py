from rest_framework import serializers
from Sigban.metodos import convertir_choice_diccionario
# from apps.users.serializers import UserListSerializers 

from .models import (
    Departamentos,
    Municipios,
    Empresa,
    Impuestos,
    Retenciones,
    PlazosDecuentosClientes,
    PlazosDecuentosProveedores,
    RetencionesClientes,
    RetencionesProveedor,
    Terceros,
    FormaPago,
    VendedoresClientes,
    numeracion,
    ListaDePrecios,
    DatosContacto,
    DatosBancarios,
    Notificacion
)










class PlazosDescuentosClientesSerializer(serializers.ModelSerializer):

    class Meta:
        model  = PlazosDecuentosClientes
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class PlazosDescuentosProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PlazosDecuentosProveedores
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
    

class DatosContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DatosContacto
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
class DatosBancariosSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DatosBancarios
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response



class VendedoresSerializer(serializers.ModelSerializer):

    class Meta:
        model  = VendedoresClientes
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response



class ImpuestosSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Impuestos
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class RetencionesSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Retenciones
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class RetencionesClientesSerializer(serializers.ModelSerializer):
    retencion = RetencionesSerializer()
    class Meta:
        model  = RetencionesClientes
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class RetencionesProveedorSerializer(serializers.ModelSerializer):
    retencion = RetencionesSerializer()
    class Meta:
        model  = RetencionesProveedor
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class MunicipiosCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Municipios
        fields = ('id','codigo','municipio')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["codigo"] = instance.codigo.replace(".", "")
        return response

class DepartamentosListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Departamentos
        fields = ('id','codigo','departamento')


    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["codigo"] = instance.codigo.replace(".", "")
        return response


class DepartamentosCreateSerializer(serializers.ModelSerializer):
    municipios = MunicipiosCreateSerializer(source="departamentos_municipios", many = True)
    class Meta:
        model  = Departamentos
        fields = ('id','codigo','departamento','municipios')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["codigo"] = instance.codigo.replace(".", "")
        return response




class EmpresaCreateSerializer(serializers.ModelSerializer):
    # datosFE = DatosFacturacionElectronicaCreateSerializer(source="empresa_datosFE")
    class Meta:
        model  = Empresa
        fields = ('logo','slogan','razon_social','correo','departamento','municipio','nit','telefono')


class EmpresaListSerializer(serializers.ModelSerializer):
    # datosFE = DatosFacturacionElectronicaCreateSerializer(source = "empresa_datosFE")
    departamento = DepartamentosCreateSerializer()
    municipio = MunicipiosCreateSerializer()
    class Meta:
        model  = Empresa
        fields = ('id','logo','slogan','razon_social','correo','departamento','municipio','nit','telefono')

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        return response

# class PlazosDescuentosCreateSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model  = PlazosDecuentos
#         fields = ('__all__')

class FormaPagoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model  = FormaPago
        fields = ('__all__')

class ListaPreciosSerializer(serializers.ModelSerializer):

    class Meta:
        model  =  ListaDePrecios

        fields = ('__all__') 

class TercerosCreateSerializer(serializers.ModelSerializer):
    listaPrecios = ListaPreciosSerializer()

    class Meta:
        model  = Terceros
        fields = ('__all__')


    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        
        response['departamento'] = instance.departamento.departamento
        response['municipio'] = instance.municipio.municipio
        return response


class TercerosListSerializer(serializers.ModelSerializer):
    vendedor                 = VendedoresSerializer()
    # cuenta_x_cobrar          = pucSerializer()
    # cuenta_x_pagar           = pucSerializer()
    # cuenta_saldo_a_cliente   = pucSerializer()
    # cuenta_saldo_a_proveedor = pucSerializer()

    listaPrecios             = ListaPreciosSerializer()
    formaPago                = FormaPagoCreateSerializer()
    departamento             = DepartamentosListSerializer()
    municipio                = MunicipiosCreateSerializer()
    descuentoCliente         = PlazosDescuentosClientesSerializer(source = "plazos_clientes", many = True)
    descuentoProveedor       = PlazosDescuentosProveedorSerializer(source = "plazos_proveedores",many = True)
    retencionCliente         = RetencionesClientesSerializer(source      = "retencion_cliente", many = True)
    retencionProveedor       = RetencionesProveedorSerializer(source = "retencion_proveedor", many = True)
    datosBancarios           = DatosBancariosSerializer(source = "datos_bancarios", many = True)

    class Meta:
        model  = Terceros
        fields = (
            'id',
            'tipoDocumento',
            'documento',
            'dv',
            'nombreComercial',
            'nombreContacto',
            'direccion',
            'departamento',
            'municipio',
            'telefonoContacto',
            'correoContacto',
            'correoFacturas',
            'vendedor',
            'formaPago',
            'tipoPersona',
            'regimen',
            'obligaciones',
            'matriculaMercantil',
            'codigoPostal',
            'saldoAFavorProveedor',
            'saldoAFavorCliente',
            'isCliente',
            'isProveedor',
            'isContabilidad',
            'isCompras',
            'isPos',
            'isElectronico',
            'isRetencion',
            'cuenta_x_cobrar',
            'cuenta_x_pagar',
            'cuenta_saldo_a_cliente',
            'cuenta_saldo_a_proveedor',
            'montoCreditoProveedor',
            'montoCreditoClientes',
            'fecha_creacion',
            'fecha_modificacion',
            'estado',
            'descuentoCliente',
            'descuentoProveedor',
            'retencionCliente',
            'retencionProveedor',
            'listaPrecios',
            'datosBancarios'
        )


    def to_representation(self, instance):
        response = super().to_representation(instance)
        # print(convertir_choice_diccionario(instance.tipoPersona,Terceros.TIPOSPERSONA_CHOICES))
        return response



class VendedoresSerializer(serializers.ModelSerializer):

    class Meta:
        model  = VendedoresClientes
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class NumeracionSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(required=False, allow_blank=True, max_length=100)
    class Meta:
        model  = numeracion
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if  (   instance.tipoDocumento == '5' or 
                instance.tipoDocumento == '6' or 
                instance.tipoDocumento == '17' or
                instance.tipoDocumento == '7' or
                instance.tipoDocumento == '19' 
            ) :
            response['numero'] = str(instance.proximaFactura).rjust(4,'0')+'-'+str(instance.prefijo)
        else:
            response['numero'] = instance.prefijo+'-'+str(instance.proximaFactura).rjust(4,'0')
        return response





