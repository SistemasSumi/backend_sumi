from rest_framework import serializers
# from apps.users.serializers import UserListSerializers

from apps.users.serializers import UserListSerializers
from apps.configuracion.serializers import *

from .models import *

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Bodega
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class tipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = tipoProducto
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response






class ProductosSerializer(serializers.ModelSerializer):
    tipoProducto = tipoProductoSerializer()
    bodega       = BodegaSerializer()
    impuesto     = ImpuestosSerializer()

    class Meta:
        model  = Productos
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # inv = ""
        # cum = ""
        # if instance.invima:
        #     inv = instance
        # if instance.cum:
        #     cum = instance.cum

        # response['nombreymarcaunico'] = instance.nombre + '('+str(instance.unidad)+')' + 'INV: '+str(inv)+' CUM: '+str(cum)     
        return response
class ProductosCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Productos
        fields = ('__all__')



    def save(self, **kwargs):
        # Implementa tu lógica personalizada aquí
        # Puedes acceder a los datos del objeto serializado utilizando self.validated_data


            # Llama al método save() de la clase padre para guardar los datos en la base de datos
            instance = Productos()
            self.instance = instance

            datos  = self.validated_data

            code = datos['nombre']
            code = code[0:3].upper()

            



            print(code)
            p = Productos.objects.filter(codigoDeBarra__startswith=code)
            n = p.count() + 1

            print(p.count(),n)
            self.instance.codigoDeBarra = code+str(n).rjust(2, '0')
            invima = ""
            cum = ""
            if datos['invima'] != "" and datos['invima'] is not None:
                invima = ' INV:'+datos['invima']
            if datos['cum'] != "" and datos['cum'] is not None :
                cum = ' CUM:'+datos['cum']
            self.instance.nombreymarcaunico = datos['nombre']+' '+datos['unidad']+invima+cum+' ('+datos['laboratorio']+')'

    
            instance = super().save(**kwargs)


            # Realiza cualquier otra operación adicional necesaria después de guardar

            return instance
    




    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class ProductosUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Productos
        fields = ('__all__')



    def update(self, instance, validated_data):

        instance.nombre          = validated_data.get('nombre', instance.nombre)
        instance.Filtro          = validated_data.get('Filtro', instance.Filtro)
        instance.invima          = validated_data.get('invima', instance.invima)
        instance.cum             = validated_data.get('cum', instance.cum)
        instance.valorCompra     = validated_data.get('valorCompra', instance.valorCompra)
        instance.valorVenta      = validated_data.get('valorVenta', instance.valorVenta)
        instance.valorventa1     = validated_data.get('valorventa1', instance.valorventa1)
        instance.valorventa2     = validated_data.get('valorventa2', instance.valorventa2)
        instance.fv              = validated_data.get('fv', instance.fv)
        instance.regulado        = validated_data.get('regulado', instance.regulado)
        instance.valorRegulacion = validated_data.get('valorRegulacion', instance.valorRegulacion)
        instance.laboratorio     = validated_data.get('laboratorio', instance.laboratorio)
        instance.stock_inicial   = validated_data.get('stock_inicial', instance.stock_inicial)
        instance.stock_min       = validated_data.get('stock_min', instance.stock_min)
        instance.stock_max       = validated_data.get('stock_max', instance.stock_max)
        instance.tipoProducto    = validated_data.get('tipoProducto', instance.tipoProducto)
        instance.habilitado      = validated_data.get('habilitado', instance.habilitado)
        instance.bodega          = validated_data.get('bodega', instance.bodega)
        instance.impuesto        = validated_data.get('impuesto', instance.impuesto)
        instance.codigoDeBarra   = validated_data.get('codigoDeBarra', instance.codigoDeBarra)
        instance.unidad          = validated_data.get('unidad', instance.unidad)
        instance.usuario         = validated_data.get('usuario', instance.usuario)



        invima = ""
        cum = ""
        if validated_data['invima'] != "":
            invima = ' INV:' + validated_data['invima']
        if validated_data['cum'] != "":
            cum = ' CUM:' + validated_data['cum']
        instance.nombreymarcaunico = (
            validated_data['nombre']
            + ' '
            + validated_data['unidad']
            + invima
            + cum
            + ' (' + validated_data['laboratorio'] + ')'
        )

        instance.save() 
      
        
        return instance



    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response




class ProductosBasicSerializer(serializers.ModelSerializer):
    # impuesto     = ImpuestosSerializer()
    class Meta:
        model  = Productos
        fields = ['id','nombreymarcaunico','valorCompra','fv','stock_min','stock_max','impuesto','bodega']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.impuesto:
            response['impuesto'] = instance.impuesto.porcentaje
        response['bodega'] = instance.bodega.nombre
        return response


class tipoProductoConProductosSerializer(serializers.ModelSerializer):

    # productos = ProductosBasicSerializer(source = "productos_tipo_producto", many = True)
    class Meta:
        model  = tipoProducto
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class BodegaCompleteSerializer(serializers.ModelSerializer):
    tiposDeProducto = tipoProductoConProductosSerializer(source = "bodega_tiposP", many = True)
    class Meta:
        model  = Bodega
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response





class KardexSerializer(serializers.ModelSerializer):
    producto     = ProductosSerializer()
    bodega       = BodegaSerializer()
    tercero      = TercerosCreateSerializer()

    class Meta:
        model  = Kardex
        fields = ('__all__')


    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class InventarioSerializer(serializers.ModelSerializer):
    idProducto     = ProductosSerializer()
    bodega         = BodegaSerializer()

    class Meta:
        model  = Inventario
        fields = ('__all__')


    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class OrdenDetalleSerializer(serializers.ModelSerializer):
    # producto    = ProductosSerializer()

    class Meta:
        model   = OrdenDetalle
        fields  = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        producto = dict()
        producto['id'] = instance.producto.id
        producto['codigo'] = instance.producto.codigoDeBarra
        producto['nombre'] = instance.producto.nombreymarcaunico
        producto['unidad'] = instance.producto.unidad
        response['producto'] = producto
        return response


class OrdenDeCompraBasicSerializer(serializers.ModelSerializer):
    # numeracion  = NumeracionSerializer()
    # proveedor   = TercerosCreateSerializer()
    # formaPago   = FormaPagoCreateSerializer()

    class Meta:
        model = OrdenDeCompra
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
 
        p  = dict()
        fp = dict()
        p['id'] = instance.proveedor.id
        p['nombreComercial'] = instance.proveedor.nombreComercial
        p['correo'] = instance.proveedor.correoContacto

        response['proveedor'] = p



        fp['id'] = instance.formaPago.id
        fp['nombre'] = instance.formaPago.nombre
        response['formaPago'] = fp
        response['usuario'] = instance.usuario.username 

        
        return response


class OrdenDeCompraDetailSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    # proveedor   = TercerosCreateSerializer()
    formaPago   = FormaPagoCreateSerializer()
    productos   = OrdenDetalleSerializer(source = 'detalle_orden', many = True )

    class Meta:
        model = OrdenDeCompra
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
       
        p = dict()
        p['id'] = instance.proveedor.id
        p['nombreComercial'] = instance.proveedor.nombreComercial
        if instance.proveedor.dv == None:
            p['documento'] = instance.proveedor.documento
        else:
            p['documento'] = instance.proveedor.documento+'-'+instance.proveedor.dv
        p['tipoDocumento'] = instance.proveedor.tipoDocumento
        if instance.proveedor.telefonoContacto == None:
            p['telefono'] = 'N/A'
        else:
            p['telefono'] = instance.proveedor.telefonoContacto
        p['direccion'] = instance.proveedor.direccion
        p['correo'] = instance.proveedor.correoContacto
        response['proveedor'] = p
        response['usuario'] = instance.usuario.username
     
        return response




class ImpuestoOrdenSerializer(serializers.ModelSerializer):
    impuesto    = ImpuestosSerializer()

    class Meta:
        model = ImpuestoOrden
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class RetencionOrdenSerializer(serializers.ModelSerializer):
    retencion   = RetencionesSerializer()

    class Meta:
        model = RetencionOrden
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class IngresoDetalleSerializer(serializers.ModelSerializer):
    # productos   = ProductosSerializer()

    class Meta:
        model = IngresoDetalle
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        producto = dict()
        producto['id'] = instance.producto.id
        producto['nombreymarcaunico'] = instance.producto.nombreymarcaunico
        producto['codigoDeBarra'] = instance.producto.codigoDeBarra
        producto['unidad'] = instance.producto.unidad
        response['producto'] = producto
        return response

class IngresoSerializer(serializers.ModelSerializer):
    numeracion    = NumeracionSerializer()
    orden         = OrdenDeCompraBasicSerializer()
    proveedor     = TercerosCreateSerializer()
    formaPago     = FormaPagoCreateSerializer()
    usuario       = UserListSerializers()
    productos     = IngresoDetalleSerializer(source = 'ingreso_detalle', many = True)

    class Meta:
        model = Ingreso
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
class IngresoBasicSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Ingreso
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class IngresoCompleteDetalleSerializer(serializers.ModelSerializer):
    producto   = ProductosSerializer()

    class Meta:
        model = IngresoDetalle
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response



class ImpuestoIngresoSeriliazer(serializers.ModelSerializer):
    ingreso     = IngresoSerializer()
    impuesto    = ImpuestosSerializer()

    class Meta:
        model = ImpuestoIngreso
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class RetencionIngresoSerializer(serializers.ModelSerializer):
    ingreso     = IngresoSerializer()
    retencion   = RetencionesSerializer()

    class Meta:
        model = RetencionIngreso
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class CxPComprasSerializer(serializers.ModelSerializer):
    ingreso     = IngresoSerializer()
    formaPago   = FormaPagoCreateSerializer()
    proveedor   = TercerosCreateSerializer()

    class Meta:
        model = CxPCompras
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class PagosComprasSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    ingreso     = IngresoSerializer()
    usuario     = UserListSerializers()

    class Meta:
        model = PagosCompras
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class NotaDebitoSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    ingreso     = IngresoSerializer()
    proveedor   = TercerosCreateSerializer()
    usuario     = UserListSerializers()

    class Meta:
        model = NotaDebito
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class NotaDebitoDetalleSerializer(serializers.ModelSerializer):
    nota        = NotaDebitoSerializer()
    producto    = ProductosSerializer()

    class Meta:
        model = NotaDebitoDetalle
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






class DetalleNotaCreditoSerializer(serializers.ModelSerializer):
    producto    = ProductosSerializer()

    class Meta:
        model = DetalleNotaCredito
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
    

    



class NotaCreditoSerializer(serializers.ModelSerializer):
    tipoNota    = ChoiceField(choices=NotaCredito.TIPO_DE_NOTAS_CHOICES)
    numeracion  = NumeracionSerializer()
    ingreso     = IngresoSerializer()
    proveedor   = TercerosCreateSerializer()
    productos   = DetalleNotaCreditoSerializer(source = 'detalle_NotaCredito', many = True)

    class Meta:
        model = NotaCredito
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['usuario'] = instance.usuario.username
        # response['tipoNota'] = instance.tipoNota.get_gender_display()
        return response
    



class DetalleAjusteSerializer(serializers.ModelSerializer):
    producto    = ProductosSerializer()

    class Meta:
        model = AjusteDetalle
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)

        tipo = convertir_choice_diccionario(instance.tipoAjuste,AjusteDetalle.TIPO_CHOICES)
        response['tipoAjuste'] = tipo
        

        return response


class AjusteSerializer(serializers.ModelSerializer):
   
    numeracion  = NumeracionSerializer()

    productos   = DetalleAjusteSerializer(source = 'detalle_ajuste', many = True)

    class Meta:
        model = AjusteStock
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['usuario'] = instance.usuario.username
        # response['tipoNota'] = instance.tipoNota.get_gender_display()
        return response
    


class PagoComprasSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    cuenta      = FormaPagoCreateSerializer()
    proveedor   = TercerosCreateSerializer()
    usuario     = UserListSerializers()

    class Meta:
        model = PagosCompras
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
    


class DetailPaymentInvoiceSerializer(serializers.ModelSerializer):
    cxpCompra  = CxPComprasSerializer()
  

    class Meta:
        model = DetailPaymentInvoice
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class PagoComprasInvoceSerializer(serializers.ModelSerializer):
    numeracion  = NumeracionSerializer()
    cuenta      = FormaPagoCreateSerializer()
    proveedor   = TercerosListSerializer()
    usuario     = UserListSerializers()
    facturas    = DetailPaymentInvoiceSerializer(source = "detalle_compra", many = True)

    class Meta:
        model = PagosCompras
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
    


class ResultadoSerializer(serializers.Serializer):
    retencion = serializers.IntegerField()
    tercero = serializers.IntegerField()
    suma_bases = serializers.FloatField()
    suma_retenciones = serializers.FloatField()

class ConsultaRetencionesSerializer(serializers.Serializer):
    fecha_inicio = serializers.DateField()
    fecha_final = serializers.DateField()
    resultados = ResultadoSerializer(many=True)