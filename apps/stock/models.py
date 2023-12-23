from django.db import models
# from .manager import OrdenManager
# Create your models here.
from datetime import date, timedelta, datetime
from apps.configuracion.models import *
from .signals import *
from django.db.models.signals import post_save,post_delete

from django.utils import timezone


class Bodega(models.Model):
    """Model definition for Bodega."""

    # TODO: Define fields here
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Bogeda', max_length=100)

    class Meta:
        """Meta definition for Bodega."""

        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        

    def __str__(self):
        return self.nombre

class tipoProducto(models.Model):
    """Model definition for Bodega."""

    # TODO: Define fields here
    id         = models.AutoField(primary_key          = True)
    nombre     = models.CharField('TIPO', max_length = 100)
    bodega     = models.ForeignKey(Bodega, related_name="bodega_tiposP", on_delete=models.PROTECT)
    c_tipo     = models.ForeignKey(to='contabilidad.puc',related_name='cuenta_tipo',verbose_name='Cuenta inventario:', on_delete=models.PROTECT)
    c_ingreso  = models.ForeignKey(to='contabilidad.puc',related_name='cuenta_ingreso',verbose_name='Cuenta Ingreso:', on_delete=models.PROTECT)
    c_dev      = models.ForeignKey(to='contabilidad.puc',related_name='cuenta_dev_ingreso',verbose_name='Cuenta Devolucion Ingreso:', on_delete=models.PROTECT)
    c_costo    = models.ForeignKey(to= 'contabilidad.puc',related_name='cuenta_costo',verbose_name='Cuenta Costo', on_delete=models.PROTECT)
    c_gasto    = models.ForeignKey(to= 'contabilidad.puc',related_name='cuenta_gasto',verbose_name='Cuenta Gasto', on_delete=models.PROTECT)

    class Meta:
        """Meta definition for Bodega."""

        verbose_name = 'tipoProducto'
        verbose_name_plural = 'tiposDeProductos'
       

    def __str__(self):
        return self.nombre


class Productos(models.Model):
    id                = models.AutoField(primary_key = True)  # Field name made lowercase.
    nombre            = models.CharField('Nombre', max_length = 150)
    Filtro            = models.CharField('Filtro', max_length  = 150)
    invima            = models.CharField(max_length           = 50, blank = True, null = True)
    cum               = models.CharField(max_length = 50, blank = True, null = True, default="N/A")
    valorCompra       = models.FloatField()
    valorVenta        = models.FloatField(blank = True, null = True)
    valorventa1       = models.FloatField(blank = True, null = True)
    valorventa2       = models.FloatField(blank = True, null = True)
    fv                = models.BooleanField(default = True)
    regulado          = models.BooleanField(default = False)
    valorRegulacion   = models.FloatField(default = 0)
    laboratorio       = models.CharField('Laboratorio:', max_length=150, blank=False, null=False)

    stock_inicial     = models.IntegerField(default = 0)
    stock_min         = models.IntegerField(default = 0)
    stock_max         = models.IntegerField(default = 0)
    tipoProducto      = models.ForeignKey(tipoProducto, related_name="productos_tipo_producto",on_delete=models.PROTECT)
    habilitado        = models.BooleanField(default = True)
    bodega            = models.ForeignKey(Bodega, on_delete=models.PROTECT)
    impuesto          = models.ForeignKey("configuracion.Impuestos", blank=True, null=True, related_name="productos_impuesto",on_delete=models.PROTECT)
    codigoDeBarra     = models.CharField(max_length=50, blank=True, null=True)  # Field name made lowercase.
    unidad            = models.CharField('Unidad', max_length=150)
    usuario           = models.ForeignKey("users.User", related_name="productos_usuario",on_delete=models.PROTECT)
    creado            = models.DateTimeField(auto_now=True)
    modificado        = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    nombreymarcaunico = models.CharField(unique=True, max_length=900, blank=True, null=True)
    
    class Meta:
        """Meta definition for Iventario."""

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        

    def __str__(self):
        return self.codigoDeBarra+' - '+self.nombre


    # def save(self, *args, **kwargs):
    #         code = self.nombre[0:3]
    #         p = Productos.objects.filter(nombre__icontains=code)
    #         n = p.count() + 1
    #         self.codigoDeBarra = code+str(n).rjust(2, '0')
    #         invima = ""
    #         cum = ""
    #         if self.invima != "":
    #             invima = 'INV:'+self.invima
    #         if self.cum != "":
    #             cum = 'CUM:'+self.cum
    #         self.nombreymarcaunico = self.nombre
    #         super(Productos, self).save(*args, **kwargs)
    
    
    # def save(self, *args, **kwargs):
    #     t = Terceros.objects.get(documento = "1221981200")
    #     k = Kardex()
    #     k.producto = self       
    #     k.descripcion = "Saldo Inicial"
    #     k.tipo       = "SI"
    #     k.tercero    = t
    #     k.bodega     = self.bodega   
    #     k.unidades   = self.stock_inicial
    #     k.balance    = self.stock_inicial
    #     k.precio     = self.valorCompra
    #     k.save()
    #     super(Productos, self).save(*args, **kwargs)






class Kardex(models.Model):
    """Model definition for Kardex."""
    id          = models.AutoField(primary_key = True)
    descripcion = models.CharField('descripcion', max_length= 250)
    tipo        = models.CharField('tipo', max_length= 50)
    producto    = models.ForeignKey(Productos, related_name="kardexs_producto", on_delete = models.PROTECT)
    tercero     = models.ForeignKey("configuracion.Terceros", related_name="kardexs_terceros",on_delete = models.PROTECT)
    bodega      = models.ForeignKey(Bodega, on_delete= models.PROTECT,related_name = "kardexs_bodega")
    unidades    = models.IntegerField()
    fecha       = models.DateField("fecha:", auto_now=False, auto_now_add=False)
    balance     = models.IntegerField(default= 0)
    precio      = models.FloatField()


    # TODO: Define fields here

    class Meta:
        """Meta definition for Kardex."""

        verbose_name = 'Kardex'
        verbose_name_plural = 'Kardex'
        db_table = 'kardexs'

    def __str__(self):
       return self.descripcion
    
    def save(self, *args, **kwargs):
        if self.fecha is None:
            self.fecha = timezone.now().date()
        super().save(*args, **kwargs)


class Inventario(models.Model):
    """Model definition for Iventario."""
    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    bodega      = models.ForeignKey(Bodega, related_name="inventario_bodega", on_delete=models.PROTECT)
    idProducto  = models.ForeignKey(Productos, related_name="inventario_producto", on_delete=models.PROTECT)
    vencimiento = models.DateField('Fecha vencimiento', auto_now=False, auto_now_add=False, null=True, blank=True)
    valorCompra = models.FloatField()
    unidades    = models.IntegerField()
    lote        = models.CharField('lote', max_length=50)
    estado      = models.BooleanField()
    class Meta:
        """Meta definition for Iventario."""

        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return self.lote

    @classmethod
    def obtener_valor_compra_mas_alto(cls, id_producto, lote):
        valor_maximo = cls.objects.filter(
            idProducto__id=id_producto,
            lote=lote,
            unidades__gt=0
        ).aggregate(models.Max('valorCompra'))['valorCompra__max']
        
        return valor_maximo

class OrdenDeCompra(models.Model):
    """Model definition for OrdenDeCompra"""
    # TODO: Define the fields here
    id          = models.AutoField(primary_key=True)
    numeracion  = models.ForeignKey("configuracion.numeracion", related_name="numeracion_orden", on_delete=models.PROTECT)
    numero      = models.CharField("Numero:", max_length=20, blank=True, null=True)
    consecutivo = models.IntegerField(blank=True, null=True)
    prefijo     = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    proveedor   = models.ForeignKey("configuracion.Terceros", related_name="Orden_proveedor",on_delete=models.PROTECT)
    fecha       = models.DateTimeField("Fecha:", auto_now=False, auto_now_add=False)
    formaPago   = models.ForeignKey("configuracion.FormaPago", related_name="orden_formaPago",on_delete=models.PROTECT)
    usuario     = models.ForeignKey("users.User", related_name="orden_usuario",on_delete=models.PROTECT)
    observacion = models.TextField(default="", blank=True, null=True)
    subtotal    = models.FloatField()
    iva         = models.FloatField()
    retencion   = models.FloatField()
    ingresada   = models.BooleanField(default = False, blank=True, null=True)
    descuento   = models.FloatField(default = 0)
    total       = models.FloatField()   

    class Meta:
        """Meta definition for OrdenDeCompra"""
        
        verbose_name = "Orden de compra"
        verbose_name_plural = "Orden de Compras"
        db_table = 'ordendecompra'

    def __str__(self):
        return self.numero
    
    
 

class OrdenDetalle(models.Model):
    """Model definition for DettaleOrden"""
    # TODO: Define the fields here
    id          = models.AutoField(primary_key=True)
    orden       = models.ForeignKey(OrdenDeCompra, related_name="detalle_orden",on_delete=models.PROTECT)
    producto    = models.ForeignKey(Productos, related_name="detalleOrden_productos",on_delete=models.PROTECT)
    cantidad    = models.IntegerField()
    valorUnidad = models.FloatField()
    descuento   = models.FloatField(default = 0)
    iva         = models.FloatField()

    class Meta:
        """Meta definition for DetalleOrden"""

        verbose_name = "Detalle de Orden"
        verbose_name_plural = "Detalle de Ordenes"
        db_table = "ordendetalle"

    def __str__(self):
        return self.orden.numero

class ImpuestoOrden(models.Model):
    """Model definition for ImpuestoOrden"""
    # TODO: Define the fields here
    id          = models.AutoField(primary_key=True)
    orden       = models.ForeignKey(OrdenDeCompra, related_name="impuesto_orden" ,on_delete=models.PROTECT)
    impuesto    = models.ForeignKey("configuracion.Impuestos", related_name="impuestos_orden",on_delete=models.PROTECT)
    base        = models.FloatField()
    procentaje  = models.FloatField()
    total       = models.FloatField()

    class Meta:
        """Meta definition for ImpuestoOrden"""

        verbose_name = "Impuesto de orden"
        verbose_name_plural = "Impuesto de ordenes"
        db_table = "impuesto_orden"

    def __str__(self):
        return self.orden.numero

class RetencionOrden(models.Model):
    """Model definition for RetencionOrden"""
    # TODO: Define the fields here
    id          = models.AutoField(primary_key=True)
    orden       = models.ForeignKey(OrdenDeCompra, related_name="retencion_orden", on_delete=models.PROTECT)
    retencion   = models.ForeignKey("configuracion.Retenciones", related_name="retenciones_orden",on_delete=models.PROTECT)
    base        = models.FloatField()
    porcentaje  = models.FloatField()
    total       = models.FloatField()

    class Meta:
        """Meta definition for RetencionOrden"""

        verbose_name = "Retencion de orden"
        verbose_name_plural = "Retencion de ordenes"
        db_table = "retencionesorden"

    def __str__(self):
        return self.orden.numero               

class Ingreso(models.Model):
    """Model definition for Ingreso."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    numeracion  = models.ForeignKey("configuracion.numeracion", related_name="ingreso_numeracion",on_delete=models.PROTECT)
    numero      = models.CharField("Numero:", max_length=20, blank=True, null=True)
    consecutivo = models.IntegerField(blank=True, null=True)
    prefijo     = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    orden       = models.ForeignKey(OrdenDeCompra, related_name="ingreso_orden" , on_delete=models.PROTECT)
    factura     = models.CharField("Factura:", max_length=50)
    proveedor   = models.ForeignKey("configuracion.Terceros", related_name="ingreso_proveedor",on_delete=models.PROTECT)
    fecha       = models.DateField("Fecha:", auto_now=False, auto_now_add=False)
    formaPago   = models.ForeignKey("configuracion.FormaPago", related_name="ingreso_formaPago",on_delete=models.PROTECT)
    usuario      = models.ForeignKey("users.User", related_name="ingreso_usuario" ,on_delete=models.PROTECT)
    observacion = models.TextField(default="", blank=True, null=True)
    subtotal    = models.FloatField()
    iva         = models.FloatField()
    retencion   = models.FloatField()
    descuento   = models.FloatField(default = 0)
    total       = models.FloatField()

    class Meta:
        """Meta definition for Ingreso."""

        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        db_table = "ingreso"


    def __str__(self):
        """Unicode representation of Ingreso."""
        return  str(self.numero)
    
class IngresoDetalle(models.Model):
    """Model definition for IngresoDetalle."""

    # TODO: Define fields here
    id               = models.AutoField(primary_key=True)
    ingreso          = models.ForeignKey(Ingreso, related_name="ingreso_detalle" ,on_delete=models.PROTECT)
    producto         = models.ForeignKey(Productos, related_name="ingreso_producto",on_delete=models.PROTECT)
    cantidad         = models.IntegerField()
    fechaVencimiento = models.DateField("Fecha de vencimiento:", auto_now=False, auto_now_add=False, blank=True, null=True)
    lote             = models.CharField("Lote:", max_length=50)
    valorUnidad      = models.FloatField()
    descuento        = models.FloatField(default = 0)
    iva              = models.FloatField()
    subtotal         = models.FloatField()
    total            = models.FloatField()

    class Meta:
        """Meta definition for IngresoDetalle."""

        verbose_name = 'IngresoDetalle'
        verbose_name_plural = 'IngresoDetalles'
        db_table = 'ingresodetalle'

    def __str__(self):
        """Unicode representation of IngresoDetalle."""
        return self.ingreso.numero

class ImpuestoIngreso(models.Model):
    """Model definition for ImpuestoIngreso."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    ingreso     = models.ForeignKey(Ingreso, related_name="impuesto_ingreso", on_delete=models.PROTECT)
    impuesto    = models.ForeignKey("configuracion.Impuestos", related_name="impuestos_ingreso",on_delete=models.PROTECT)
    base        = models.FloatField()
    fecha       = models.DateField('fecha', auto_now=False, auto_now_add=False)
    procentaje  = models.FloatField()
    total       = models.FloatField()

    class Meta:
        """Meta definition for ImpuestoIngreso."""

        verbose_name = 'ImpuestoIngreso'
        verbose_name_plural = 'ImpuestoIngresos'
        db_table = "impuestoingreso"

    def __str__(self):
        """Unicode representation of ImpuestoIngreso."""
        return self.ingreso.numero


    def save(self, *args, **kwargs):
        self.fecha = datetime.strptime(str(self.ingreso.fecha),"%Y-%m-%d")

        super(ImpuestoIngreso, self).save(*args, **kwargs)


class RetencionIngreso(models.Model):
    """Model definition for RetencionIngreso."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    ingreso     = models.ForeignKey(Ingreso, related_name="retencion_ingreso",on_delete=models.PROTECT)
    retencion   = models.ForeignKey("configuracion.Retenciones", related_name="reteciones_ingreso",on_delete=models.PROTECT)
    base        = models.FloatField()
    fecha       = models.DateField('fecha', auto_now=False, auto_now_add=False)
    procentaje  = models.FloatField()
    total       = models.FloatField()

    class Meta:
        """Meta definition for RetencionIngreso."""

        verbose_name = 'RetencionIngreso'
        verbose_name_plural = 'RetencionIngresos'
        db_table = "retencioningreso"

    def __str__(self):
        """Unicode representation of RetencionIngreso."""
        return self.ingreso.numero
    
    def save(self, *args, **kwargs):
        self.fecha = datetime.strptime(str(self.ingreso.fecha),"%Y-%m-%d")

        super(RetencionIngreso, self).save(*args, **kwargs)
        
class CxPCompras(models.Model):
    """Model definition for CxPCompras."""

    # TODO: Define fields here
    # ==== Tipos de estado ==== 
    # False = Pendiente x Pago 
    # True = Pagada
    id                 = models.AutoField(primary_key=True)
    ingreso            = models.ForeignKey(Ingreso, related_name="cxpcompras_ingreso", on_delete=models.PROTECT,db_index=True)
    factura            = models.CharField("Factura:", max_length=50, blank=True, null=True,db_index=True)
    formaPago          = models.ForeignKey(FormaPago, related_name="cxpcompras_formaPago",on_delete=models.PROTECT, blank=True, null=True,db_index=True)
    fecha              = models.DateField("Fecha:", auto_now=False, auto_now_add=False, blank=True, null=True, db_index=True)
    fechaVencimiento   = models.DateField("Fecha de Vencimiento:", auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion        = models.CharField("Observación:", max_length=120, blank=True, null=True)
    proveedor          = models.ForeignKey("configuracion.Terceros", related_name="cxpcompras_proveedor",on_delete=models.PROTECT,db_index=True)
    estado             = models.BooleanField(default=False)
    notaCredito        = models.BooleanField(default=False)
    base               = models.FloatField(default=0)
    iva                = models.FloatField(default=0)
    valorAbono         = models.FloatField(default=0)
    reteFuente         = models.FloatField(default=0)
    reteIca            = models.FloatField(default=0)
    valorTotal         = models.FloatField(default=0)

    class Meta:
        """Meta definition for CxPCompras."""
        verbose_name = 'CxPCompras'
        verbose_name_plural = 'CxPComprass'
        db_table = 'cxpcompras'

    def __str__(self):
        """Unicode representation of CxPCompras."""
        return 'd'

    def save(self, *args, **kwargs):
        
        self.fecha     = datetime.strptime(str(self.ingreso.fecha),"%Y-%m-%d")
        self.factura   = self.ingreso.factura
        self.formaPago = self.ingreso.formaPago
        
        if self.formaPago.nombre == 'CONTADO':
            self.fechaVencimiento =  self.fecha
        elif self.formaPago.nombre == 'CRÉDITO 30 DIAS':
            self.fechaVencimiento =  self.fecha + timedelta(30)
        elif self.formaPago.nombre == 'CRÉDITO 45 DIAS':
            self.fechaVencimiento =  self.fecha + timedelta(45)
        elif self.formaPago.nombre == 'CRÉDITO 60 DIAS':
            self.fechaVencimiento =  self.fecha + timedelta(60)
        elif self.formaPago.nombre == 'CRÉDITO 75 DIAS':
            self.fechaVencimiento =  self.fecha + timedelta(75)
        elif self.formaPago.nombre == 'CRÉDITO 90 DIAS':
            self.fechaVencimiento =  self.fecha + timedelta(90)
        elif self.formaPago.nombre == 'CRÉDITO 120 DIAS':
            self.fechaVencimiento =  self.fecha + timedelta(120)
        else:
            self.fechaVencimiento =  self.fecha
        super(CxPCompras, self).save(*args, **kwargs) # Call the real save() method


class PagosCompras(models.Model):
    """Model definition for PagosCompras."""

    # TIPO TRANSACCIÓN
    SIN_FACTURA = 0
    CON_FACTURA = 1

    TIPO_TRANSACCION = (
        (SIN_FACTURA, "Pago sin relación"),
        (CON_FACTURA, "Pago con relación"),
    )

    # TODO: Define fields here
    id              = models.AutoField(primary_key=True)
    numeracion      = models.ForeignKey("configuracion.numeracion", related_name="pagos_numeracion" ,on_delete=models.PROTECT)
    numero          = models.CharField("Numero:", max_length=20, blank=True, null=True)
    consecutivo     = models.IntegerField(blank=True, null=True)
    prefijo         = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    tipoTransaccion = models.BooleanField('Tipo de transaccion:', choices = TIPO_TRANSACCION )
    usuario         = models.ForeignKey("users.User", related_name="pagos_usuario",on_delete=models.PROTECT)
    proveedor       = models.ForeignKey(Terceros, related_name="pagos_proveedor" ,on_delete=models.PROTECT)
    fecha           = models.DateField("Fecha:", auto_now=False, auto_now_add=False)
    cuenta          = models.ForeignKey('contabilidad.puc', on_delete=models.PROTECT)
    concepto        = models.TextField("Concepto:", blank=True, null=True)
    observacion     = models.TextField("Observacion:", blank=True, null=True)
    total           = models.FloatField(default = 0)
    # ValorAbono      = models.FloatField()
    # diferenciaBanco = models.FloatField(default=0)
    # totalSaldoFavor = models.FloatField(default=0)
    # descuento       = models.FloatField(default=0)
    # total           = models.FloatField()

    class Meta:
        """Meta definition for PagosCompras."""

        verbose_name = 'PagosCompra'
        verbose_name_plural = 'PagosCompras'
        db_table = 'pagoscompras'

    def __str__(self):
        """Unicode representation of PagosCompras."""
        return self.numero

    

    @classmethod
    def filter_ce(cls, obj):
  
        queryset = cls.objects.all().prefetch_related('proveedor','numeracion','cuenta')
        inicial = True

        if 'numero' in obj and obj['numero'] is not None:
            queryset = queryset.filter(numero=obj['numero'])
            inicial = False

        if 'consecutivo' in obj and obj['consecutivo'] is not None:
            queryset = queryset.filter(consecutivo=obj['consecutivo'])
            inicial = False

        if 'year' in obj and obj['year'] is not None:
            queryset = queryset.filter(fecha__year=obj['year'])
            inicial = False

        if 'mes' in obj and obj['mes'] is not None:
            queryset = queryset.filter(fecha__month=obj['mes'])
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

        if 'observacion' in obj and obj['observacion'] is not None:
            queryset = queryset.filter(observacion__icontains=obj['observacion'])
            inicial = False

        if 'total' in obj and obj['total'] is not None:
            queryset = queryset.filter(total=obj['total'])
            inicial = False

        if 'cuenta' in obj and obj['cuenta'] is not None:
            queryset = queryset.filter(cuenta__id=obj['cuenta'])
            inicial = False

        if 'factura' in obj and obj['factura'] is not None:
            queryset = queryset.filter(detalle_compra__factura__icontains=obj['factura'])
            inicial = False
        
        if 'orden' in obj and obj['orden'] is not None:
            queryset = queryset.filter(detalle_compra__orden__numero=obj['orden'])
            inicial = False


        if 'proveedor' in obj and obj['proveedor'] is not None:
            queryset = queryset.filter(proveedor__id=obj['proveedor'])
            inicial = False


        if 'concepto' in obj and obj['concepto'] is not None:
            queryset = queryset.filter(concepto__icontains=obj['concepto'])
            inicial = False

        if inicial:
            return queryset.order_by('-fecha','-id')[:20]

        return queryset.order_by('-fecha','-id')

        
    # def save(self, *args, **kwargs):
    #    self.consecutivo = self.numeracion.proximaFactura
    #    self.prefijo     = self.numeracion.prefijo
    #    self.numero      = self.numeracion.prefijo+'-'+str(self.numeracion.proximaFactura)
    #    super(PagosCompras, self).save(*args, **kwargs) # Call the real save() method
    

class DetailPayment(models.Model):
    """Model definition for DetailPayment."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    pago        = models.ForeignKey(PagosCompras, related_name="detallep_compra" ,on_delete=models.PROTECT)
    cuenta      = models.ForeignKey('contabilidad.puc', on_delete=models.PROTECT)
    valor       = models.FloatField()
    descuento   = models.FloatField(default=0)
    total       = models.FloatField()

    class Meta:
        """Meta definition for DetailPayment."""

        verbose_name = 'DetailPayment'
        verbose_name_plural = 'DetailPayments'
        db_table = 'detailpayment'
    def __str__(self):
        """Unicode representation of DetailPayment."""
        return self.ingreso.numero
        
   

class DetailPaymentInvoice(models.Model):
    """Model definition for PagoDetalle."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    ingreso     = models.ForeignKey(Ingreso, related_name="detalle_ingreso", on_delete=models.PROTECT)
    pago        = models.ForeignKey(PagosCompras, related_name="detalle_compra" ,on_delete=models.PROTECT)
    factura     = models.CharField("Factura:", max_length=50, db_index=True)
    orden       = models.ForeignKey(OrdenDeCompra, related_name="detailorden" ,on_delete=models.PROTECT)
    cxpCompra   = models.ForeignKey(CxPCompras, related_name="detailcxp" ,on_delete=models.PROTECT)
    descuento   = models.FloatField(default=0)
    saldoAFavor = models.FloatField(default=0)
    saldo       = models.FloatField(default=0)
    totalAbono  = models.FloatField()


    class Meta:
        """Meta definition for PagoDetalle."""

        verbose_name = 'DetailPaymentInVoice'
        verbose_name_plural = 'DetailPaymentInVoices'
        db_table = "detailpaymentinvoice"

    def __str__(self):
        """Unicode representation of PagoDetalle."""
        return self.ingreso.numero
    
    
 

class NotaDebito(models.Model):

    ADICION = '1'
    AUMENTO_PRECIO = '2'

    TIPO_DE_NOTA_CHOICES = (
        (ADICION, 'Adición de productos'),
        (AUMENTO_PRECIO, 'Aumento de precios'),
    )

    """Model definition for NotaDebito."""

    # TODO: Define fields here
    id              = models.AutoField(primary_key=True)
    tipoDeNota      = models.CharField("Tipo de nota:", max_length=50, choices=TIPO_DE_NOTA_CHOICES)
    numero          = models.CharField("Numero:", max_length=20, blank=True, null=True)
    consecutivo     = models.IntegerField(blank=True, null=True)
    prefijo         = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    numeracion      = models.ForeignKey("configuracion.numeracion", related_name="notaDebito_numeracion",on_delete=models.PROTECT)
    factura         = models.CharField("Factura:", max_length=50)
    ingreso         = models.ForeignKey(Ingreso, related_name="notaDebito_ingreso",on_delete=models.PROTECT)
    observacion     = models.TextField(default = "",blank=True, null=True)
    fecha           = models.DateField("Fecha:", auto_now=False, auto_now_add=False)
    valorTotal      = models.FloatField(default = 0)
    iva             = models.FloatField(default = 0)
    retencion       = models.FloatField(default = 0)
    proveedor       = models.ForeignKey("configuracion.Terceros", related_name="notaDebito_proveedor",on_delete=models.PROTECT)
    usuario         = models.ForeignKey("users.User", related_name="notaDebito_usuario",on_delete=models.PROTECT)

    class Meta:
        """Meta definition for NotaDebito."""

        verbose_name = 'NotaDebito'
        verbose_name_plural = 'NotaDebitos'
        db_table = 'notadebitocompras'

    def __str__(self):
        """Unicode representation of NotaDebito."""
        return self.numero
    
    def save(self, *args, **kwargs):
       self.consecutivo = self.numeracion.proximaFactura
       self.prefijo     = self.numeracion.prefijo
       self.numero      = self.numeracion.prefijo+'-'+str(self.numeracion.proximaFactura)
       super(NotaDebito, self).save(*args, **kwargs) # Call the real save() method

class NotaDebitoDetalle(models.Model):
    """Model definition for NotaDebitoDetalle."""

    # TODO: Define fields here

    id          = models.AutoField(primary_key=True)
    nota        = models.ForeignKey(NotaDebito, related_name="detalle_notaDebito",on_delete=models.PROTECT)
    producto    = models.ForeignKey(Productos, related_name="producto_notaDebito",on_delete=models.PROTECT)
    lote        = models.CharField("Lote:", max_length=50)
    cantidad    = models.IntegerField()
    valorUnidad = models.FloatField()
    iva         = models.FloatField(default = 0)
    subtotal    = models.FloatField()

    class Meta:
        """Meta definition for NotaDebitoDetalle."""

        verbose_name = 'NotaDebitoDetalle'
        verbose_name_plural = 'NotaDebitoDetalles'
        db_table = 'notadebitodetallecompras'

    def __str__(self):
        """Unicode representation of NotaDebitoDetalle."""
        return self.nota.numero


class NotaCredito(models.Model):

    DEVOLUCION = '1'
    REBAJA_PRECIO = '2'
    REBAJA_PARCIAL_TOTAL = '3'
    CORRECION = '4'

    TIPO_DE_NOTAS_CHOICES = (
        (DEVOLUCION, 'Devoluciones'),
        (REBAJA_PRECIO, 'Rebajas o disminución de precio'),
        (REBAJA_PARCIAL_TOTAL, 'Rebajas o descuento parcial o total'),
        (CORRECION, 'Correción a item'),
    )

    FACTURA = 'FACTURA'
    FECHA = 'FECHA'
    ITEM = 'ITEM'

    CORRECION_CHOICES = (
        (FACTURA, 'Correción factura'),
        (FECHA, 'Correción fecha'),
        (ITEM, 'Correción item'),
    )

    """Model definition for NotaCredito."""

    # TODO: Define fields here
    id              = models.AutoField(primary_key=True)  
    numeracion      = models.ForeignKey("configuracion.numeracion", related_name="NotaCredito_numeracion",on_delete=models.PROTECT)
    numero          = models.CharField("Numero:", max_length=20, blank=True, null=True)
    consecutivo     = models.IntegerField(blank=True, null=True)
    prefijo         = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    tipoNota        = models.CharField("Tipo de nota:", max_length=50, choices=TIPO_DE_NOTAS_CHOICES)
    tipoCorrecion   = models.CharField("Tipo de correccion:", max_length=50, choices=CORRECION_CHOICES , null=True, blank=True)
    ingreso         = models.ForeignKey(Ingreso, related_name="NotaCredito_ingreso",on_delete=models.PROTECT)
    fecha           = models.DateField('fecha:', auto_now=False, auto_now_add=False)
    anulada         = models.BooleanField(default=False)
    proveedor       = models.ForeignKey("configuracion.Terceros", related_name="NotaCredito_proveedor",on_delete=models.PROTECT)
    factura         = models.CharField("Factura:", max_length=50, null=True, blank=True)
    contabilizado   = models.BooleanField(default=False)
    observacion     = models.TextField(default = "", blank=True, null=True)
    numeroNota      = models.CharField("Numero de nota:", max_length=50, null=True, blank=True)
    subtotal        = models.FloatField(default=0)
    iva             = models.FloatField(default=0)
    retencion       = models.FloatField(default=0)
    total           = models.FloatField()
    usuario         = models.ForeignKey("users.User", related_name="notaCreditoC_usuario",on_delete=models.PROTECT)



    class Meta:
        """Meta definition for NotaCredito."""

        verbose_name = 'NotaCredito'
        verbose_name_plural = 'NotaCreditos'
        db_table = 'notacreditocompras'

    def __str__(self):
        """Unicode representation of NotaCredito."""
        return self.numero
    
    def save(self, *args, **kwargs):
       super(NotaCredito, self).save(*args, **kwargs) # Call the real save() method
    
class DetalleNotaCredito(models.Model):
    """Model definition for DetalleNotaCredito."""

    # TODO: Define fields here
    id          = models.AutoField(primary_key=True)
    nota        = models.ForeignKey(NotaCredito, related_name="detalle_NotaCredito" , on_delete=models.PROTECT)
    producto    = models.ForeignKey(Productos, related_name = "prdoucto_notaCreditoDetalle", on_delete=models.PROTECT)
    lote        = models.CharField("Lote:", max_length=50)
    cantidad    = models.IntegerField()
    valorUnidad = models.FloatField()
    iva         = models.FloatField(default=0)
    subtotal    = models.FloatField()


    class Meta:
        """Meta definition for DetalleNotaCredito."""

        verbose_name = 'DetalleNotaCredito'
        verbose_name_plural = 'DetalleNotaCreditos'
        db_table = 'notacreditodetalle'

    def __str__(self):
        """Unicode representation of DetalleNotaCredito."""
        return self.nota.numero





class AjusteStock(models.Model):
    """Model definition for AjusteStock."""
   
    
    # TODO: Define fields here
    id = models.AutoField(primary_key=True)
    numeracion  = models.ForeignKey("configuracion.numeracion", related_name="ajuste_numeracion",on_delete=models.PROTECT)
    numero      = models.CharField("Numero:", max_length=20, blank=True, null=True)
    prefijo     = models.CharField("Prefijo:", max_length=20,blank=True, null=True)
    consecutivo = models.IntegerField(blank=True, null=True)
    fecha       = models.DateField('fecha', auto_now=False, auto_now_add=True)
    
    usuario     = models.ForeignKey("users.User", on_delete=models.PROTECT,related_name="ajuste_usuario")
    observacion = models.TextField(default = '')

    class Meta:
        """Meta definition for AjusteStock."""

        verbose_name = 'Ajuste de inventario'
        verbose_name_plural = 'Ajustes de inventario'
        db_table = 'ajuste_stock'

    def __str__(self):
        """Unicode representation of AjusteStock."""
        return self.numero


class AjusteDetalle(models.Model):
    """Model definition for AjusteDetalle."""
    SOBRANTES                       = '1'
    BONIFICACION                    = '2'
    LOTE_TROCADO                    = '3'
    FV_ERRADA                       = '4'
    PERDIDA                         = '5'

    TIPO_CHOICES = (
        (SOBRANTES, 'SOBRANTES'),
        (BONIFICACION, 'BONIFICACIÓN'),
        (LOTE_TROCADO, 'LOTE TROCADO'),
        (FV_ERRADA, 'FV ERRADA'),
        (PERDIDA, 'PERDIDA'),
    )

    # TODO: Define fields here
    id               = models.AutoField(primary_key=True)
    ajuste           = models.ForeignKey(AjusteStock, related_name="detalle_ajuste",on_delete=models.PROTECT)
    tipoAjuste       = models.CharField('Tipo de ajuste:',choices=TIPO_CHOICES, max_length=2)
    producto         = models.ForeignKey(Productos, related_name = "prdoucto_ajuste_stock", on_delete=models.PROTECT)
    cantidad         = models.IntegerField(default=0)
    costo            = models.FloatField(default = 0)
    lote             = models.CharField('Lote', max_length=50)
    fechaVencimiento = models.DateField('Fecha de Vencimiento', auto_now=False, auto_now_add=False)
    existencia       = models.IntegerField(default=0)
    isEntrada        = models.BooleanField(default=False)
    isSalida         = models.BooleanField(default=False)
    total            = models.FloatField(default = 0)


    class Meta:
        """Meta definition for AjusteDetalle."""

        verbose_name = 'Ajuste Detalle'
        verbose_name_plural = 'Ajustes Detalles'
        db_table = 'ajuste_detalle_stock'


    def __str__(self):
        """Unicode representation of AjusteDetalle."""
        return self.ajuste.numero



# signals para el modelo pagosComprasDetalle
post_save.connect(update_factura_pago,sender=DetailPaymentInvoice)
post_delete.connect(delete_factura_pago,sender=DetailPaymentInvoice)
