from rest_framework import serializers

from apps.stock.models import Productos,Inventario
from apps.configuracion.models import numeracion,Terceros



def validarFactura(dataTercero):
    pass



def ValidarNotaC(notaC):
        if notaC['numeracion'] is None or notaC['numeracion'] == '':
            raise serializers.ValidationError('La numeración no puede quedar nulo o vacio!')
        if notaC['factura'] is None or notaC['factura'] == '':
            raise serializers.ValidationError('la factura no puede quedar nulo o vacio!')
        if notaC['cliente'] is None or notaC['cliente'] == '':
            raise serializers.ValidationError('El cliente no puede quedar nulo o vacio!')


def ValidarInventario(producto:Productos, lote:str,cantidad:int):
        query = Inventario.objects.get(idProducto__id = producto.id,lote =lote)
        if query.unidades <= 0 or query.unidades < cantidad:
            raise serializers.ValidationError(f'El producto: "{producto.nombre}" NO TIENE UNIDADES O LA CANTIDAD EXCEDE LAS UNIDADES EN EL SISTEMA. LOTE: "{lote}" - UNIDADES: "{query.unidades}" !')
        


def ValidarConversionProformas(data):
        from .models import CxcMovi
        if data:
            cliente = None
            i = 0
            for x in data['values']:
                # validar existencia

                existe =  CxcMovi.objects.filter(numero = x, numeracion__tipoDocumento = numeracion.PROFORMA).exists()

                if existe:

                    pf = CxcMovi.objects.get(numero = x )


                    if i == 0:
                        cliente = pf.cliente
                        i+=1


                    # Validar que el cliente sea igual
                    if pf.cliente != cliente:
                        mensaje = f"Lamentamos informarle que el cliente en la proforma con número: <span class='text-danger fw-bold'>{x}</span> no coincide con el cliente  <span  class='text-black fw-bold'>{cliente.nombreComercial}</span> en otras proformas. Disculpe las molestias."
                        raise serializers.ValidationError(mensaje)


                    if pf.proformada:
                        mensaje = f"Lamentamos informarle que la proforma número: <span class='text-danger fw-bold'>{x}</span> ya ha sido convertida a factura electrónica en nuestra base de datos. Disculpe las molestias."
                        raise serializers.ValidationError(mensaje)
                    
                else:
                    raise serializers.ValidationError(f"Lamentamos informarle que no se encontró ninguna información o registro relacionado con el número: <span class='text-danger fw-bold'>{x}</span> en nuestra base de datos. Disculpe las molestias.")
                


                    

                

        # query = Inventario.objects.get(idProducto__id = producto.id,lote =lote)
        # if query.unidades <= 0 or query.unidades < cantidad:
        #     raise serializers.ValidationError(f'El producto: "{producto.nombre}" NO TIENE UNIDADES O LA CANTIDAD EXCEDE LAS UNIDADES EN EL SISTEMA. LOTE: "{lote}" - UNIDADES: "{query.unidades}" !')
            







    
            
