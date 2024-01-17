from django.db import models
from apps.users.models import User
from apps.configuracion.models import numeracion
from datetime import date, timedelta
from django.db.models import Q
from django.db import transaction
from datetime import datetime
from .signals import delete_factura_pago,update_factura_pago
from django.db.models.signals import post_save,post_delete

class CxcMovi(models.Model):
    """Model definition for CxcMovi."""


    # TODO: Define fields here
    id                 = models.AutoField(primary_key = True)
    numeracion         = models.ForeignKey(to="configuracion.numeracion", related_name="numeracion_factura", on_delete=models.PROTECT)
    consecutivo        = models.IntegerField()
    numero             = models.CharField('numero', max_length=50, unique=True)
    prefijo            = models.CharField('prefijo', max_length=50)
    cliente            = models.ForeignKey("configuracion.Terceros",models.PROTECT, related_name="cliente_factura")
    valor              = models.FloatField()
    fecha              = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    hora               = models.TimeField('Hora', auto_now=True, auto_now_add=False)
    fechaVencimiento   = models.DateField('Fecha de vencimiento', auto_now=False, auto_now_add=False)
    abono              = models.FloatField(default = 0)
    descuento          = models.FloatField(default = 0)
    valorDomicilio     = models.FloatField(default = 0)
    valorLetras        = models.CharField('Valor en letras', max_length=250)
    observacion        = models.CharField('Observacion', max_length=350,blank=True, null=True)
    formaPago          = models.ForeignKey(to='configuracion.FormaPago', related_name="cxc_formaPago", on_delete=models.PROTECT)
    vendedor           = models.ForeignKey(to="configuracion.VendedoresClientes", related_name="facturas_vendedor", on_delete=models.PROTECT)
    pagada             = models.BooleanField(default = False)
    usuario            = models.ForeignKey("users.User",models.PROTECT)
    xmlEstado          = models.BooleanField(default = False)
    transaccionID      = models.CharField('transaccionID', max_length=500, blank=True, null=True)
    cufe               = models.TextField('cufe', blank=True, null=True)
    proformada         = models.BooleanField(default = False)
    qr                 = models.TextField('qr', blank=True, null=True)
    statusFac          = models.CharField('statusFac', max_length=350, blank=True, null=True)
    valorIva           = models.FloatField(default = 0)
    valorReteFuente    = models.FloatField(default = 0)
    subtotal           = models.FloatField(default = 0)
    valor_nota_credito = models.FloatField(default = 0)
    valor_nota_debito  = models.FloatField(default = 0)
    numero_nota_credito= models.CharField('numero nota credito', max_length=50, blank=True, null=True)
    numero_nota_debito = models.CharField('numero nota debito', max_length=50, blank=True, null=True)
    despachado         = models.BooleanField(default = False)
    correoEnviado      = models.BooleanField(default = False)
    isElectronica      = models.BooleanField(default = False)
    enviadaDian        = models.BooleanField(default = False)

    class Meta:
        """Meta definition for CxcMovi."""

        verbose_name = 'CxcMovi'
        verbose_name_plural = 'CxcMovi'

    def __str__(self): 
        return f'{self.numero}'
    
    def save(self, *args, **kwargs):

        if self.fecha is None:
            self.fecha =  date.today()
        if self.formaPago.nombre == 'CONTADO':
            self.fechaVencimiento =  self.fecha
        if self.formaPago.nombre == 'CRÉDITO 30 DIAS':
            td = timedelta(30)
            self.fechaVencimiento =  self.fecha + td
        if self.formaPago.nombre == 'CRÉDITO 45 DIAS':
            td = timedelta(45)
            self.fechaVencimiento =  self.fecha + td
        if self.formaPago.nombre == 'CRÉDITO 60 DIAS':
            td = timedelta(60)
            self.fechaVencimiento =  self.fecha + td
        if self.formaPago.nombre == 'CRÉDITO 90 DIAS':
            td = timedelta(90)
            self.fechaVencimiento =  self.fecha + td
        super(CxcMovi, self).save(*args, **kwargs)

    @classmethod
    def filter_by_criterio_ventas(cls, obj):
        
        inicial = True
        

        queryset = cls.objects.filter(~Q(numeracion__tipoDocumento=numeracion.PROFORMA)).select_related(
            'numeracion',
            'cliente',
            'formaPago',
            'vendedor',
            'usuario',
        )
        
        if 'prefijo' in obj and obj['prefijo'] is not None and obj['prefijo'].strip()  != '' :
            queryset = queryset.filter(prefijo__iexact=obj['prefijo'])
            inicial = False

        if 'numero' in obj and obj['numero'] is not None:
            queryset = queryset.filter(consecutivo=int(obj['numero']))
            inicial = False

        if 'cliente' in obj and obj['cliente'] is not None:
            queryset = queryset.filter(cliente__id=obj['cliente'])
            inicial = False

        if 'fechaInicial' in obj and 'fechaFinal' in obj and obj['fechaInicial'] is not None and obj['fechaFinal'] is not None:
            fecha_inicial = obj['fechaInicial']
            fecha_final = obj['fechaFinal']


            fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%dT%H:%M:%S.%fZ")
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ")





            fecha_inicial = fecha_inicial.strftime("%Y-%m-%d") 
            fecha_final   = fecha_final.strftime("%Y-%m-%d")

            # fecha_inicial = datetime.strptime(fecha_inicial_str, '%Y-%m-%dT%H:%M:%S')
            # fecha_final   = datetime  .strptime(fecha_final_str, '%Y-%m-%dT%H:%M:%S')

            if fecha_inicial and fecha_final:
                queryset = queryset.filter(fecha__gte=fecha_inicial, fecha__lte=fecha_final)
                inicial = False

        if 'observacion' in obj and obj['observacion'] is not None and obj['observacion'].strip()  != '':
            queryset = queryset.filter(observacion__icontains=obj['observacion'])
            inicial = False

        if 'formaPago' in obj and obj['formaPago'] is not None:
            queryset = queryset.filter(formaPago__id=obj['formaPago'])
            inicial = False

        if 'vendedor' in obj and obj['vendedor'] is not None:
            queryset = queryset.filter(vendedor__id=obj['vendedor'])
            inicial = False

        if 'valor' in obj and obj['valor'] is not None :
            queryset = queryset.filter(valor=obj['valor'])
            inicial = False

        if 'estadoDian' in obj and obj['estadoDian'] is not None :
            queryset = queryset.filter(isElectronica=True, enviadaDian=obj['estadoDian'])
            inicial = False

      
        if inicial:
            return filter_and_combine(queryset)


        print(obj)
        return queryset.order_by('-fecha','despachado','-numero')


    @classmethod
    def filter_by_criterio_proformas(cls, obj):
        

        inicial = True

        queryset = cls.objects.filter(Q(numeracion__tipoDocumento=numeracion.PROFORMA)).select_related(
            'numeracion',
            'cliente',
            'formaPago',
            'vendedor',
            'usuario',
        )
        
        if 'prefijo' in obj and obj['prefijo'] is not None and obj['prefijo'].strip()  != '' :
            queryset = queryset.filter(prefijo__iexact=obj['prefijo'])
            inicial = False

        if 'numero' in obj and obj['numero'] is not None:
            queryset = queryset.filter(consecutivo=int(obj['numero']))
            inicial = False

        if 'cliente' in obj and obj['cliente'] is not None:
            queryset = queryset.filter(cliente=obj['cliente'])
            inicial = False

        if 'fechaInicial' in obj and 'fechaFinal' in obj and obj['fechaInicial'] is not None and obj['fechaFinal'] is not None:
                fecha_inicial = obj['fechaInicial']
                fecha_final = obj['fechaFinal']


                fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%dT%H:%M:%S.%fZ")
                fecha_final = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ")





                fecha_inicial = fecha_inicial.strftime("%Y-%m-%d") 
                fecha_final   = fecha_final.strftime("%Y-%m-%d")


                if fecha_inicial and fecha_final:
                    queryset = queryset.filter(fecha__gte=fecha_inicial, fecha__lte=fecha_final)
                    inicial = False

        if 'observacion' in obj and obj['observacion'] is not None and obj['observacion'].strip()  != '' :
            queryset = queryset.filter(observacion__icontains=obj['observacion'])
            inicial = False

        if 'formaPago' in obj and obj['formaPago'] is not None:
            queryset = queryset.filter(formaPago=obj['formaPago'])
            inicial = False

        if 'vendedor' in obj and obj['vendedor'] is not None:
            queryset = queryset.filter(vendedor=obj['vendedor'])
            inicial = False

        if 'valor' in obj and obj['valor'] is not None:
            queryset = queryset.filter(valor=obj['valor'])
            inicial = False

      
        if inicial:
            return  queryset.order_by('-fecha','proformada','-numero')[:20]

        return queryset.order_by('-fecha','proformada','-numero')



    @classmethod
    def convertir_proformas_a_factura(cls, datos, usuario):
        from apps.stock.models import Kardex
        from apps.configuracion.models import RetencionesClientes,Impuestos
        from .functions import contabilizarFacturas

        with transaction.atomic():
            num = numeracion()

            isElectronica = None

            proformas = datos['values']
            if datos['type'] == 'ELECTRONICA':
                num = numeracion.objects.filter(tipoDocumento=num.FACTURA_ELECTRONICA,estado = True)[0]
                isElectronica = True
            else:
                num = numeracion.objects.filter(tipoDocumento=num.FACTURA_POS,estado = True)[0]
                isElectronica = False
            pf = cls.objects.get(numero=proformas[0])


            # Crear una nueva instancia de CxcMovi
            newVenta = CxcMovi()
            newCxc   = CxcVentas()


            newVenta.numeracion      = num
            newVenta.consecutivo     = num.proximaFactura
            newVenta.prefijo         = num.prefijo
            newVenta.numero          = num.prefijo+'-'+str(num.proximaFactura).zfill(4)
            newVenta.cliente         = pf.cliente
            newVenta.formaPago       = pf.cliente.formaPago
            newVenta.fecha           = date.today()
            newVenta.observacion     = 'PROFORMA N°: '+', '.join(map(str, proformas))
            newVenta.valorLetras     = ""
            newVenta.vendedor        = pf.cliente.vendedor
            newVenta.usuario         = usuario
            newVenta.isElectronica   = isElectronica
            newVenta.subtotal        = 0
            newVenta.valorReteFuente = 0
            newVenta.valorDomicilio  = 0
            newVenta.valorIva        = 0
            newVenta.descuento       = 0
            newVenta.valor           = 0
            newVenta.save()
            
         


            
            for x in datos['values']:
                # Obtener el detalle proforma 
                proforma_original = cls.objects.get(numero=x)
                proforma_original_detalle = proforma_original.detalle_factura.all()

                proforma_original.proformada = True


                detalleFacturaSave = []
                for item in proforma_original_detalle:
                    
                    facturaDetalleObject = CxcMoviDetalle() 
                    kardexObject         = Kardex()
                    product              = item.producto

                    # ValidarInventario(product,item['lote'],item['cantidad'])
                    facturaDetalleObject.factura          = newVenta
                    facturaDetalleObject.producto         = product
                    facturaDetalleObject.cantidad         = item.cantidad
                    facturaDetalleObject.valor            = item.valor
                    facturaDetalleObject.valorCompra      = item.valorCompra
                    facturaDetalleObject.lote             = item.lote
                    facturaDetalleObject.vence            = item.vence

                    facturaDetalleObject.iva = item.iva
                  
                    facturaDetalleObject.descuento = item.descuento
                    
                    
                    facturaDetalleObject.subtotal = item.subtotal
                    facturaDetalleObject.total    = item.total

                    facturaDetalleObject.save()

                    detalleFacturaSave.append(facturaDetalleObject)

                    newVenta.subtotal        += item.subtotal
                    newVenta.valorIva        += item.iva * item.cantidad
                    newVenta.descuento       += item.descuento * item.cantidad
                    newVenta.valor           += item.total

                    
                    kardexObject.descripcion = 'Factura No. '+facturaDetalleObject.factura.numero
                    kardexObject.tipo        = 'FA'
                    
                    
                    kardexObject.producto    = facturaDetalleObject.producto
                    kardexObject.tercero     = facturaDetalleObject.factura.cliente
                    kardexObject.bodega      = facturaDetalleObject.producto.bodega
                    kardexObject.unidades    = 0 - facturaDetalleObject.cantidad
                    kardexObject.balance     = facturaDetalleObject.producto.stock_inicial
                    kardexObject.precio      = facturaDetalleObject.valor

                    kardexObject.save()

                proforma_original.save()

            retencion = RetencionesClientes.objects.filter(tercero__id = newVenta.cliente.id)
            for r in retencion:
                reteFac = RetencionCxc()
                if r.fija:
                    reteFac.factura    = newVenta
                    reteFac.retencion  = r.retencion
                    reteFac.base       = newVenta.subtotal - newVenta.descuento
                    reteFac.procentaje = r.retencion.porcentaje
                    reteFac.total      = reteFac.base * reteFac.procentaje / 100

                    newVenta.valorReteFuente = reteFac.total
                    reteFac.save()
                else:
                    if r.retencion.base > 0 and (newVenta.subtotal - newVenta.descuento) >= r.retencion.base:
                        # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                        reteFac.factura    = newVenta
                        reteFac.retencion  = r.retencion 
                        reteFac.base       = newVenta.subtotal -  newVenta.descuento
                        reteFac.procentaje = r.retencion.porcentaje
                        reteFac.total      = reteFac.base * reteFac.procentaje / 100
                        newVenta.valorReteFuente = reteFac.total
                        reteFac.save()    

            if newVenta.valorIva > 0:
                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                        impFactura = ImpuestoCxc()
                        impFactura.factura    = newVenta
                        impFactura.impuesto   = imp
                        impFactura.procentaje = imp.porcentaje
                        totalIva = 0
                        totalBase = 0
                        for item in detalleFacturaSave:
                                if item.iva > 0:
                                        totalIva += item.iva * item.cantidad
                                        totalBase += (float(item.valor) -  float(item.descuento)) * item.cantidad
                        impFactura.base       = totalBase
                        impFactura.total      = totalIva    
                        impFactura.save()

            newVenta.valor = newVenta.subtotal - newVenta.descuento - newVenta.valorReteFuente
            newVenta.valor += newVenta.valorIva 
            newVenta.save()


                
            newCxc.cxc              = newVenta
            newCxc.factura          = newVenta.numero
            newCxc.formaPago        = newVenta.formaPago
            newCxc.fecha            = newVenta.fecha
            newCxc.fechaVencimiento = newVenta.fechaVencimiento
            newCxc.observacion      = newVenta.observacion
            newCxc.cliente          = newVenta.cliente
            newCxc.base             = newVenta.subtotal
            newCxc.iva              = newVenta.valorIva
            newCxc.reteFuente       = newVenta.valorReteFuente
            newCxc.valorTotal       = newVenta.valor

            newCxc.save()

            contabilizarFacturas(newVenta,detalleFacturaSave)

            num.proximaFactura += 1
            num.save()
            return newVenta.numero
    


class CxcMoviDetalle(models.Model):
    """Model definition for CxcMoviDetalle."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key= True)
    factura     = models.ForeignKey(CxcMovi, related_name= "detalle_factura", on_delete = models.PROTECT)
    producto    = models.ForeignKey("stock.Productos", related_name="producto_detalle_factura", on_delete = models.PROTECT)
    valorCompra = models.FloatField()
    valor       = models.FloatField()
    cantidad    = models.IntegerField()
    vence       = models.DateField('vencimiento:', auto_now=False, auto_now_add=False)
    descuento   = models.FloatField()
    lote        = models.CharField('lote: ', max_length= 50)
    subtotal    = models.FloatField()
    descuento   = models.FloatField(default= 0)
    iva         = models.FloatField(default= 0)
    total       = models.FloatField()


    class Meta:
        """Meta definition for CxcMoviDetalle."""

        verbose_name = 'CxcMoviDetalle'
        verbose_name_plural = 'CxcMoviDetalles'

    def __str__(self): 
        return f'{self.id}, {self.producto.nombre}'
    
class CxcVentas(models.Model):
    """Model definition for Cxc."""

    # TODO: Define fields here
    # ==== Tipos de estado ==== 
    # False = Pendiente x Pago 
    # True = Pagada
    id                 = models.AutoField(primary_key=True)
    cxc                = models.ForeignKey(CxcMovi, related_name="CxcVentas_factura", on_delete=models.PROTECT,db_index=True)
    factura            = models.CharField("Factura:", max_length=50, blank=True, null=True,db_index=True)
    formaPago          = models.ForeignKey(to='configuracion.FormaPago', related_name="cxcventas_formaPago",on_delete=models.PROTECT, blank=True, null=True,db_index=True)
    fecha              = models.DateField("Fecha:", auto_now=False, auto_now_add=False, blank=True, null=True, db_index=True)
    fechaVencimiento   = models.DateField("Fecha de Vencimiento:", auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion        = models.TextField("Observación:", blank=True, null=True)
    cliente            = models.ForeignKey("configuracion.Terceros", related_name="cxcventas_cliente",on_delete=models.PROTECT,db_index=True)
    estado             = models.BooleanField(default=False)
    notacredito        = models.BooleanField(default=False)
    notadebito         = models.BooleanField(default=False)
    base               = models.FloatField(default=0)
    iva                = models.FloatField(default=0)
    valorDescuento     = models.FloatField(default=0)
    valorAbono         = models.FloatField(default=0)
    reteFuente         = models.FloatField(default=0)
    reteIca            = models.FloatField(default=0)
    valorTotal         = models.FloatField(default=0)
    class Meta:
        """Meta definition for Cxc."""

        verbose_name = 'Cuenta por cobrar'
        verbose_name_plural = 'Cuentas por cobrar'
        db_table = 'cxc'

    def __str__(self):
        """Unicode representation of Cxc."""
        return self.factura

    @classmethod
    def filter_cxc(cls, obj):

        filtro = cls.objects.prefetch_related(
            'cxc',
            'formaPago',
            'cliente'
        ).order_by('-fecha')
        
        condiciones = []
        
        if 'cliente' in obj and obj['cliente'] is not None:
            condiciones.append(Q(cliente__id=obj['cliente']))
        
        if 'factura' in obj and obj['factura'] is not None:
            condiciones.append(Q(factura__icontains=obj['factura']))
        
        if 'estado' in obj and obj['estado'] is not None:
            condiciones.append(Q(estado=obj['estado']))
        
        if 'formaDePago' in obj and obj['formaDePago'] is not None:
            condiciones.append(Q(formaPago__id=obj['formaDePago']))
        
        if 'fechaInicial' in obj and 'fechaFinal' in obj:
            if obj['fechaInicial'] is not None and obj['fechaFinal'] is not None:
                    fecha_inicial = obj['fechaInicial']
                    fecha_final = obj['fechaFinal']

                    fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%dT%H:%M:%S.%fZ")
                    fecha_final = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ")

                    fecha_inicial = fecha_inicial.strftime("%Y-%m-%d") 
                    fecha_final   = fecha_final.strftime("%Y-%m-%d")


                    if fecha_inicial and fecha_final:
                        condiciones.append(Q(fecha__gte=fecha_inicial, fecha__lte=fecha_final))
                        
                       
                    

                
        if 'year' in obj and obj['year'] is not None:
            condiciones.append(Q(fecha__year=obj['year']))
        
        if 'mes' in obj and obj['mes'] is not None:
            condiciones.append(Q(fecha__month=obj['mes']))
        
        if not condiciones:
            filtro = filtro[:20]
        else:
            filtro = filtro.filter(*condiciones)
        
        return filtro
    
        
class NotaCreditoVentas(models.Model):

    DEVOLUCION = '1'
    REBAJA_PRECIO = '2'
    ANULACION = '3'

    TIPO_DE_NOTAS_CHOICES = (
        (DEVOLUCION, 'Devoluciones'),
        (REBAJA_PRECIO, 'Rebajas o disminución de precio'),
        (ANULACION, 'Anulación total'),
       
    )

  

    """Model definition for NotaCredito."""

    # TODO: Define fields here
    id              = models.AutoField(primary_key=True)  
    numeracion      = models.ForeignKey("configuracion.numeracion", related_name="NotaCreditoV_numeracion",on_delete=models.PROTECT)
    numero          = models.CharField("Numero:", max_length=20, blank=True, null=True)
    consecutivo     = models.IntegerField(blank=True, null=True)
    prefijo         = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    tipoNota        = models.CharField("Tipo de nota:", max_length=50, choices=TIPO_DE_NOTAS_CHOICES)
    cxc             = models.ForeignKey(CxcMovi, related_name="NotaCredito_venta",on_delete=models.PROTECT)
    fecha           = models.DateField('fecha:', auto_now=False, auto_now_add=False)
    cliente         = models.ForeignKey("configuracion.Terceros", related_name="NotaCreditoV_proveedor",on_delete=models.PROTECT)
    observacion     = models.TextField(default = "", blank=True, null=True)
    subtotal        = models.FloatField(default=0)
    iva             = models.FloatField(default=0)
    retencion       = models.FloatField(default=0)
    total           = models.FloatField()
    contabilizado   = models.BooleanField(default=False)
    isElectronica   = models.BooleanField(default= False)
    enviadaDian     = models.BooleanField(default= False)
    transaccionID   = models.TextField()
    usuario         = models.ForeignKey("users.User", related_name="notaCreditoV_usuario",on_delete=models.PROTECT)



    class Meta:
        """Meta definition for NotaCredito."""

        verbose_name = 'Nota credito venta'
        verbose_name_plural = 'nota creditos ventas'
        db_table = 'notacreditoventas'

    def __str__(self):
        """Unicode representation of NotaCredito."""
        return self.numero
    
    def save(self, *args, **kwargs):
       super(NotaCreditoVentas, self).save(*args, **kwargs) # Call the real save() method
    
class DetalleNotaCreditoVentas(models.Model):
    """Model definition for DetalleNotaCredito."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    nota        = models.ForeignKey(NotaCreditoVentas, related_name="detalle_NotaCredito_venta" , on_delete=models.PROTECT)
    producto    = models.ForeignKey("stock.Productos", related_name = "prdoucto_notaCreditoDetalleVenta", on_delete=models.PROTECT)
    lote        = models.CharField("Lote:", max_length=50)
    cantidad    = models.IntegerField()
    valorCompra = models.FloatField()
    valorUnidad = models.FloatField()
    iva         = models.FloatField(default=0)
    subtotal    = models.FloatField()


    class Meta:
        """Meta definition for DetalleNotaCredito."""

        verbose_name = 'Detalle Nota Credito venta'
        verbose_name_plural = 'Detalles Notas Creditos Ventas'
        db_table = 'notacreditodetalleVenta'

    def __str__(self):
        """Unicode representation of DetalleNotaCredito."""
        return self.nota.numero
    



class ImpuestoCxc(models.Model):
    """Model definition for ImpuestoIngreso."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    factura     = models.ForeignKey(CxcMovi, related_name="impuesto_cxc", on_delete=models.PROTECT)
    impuesto    = models.ForeignKey("configuracion.Impuestos", related_name="impuestos_cxc",on_delete=models.PROTECT)
    base        = models.FloatField()
    procentaje  = models.FloatField('porcentaje')
    total       = models.FloatField()

    class Meta:
        """Meta definition for ImpuestoIngreso."""

        verbose_name = 'Impuesto factura'
        verbose_name_plural = 'Impuestos Facturas'
 

    def __str__(self):
        """Unicode representation of ImpuestoIngreso."""
        return self.factura.numero

class RetencionCxc(models.Model):
    """Model definition for RetencionIngreso."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    factura     = models.ForeignKey(CxcMovi, related_name="retencion_cxc",on_delete=models.PROTECT)
    retencion   = models.ForeignKey("configuracion.Retenciones", related_name="reteciones_cxc",on_delete=models.PROTECT)
    base        = models.FloatField()
    procentaje  = models.FloatField('porcentaje')
    total       = models.FloatField()

    class Meta:
        """Meta definition for RetencionIngreso."""

        verbose_name = 'Retenciones facturas '
        verbose_name_plural = 'Retenciones Documentos Ventas'
    

    def __str__(self):
        """Unicode representation of RetencionIngreso."""
        return self.factura.numero
    

class PagosVentas(models.Model):
    """Model definition for PagosVentas."""


    # TODO: Define fields here
    id              = models.AutoField(primary_key=True)
    numeracion      = models.ForeignKey("configuracion.numeracion", related_name="pagos_numeracion_ingreso" ,on_delete=models.PROTECT)
    numero          = models.CharField("Numero:", max_length=20, blank=True, null=True)
    consecutivo     = models.IntegerField(blank=True, null=True)
    prefijo         = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    usuario         = models.ForeignKey("users.User", related_name="pagos_usuario_ingreso",on_delete=models.PROTECT)
    cliente         = models.ForeignKey("configuracion.terceros", related_name="pagos_cliente" ,on_delete=models.PROTECT)
    fecha           = models.DateField("Fecha:", auto_now=False, auto_now_add=False)
    cuenta          = models.ForeignKey('contabilidad.puc', on_delete=models.PROTECT)
    concepto        = models.TextField("Concepto:", blank=True, null=True)
    observacion     = models.TextField("Observacion:", blank=True, null=True)
    total           = models.FloatField(default=0)

    class Meta:
        """Meta definition for PagosCompras."""

        verbose_name = 'pagosVentas'
        verbose_name_plural = 'pagosVentas'
        db_table = 'pagosVentas'

    def __str__(self):
        """Unicode representation of PagosCompras."""
        return self.numero
    

class DetailPaymentInvoiceVentas(models.Model):
    """Model definition for PagoDetalle."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    cxc         = models.ForeignKey(CxcMovi, related_name="detalle_factura_pago", on_delete=models.PROTECT)
    pago        = models.ForeignKey(PagosVentas, related_name="detalle_pago" ,on_delete=models.PROTECT)
    factura     = models.CharField("Factura:", max_length=50)
    descuento   = models.FloatField(default=0)
    saldoAFavor = models.FloatField(default=0)
    saldo       = models.FloatField(default=0)
    totalAbono  = models.FloatField(default=0)
    retefuente  = models.FloatField(default=0)
    reteica     = models.FloatField(default=0)

    class Meta:
        """Meta definition for PagosCompras."""

        verbose_name = 'DetailPaymentInvoice'
        verbose_name_plural = 'DetailPaymentInvoice'
    

    def __str__(self):
        """Unicode representation of PagosCompras."""
        return self.factura
        


class CotizacionInformal(models.Model):
    """Model definition for CxcMovi."""


    # TODO: Define fields here
    id                 = models.AutoField(primary_key = True)
    numeracion         = models.ForeignKey(to="configuracion.numeracion", related_name="numeracion_cotizacion", on_delete=models.PROTECT)
    consecutivo        = models.IntegerField()
    numero             = models.CharField('numero', max_length=50, unique=True)
    prefijo            = models.CharField('prefijo', max_length=50)
    cliente            = models.CharField('cliente', max_length=250)
    fecha              = models.DateField('Fecha', auto_now=False, auto_now_add=True)
    hora               = models.TimeField('Hora', auto_now=True, auto_now_add=False)
    valor              = models.FloatField()
    descuento          = models.FloatField(default = 0)
    valorLetras        = models.CharField('Valor en letras', max_length=250)
    observacion        = models.CharField('Observacion', max_length=350,blank=True, null=True)
    formaPago          = models.CharField('formaPago', max_length=100)
    usuario            = models.ForeignKey("users.User",models.PROTECT)
    valorIva           = models.FloatField(default = 0)
    valorReteFuente    = models.FloatField(default = 0)
    subtotal           = models.FloatField(default = 0)

    class Meta:
        """Meta definition for CotizacionInformal."""

        verbose_name = 'CotizacionInformal'
        verbose_name_plural = 'CotizacionInformal'
        

    def __str__(self): 
        return f'{self.numero}'
    
  

class DetalleCotizacionInformal(models.Model):
    """Model definition for CxcMoviDetalle."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key= True)
    cotizacion  = models.ForeignKey(CotizacionInformal, related_name= "detalle_cotizacion_informal", on_delete = models.PROTECT)
    producto     = models.CharField('producto', max_length=250)
    valorCompra = models.FloatField()
    valor       = models.FloatField()
    cantidad    = models.IntegerField()
    vence       = models.DateField('vencimiento:', auto_now=False, auto_now_add=False)
    subtotal    = models.FloatField()
    descuento   = models.FloatField(default= 0)
    iva         = models.FloatField(default= 0)
    total       = models.FloatField()


    class Meta:
        """Meta definition for DetalleCotizacionInformal."""

        verbose_name = 'DetalleCotizacionInformal'
        verbose_name_plural = 'DetalleCotizacionInformal'

    def __str__(self): 
        return f'{self.id}, {self.producto}'

    



def filter_and_combine(queryset):
    is_electronica_true = queryset.filter(isElectronica=True).order_by('-fecha', '-numero')[:10]
    is_electronica_false = queryset.filter(isElectronica=False).order_by('-fecha', '-numero')[:10]

    combined_results = []

    for true_row, false_row in zip(is_electronica_true, is_electronica_false):
        combined_results.append(true_row)
        combined_results.append(false_row)

    return combined_results


post_save.connect(update_factura_pago,sender=DetailPaymentInvoiceVentas)
post_delete.connect(delete_factura_pago,sender=DetailPaymentInvoiceVentas)
