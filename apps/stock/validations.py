from rest_framework import serializers
from .models import *

def ValidarOrden(orden):

    if orden['numeracion'] == None or orden['numeracion'] == '':
        raise serializers.ValidationError('La numeración no puede quedar nulo o vacio')
    if orden['proveedor'] == None or orden['proveedor'] == '':
        raise serializers.ValidationError('El proveedor no puede quedar nulo o vacio')
    if orden['fecha'] == None or orden['fecha'] == '':
        raise serializers.ValidationError('La fecha no puede quedar nulo o vacio')
    if orden['formaPago'] == None or orden['formaPago'] == '':
        raise serializers.ValidationError('La forma de pago no puede quedar nulo o vacio')
    if orden['usuario'] == None or orden['usuario'] == '':
        raise serializers.ValidationError('el usuario no puede quedar nulo o vacio')

def ValidarIngreso(ingreso):

    if ingreso['numeracion'] == None or ingreso['numeracion'] == '':
        raise serializers.ValidationError('La numeración no puede quedar nulo o vacio')
    if ingreso['orden'] == None or ingreso['orden'] == '':
        raise serializers.ValidationError("La orden no puede quedar nulo o vacaio")
    if ingreso['fecha'] == None or ingreso['fecha'] == '':
        raise serializers.ValidationError('La fecha no puede quedar nulo o vacio')
    if ingreso['usuario'] == None or ingreso['usuario'] == '':
        raise serializers.ValidationError('El usuario no puede quedar nulo o vacio')
    
def ValidarPagoCompras(PC, PagoDetalle):
    if PC['numeracion'] is None or PC['numeracion'] == '':
        raise serializers.ValidationError('La numeración no puede quedar nulo o vacio')
    if PC['usuario'] is None or PC['usuario'] == '':
        raise serializers.ValidationError('El usuario no puede quedar nulo o vacio')
    if PC['cuenta'] is None or PC['cuenta'] == '':
        raise serializers.ValidationError('La cuenta no puede quedar nulo o vacio')
    if PC['ingreso'] is None or PC['ingreso'] == '':
        raise serializers.ValidationError('El ingreso no puede quedar nulo o vacio')
    if PC['tipoTransaccion'] is None or PC['tipoTransaccion'] == '':
        raise serializers.ValidationError('La tipo de transacción no puede quedar nulo o vacio')
    
    if len(PagoDetalle) < 1:
        raise serializers.ValidatioError('El Detalle del pago deberia ser almenos uno')   
        



def ValidarNotaC(notaC):
        if notaC['numeracion'] is None or notaC['numeracion'] == '':
            raise serializers.ValidationError('La numeración no puede quedar nulo o vacio!')
        if notaC['ingreso'] is None or notaC['ingreso'] == '':
            raise serializers.ValidationError('El ingreso no puede quedar nulo o vacio!')
        if notaC['proveedor'] is None or notaC['proveedor'] == '':
            raise serializers.ValidationError('La proveedor no puede quedar nulo o vacio!')

def ValidarCorrecionFactura(notaC):
        if CxPCompras.objects.filter(ingreso = notaC['ingreso']).exists():
            raise serializers.ValidationError('Imposible actualizar el numero de factura. Esta factura ya tiene un pago')

# Validaciones de contabilidad    

def ValidarDetalle(detalle):

    if len(detalle) <= 0:
        raise serializers.ValidationError('Debe almenos existir un producto a ingresar.')



def contar_unidads_inventario(idproducto):
    cantidad_total = Inventario.objects.filter(idProducto__id=id_producto).aggregate(Sum('unidades'))['unidades__sum'] or 0
    return cantidad_total



def validarContabilidad(detalle):
    if len(detalle) < 2:
        raise serializers.ValidationError('No hubo un buen calculo de la contabilidad, no se guardaran los datos ni se afectara ningun registro')
    