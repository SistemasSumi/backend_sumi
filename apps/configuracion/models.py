from django.db import models
from apps.contabilidad.models import *
from .manager import ImpuestosEnGeneralManager,RetencionesEnGeneralManager

from datetime import date


# class FE_Encabezado(models.Model):
#     """Model definition for FE_Encambezado."""

#     # TODO: Define fields here

#     class Meta:
#         """Meta definition for FE_Encabezado."""

#         verbose_name = 'Encabezado Factura'
#         verbose_name_plural = 'Encabezado Factura'

#     def __str__(self):
#         """Unicode representation of FE_Encabezado."""
#         pass




class FormaPago(models.Model):
    """Model definition for Departamentos."""
    id     = models.AutoField(primary_key=True)
    nombre = models.CharField('forma', max_length=50)
    plazo  = models.IntegerField('Plazo en Dias',blank=True, null=True)
    

    # TODO: Define fields here

    class Meta:
        """Meta definition for formaPago."""

        verbose_name = 'Forma de pago'
        verbose_name_plural = 'Forma de pago'
        db_table = 'formasdepago'

    def __str__(self):
        """Unicode representation of formaPago."""
        return self.nombre

class Departamentos(models.Model):
    """Model definition for Departamentos."""
    id = models.AutoField(primary_key=True)
    codigo = models.CharField('codigo', max_length=100)
    departamento = models.CharField('departamento', max_length=100)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Departamentos."""

        verbose_name = 'Departamentos'
        verbose_name_plural = 'Departamentos'
        db_table = 'departamentos'

    def __str__(self):
        """Unicode representation of Departamentos."""
        return f"codigo: {self.codigo} nombre:{self.departamento}"


class Municipios(models.Model):
    """Model definition for Municipios."""
    id = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamentos, related_name="departamentos_municipios",on_delete=models.PROTECT)
    codigo = models.CharField('codigo', max_length=100)
    municipio = models.CharField('municipio', max_length=100)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Departamentos."""

        verbose_name = 'Municipios'
        verbose_name_plural = 'Municipios'
        db_table = 'municipios'

    def __str__(self):
        """Unicode representation of Departamentos."""
        return f"codigo: {self.codigo} nombre:{self.municipio}"

   

class Empresa(models.Model):
    """Model definition for Empresa."""
   # TIPOS DE PERSONAS
    PERSON_N = '1'
    PERSON_J = '2'

    TIPOSPERSONA_CHOICES = (
        (PERSON_N, 'Persona natural'),
        (PERSON_J, 'Persona judirica'),
    )

    # TODO: Define fields here
    id                 = models.AutoField(primary_key=True)
    logo               = models.CharField('Logo:', max_length=250,null=True,blank=True)
    slogan             = models.CharField('Slogan:', max_length=250,null=True)
    razon_social       = models.CharField('Razon Social', max_length=150, null=False, blank=False)
    correo             = models.EmailField('Correo:', max_length=254)
    departamento       = models.ForeignKey(Departamentos, on_delete=models.PROTECT)
    municipio          = models.ForeignKey(Municipios, on_delete=models.PROTECT)
    nit                = models.CharField('Nit:', max_length=100)
    dv                 = models.CharField('Digito de verificación:', max_length=5)
    actividadEconomica = models.CharField('Actividad economica:',max_length=50)
    nombreComercial    = models.CharField('Nombre comercial', max_length=100)
    tipoPersona        = models.CharField('Tipo de persona:',max_length=5,choices=TIPOSPERSONA_CHOICES)
    obligaciones       = models.CharField('Obligaciones', max_length=50, default="R-99-PN")
    telefono           = models.CharField('Tel::', max_length=100)
    registroMercantil  = models.CharField('registroMercantil', max_length=50)
    correoContacto     = models.EmailField()
    fecha_creacion     = models.DateTimeField('fecha Creacion:')
    fecha_modificacion = models.DateTimeField('fecha Modificacion:')
    estado             = models.BooleanField(default = True)



    class Meta:
        """Meta definition for Empresa."""

        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'empresa'

    def __str__(self):
        return self.razon_social




    
class numeracion(models.Model):
    """Model definition for numeracion."""
    FACTURA_ELECTRONICA        = '1'
    FACTURA_POS                = '2'
    NOTA_CREDITO               = '3'
    NOTA_DEBITO                = '4'
    COMPROBANTE_INGRESO        = '5'
    COMPROBANTE_EGRESO         = '6'
    COTIZACION                 = '7'
    ORDEN_COMPRA               = '8'
    PROFORMA                   = '9'
    DOCUMENTO_SOPORTE          = '10'
    NOTA_CREDITO_COMPRAS       = '11'
    NOTA_DEBITO_COMPRAS        = '12'
    AJUSTE_INVENTARIO          = '13'
    NOTA_AJUSTE_DOC_SOPORTE    = '14'
    TRASLADO_ENTRE_UBICACIONES = '15'
    RECEPCION_COMPRAS          = '16'
    COMPROBANTE_CONTABLE       = '17'
    INGRESO_ALMACEN            = '18'
    TRASLADO_FONDOS            = '19'
    NOMINA_GENERAL             = '20'
    NOMINA_INDIVIDUAL          = '21'
    NOTA_CREDITO_POS           = '22'
    CONCILIACION               = '23'

    TIPOSDOCUMENTOS_CHOICES = (
        (FACTURA_ELECTRONICA, 'FACTURA ELECTRÓNICA'),
        (FACTURA_POS, 'FACTURA POS'),
        (NOTA_CREDITO, 'NOTA CRÉDITO'),
        (NOTA_CREDITO_POS, 'NOTA CRÉDITO POS'),
        (NOTA_DEBITO, 'NOTA DÉBITO'),
        (COMPROBANTE_INGRESO, 'COMPROBANTE DE INGRESO'),
        (COMPROBANTE_EGRESO, 'COMPROBANTE DE EGRESO'),
        (COTIZACION, 'COTIZACIÓN'),
        (ORDEN_COMPRA, 'ORDEN DE COMPRA'),
        (PROFORMA, 'PROFORMA'),
        (DOCUMENTO_SOPORTE, 'DOCUMENTOS SOPORTE'),
        (NOTA_CREDITO_COMPRAS, 'NOTA CRÉDITO COMPRAS'),
        (NOTA_DEBITO_COMPRAS, 'NOTA DÉBITO COMPRAS'),
        (AJUSTE_INVENTARIO, 'AJUSTE DE INVENTARIO'),
        (NOTA_AJUSTE_DOC_SOPORTE, 'NOTA DE AJUSTE DOC. SOPORTE'),
        (TRASLADO_ENTRE_UBICACIONES, 'TRASLADO ENTRE UBICACIONES'),
        (RECEPCION_COMPRAS, 'RECEPCIÓN DE COMPRAS'),
        (COMPROBANTE_CONTABLE, 'COMPROBANTE CONTABLE'),
        (INGRESO_ALMACEN, 'INGRESO AL ALMACEN'),
        (TRASLADO_FONDOS, 'TRASLADOS DE FONDOS'),
        (NOMINA_GENERAL, 'NOMINA GENERAL'),
        (NOMINA_INDIVIDUAL, 'NOMINA ELECTRONICA INDIVIDUAL'),
        (CONCILIACION, 'CONCILIACIÓN'),
    )

    # TODO: Define fields here

    id                = models.AutoField(primary_key=True)
    tipoDocumento     = models.CharField('Tipo de documento:',max_length=5,choices=TIPOSDOCUMENTOS_CHOICES)
    nombre            = models.CharField('nombre:', max_length=100, blank=False, null=False)
    prefijo           = models.CharField('prefijo:', max_length=50)
    proximaFactura    = models.IntegerField('Próxima Factura:')
    desde             = models.IntegerField('Desde el número:')
    hasta             = models.IntegerField('Hasta el número:')
    resolucion        = models.CharField('N° Resolución:', max_length=500)
    producccion       = models.BooleanField(default = False)
    textoResolucion   = models.CharField('Texto Resolución:', max_length=5000)
    empresa           = models.ForeignKey(Empresa, related_name='numeracion_empresa', on_delete=models.PROTECT)
    fecha_inicio      = models.DateField('fecha Inicio:', auto_now=False, auto_now_add=False,blank=True, null=True)
    fecha_vencimiento = models.DateField('fecha vencimiento:', auto_now=False, auto_now_add=False,blank=True, null=True)
    estado            = models.BooleanField('estado:',default = True)



    class Meta:
        """Meta definition for numeracion."""

        verbose_name = 'numeracion'
        verbose_name_plural = 'numeraciones'
        db_table = 'numeraciones'

    def __str__(self):
        return self.tipoDocumento



class TimeLine(models.Model):
    """Model definition for TimeLine."""

    # TODO: Define fields here
    fecha_creacion     = models.DateTimeField('fecha Creacion:')
    fecha_modificacion = models.DateTimeField('fecha Creacion:')
    estado             = models.BooleanField(default = True)

    class Meta:
        """Meta definition for TimeLine."""
        abstract = True
        

class VendedoresClientes(models.Model):
    """Model definition for Vendedor."""
    id         = models.AutoField(primary_key = True)
    nombre     = models.CharField('nombre:', max_length=80)
    usuario    = models.ForeignKey(to="users.User", related_name="usuario_vendedor",on_delete=models.PROTECT)
    meta       = models.FloatField(default= 0,blank=True, null=True)

    
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for Vendedor."""

        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        db_table = 'vendedores_clientes'

    def __str__(self):
        return self.nombre



class ListaDePrecios(models.Model):
    TIPO_LOCAL         = 'LOCAL'
    TIPO_REGIONAL      = 'REGIONAL'
    TIPO_NACIONAL      = 'NACIONAL'
    TIPO_INTERNACIONAL = 'INTERNACIONAL'

    TIPOS_CHOICES = (
        (TIPO_LOCAL, 'LOCAL'),
        (TIPO_REGIONAL, 'REGIONAL'),
        (TIPO_NACIONAL, 'NACIONAL'),
        (TIPO_INTERNACIONAL, 'INTERNACIONAL'),
    )

    """Model definition for Impuestos."""
    id           = models.AutoField(primary_key = True)
    tipo  = models.CharField('Tipo',max_length=50,choices=TIPOS_CHOICES)
    precio1   = models.FloatField('precio 1')
    precio2   = models.FloatField('precio 2')
    precio3   = models.FloatField('precio 3')
    precioMinimo = models.FloatField('Precio minimo')
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for Impuestos."""

        verbose_name = 'Lista de precio'
        verbose_name_plural = 'Listas de Precios'
        db_table = 'listaDePrecios'

    def __str__(self):
       return self.tipo


class Terceros(models.Model):
    PERSON_J = '1'
    PERSON_N = '2'

    TIPOSPERSONA_CHOICES = (
        (PERSON_N, 'Persona natural'),
        (PERSON_J, 'Persona judirica'),
    )
    id                          = models.AutoField(primary_key=True)
    tipoDocumento               = models.CharField('tipoDocumento', max_length=70)
    documento                   = models.CharField('Documento', max_length=50, unique=True)
    dv                          = models.CharField('Digito Verificacion', max_length=5, null=True,blank=True)
    nombreComercial             = models.CharField('nombreComercial', max_length=120)
    nombreContacto              = models.CharField('nombreContacto', max_length=120, blank=True, null=True)
    direccion                   = models.CharField('Direccion', max_length=250)
    departamento                = models.ForeignKey(Departamentos, on_delete=models.PROTECT)
    municipio                   = models.ForeignKey(Municipios, on_delete=models.PROTECT)
    telefonoContacto            = models.CharField('Tel:', max_length=50,blank=True, null=True)
    correoContacto              = models.EmailField('Correo Contacto', max_length=254, blank=True, null=True)
    correoFacturas              = models.EmailField('Correo Facturas', max_length=254,blank=True, null=True)
    # correoContabilidad          = models.EmailField('Correo Contabilidad', max_length=254,blank=True, null=True)
    vendedor                    = models.ForeignKey(VendedoresClientes,related_name="vendedor_tercero",on_delete=models.PROTECT,blank=True, null=True)  
    formaPago                   = models.ForeignKey(FormaPago,related_name="tercero_formaPago", on_delete=models.PROTECT)  
    tipoPersona                 = models.CharField('Tipo Persona',max_length=5,choices=TIPOSPERSONA_CHOICES)
    regimen                     = models.CharField('Regimen:',max_length=50,blank=True, null=True)
    obligaciones                = models.CharField('Obligaciones', max_length=50, default="R-99-PN")
    matriculaMercantil          = models.CharField('matriculaMercantil', max_length=50,blank=True, null=True)
    codigoPostal                = models.CharField('codigoPostal', max_length=50, blank=True, null=True)
    saldoAFavorProveedor        = models.FloatField(default = 0,blank=True, null=True)
    saldoAFavorCliente          = models.FloatField(default = 0,blank=True, null=True)
    isRetencion                 = models.BooleanField(default=False,blank=True, null=True)
    isCliente                   = models.BooleanField(default=False,blank=True, null=True)
    isProveedor                 = models.BooleanField(default=False,blank=True, null=True)
    isContabilidad              = models.BooleanField(default=False,blank=True, null=True)
    isCompras                   = models.BooleanField(default=False,blank=True, null=True)
    isPos                       = models.BooleanField(default=False,blank=True, null=True)
    isElectronico               = models.BooleanField(default=False,blank=True, null=True)
    cuenta_x_cobrar             = models.ForeignKey(to="contabilidad.puc", related_name="cuenta_cobrar_tercero", on_delete=models.PROTECT,blank=True, null=True)
    cuenta_x_pagar              = models.ForeignKey(to="contabilidad.puc", related_name="cuenta_pagar_tercero", on_delete=models.PROTECT,blank=True, null=True)
    cuenta_saldo_a_cliente      = models.ForeignKey(to="contabilidad.puc",related_name="cuenta_saldo_cliente", on_delete=models.PROTECT,blank=True, null=True)
    cuenta_saldo_a_proveedor    = models.ForeignKey(to="contabilidad.puc",related_name="cuenta_saldo_proveedor", on_delete=models.PROTECT,blank=True, null=True)
    montoCreditoProveedor       = models.FloatField(default = 0,blank=True, null=True)
    montoCreditoClientes        = models.FloatField(default = 0,blank=True, null=True)
    fecha_creacion              = models.DateField('fecha Creacion:',blank=True, null=True)
    fecha_modificacion          = models.DateField('fecha Modificacion:',blank=True, null=True)
    listaPrecios                = models.ForeignKey(ListaDePrecios, on_delete=models.PROTECT,blank=True, null=True)
    estado                      = models.BooleanField(default = True)


    class Meta:
        """Meta definition for Tercero."""

        verbose_name = 'Tercero'
        verbose_name_plural = 'Terceros'
        db_table = 'terceros'

    def __str__(self):
        """Unicode representation of Tercero."""
        return self.nombreComercial


    def save(self, *args, **kwargs):

        if self.fecha_creacion:
            self.fecha_modificacion = date.today()
        else:
            self.fecha_creacion     = date.today()
            self.fecha_modificacion = date.today()
                    
        super(Terceros, self).save(*args, **kwargs)


class PlazosDecuentosProveedores(models.Model):
    """Model definition for PlazosDecuentos."""
    
    # TODO: Define fields here
    id             = models.AutoField(primary_key=True)
    tercero        = models.ForeignKey(Terceros, related_name="plazos_proveedores",on_delete=models.PROTECT)
    quince         = models.FloatField(default = 0)
    treinta        = models.FloatField(default = 0)
    cuarenta       = models.FloatField(default = 0)
    cuarentaYcinco = models.FloatField(default = 0)
    sesenta        = models.FloatField(default = 0)
    noventa        = models.FloatField(default = 0)
    


    class Meta:
        """Meta definition for PlazosDecuentos."""

        verbose_name = 'PlazosProveedor'
        verbose_name_plural = 'PlazosProveedores'
        db_table = 'plazo_proveedor'

    def __str__(self):
        """Unicode representation of PlazosDecuentos."""
        return self.tercero.nombreComercial

class PlazosDecuentosClientes(models.Model):
    """Model definition for PlazosDecuentos."""
    
    # TODO: Define fields here
    id             = models.AutoField(primary_key=True)
    tercero        = models.ForeignKey(Terceros, related_name="plazos_clientes",on_delete=models.PROTECT)
    quince         = models.FloatField(default = 0)
    treinta        = models.FloatField(default = 0)
    cuarentaYcinco = models.FloatField(default = 0)
    sesenta        = models.FloatField(default = 0)
    noventa        = models.FloatField(default = 0)
    


    class Meta:
        """Meta definition for PlazosDecuentos."""

        verbose_name = 'PlazosCliente'
        verbose_name_plural = 'PlazosClientes'
        db_table = 'plazo_clientes'

    def __str__(self):
        """Unicode representation of PlazosDecuentos."""
        return self.tercero.nombreComercial


class DatosContacto(models.Model):
    """Model definition for DatosContacto."""
    CONTA   = 'CONTABILIDAD'
    FACTURA = 'FACTURACION'
    COMPRAS = 'COMPRAS'

    DATOS_CHOICES = (
        (CONTA, 'CONTABILIDAD'),
        (FACTURA, 'FACTURACIÓN'),
        (COMPRAS, 'COMPRAS'),
    )    



    # TODO: Define fields here
    id             = models.AutoField(primary_key=True)
    tercero        = models.ForeignKey(Terceros, related_name="datos_contacto",on_delete=models.PROTECT)
    tipo           = models.CharField('Tipo de contacto:', choices=DATOS_CHOICES, max_length=50)
    nombre         = models.CharField('Nombre:', max_length=50)
    telefono       = models.CharField('Nombre:', max_length=50)
    correo         = models.CharField('correo:', max_length=50)


    class Meta:
        """Meta definition for DatosContacto."""

        verbose_name = 'Datos de contacto'
        verbose_name_plural = 'Datos de contactos'
        db_table = 'datos_contacto'

    def __str__(self):
        """Unicode representation of datos_contacto."""
        return self.tercero.nombreComercial

class DatosBancarios(models.Model):
    """Model definition for DatosBancarios."""
    CORRIENTE   = 'CORRIENTE'
    AHORROS     = 'AHORROS'

    TIPO_CHOICES = (
        (CORRIENTE, 'CORRIENTE'),
        (AHORROS, 'AHORROS'),
    )    



    # TODO: Define fields here
    id             = models.AutoField(primary_key=True)
    tercero        = models.ForeignKey(Terceros, related_name="datos_bancarios",on_delete=models.PROTECT)
    tipo           = models.CharField('Tipo:', choices=TIPO_CHOICES, max_length=50)
    banco          = models.CharField('Banco:', max_length=50)
    cuenta         = models.CharField('cuenta:', max_length=50)


    class Meta:
        """Meta definition for DatosContacto."""

        verbose_name = 'Dato bancario'
        verbose_name_plural = 'Datos  bancarios'
        db_table = 'DatosBancarios'

    def __str__(self):
        """Unicode representation of DatosBancarios."""
        return self.tercero.nombreComercial


class Impuestos(models.Model):
    """Model definition for Impuestos."""
    id         = models.AutoField(primary_key = True)
    nombre     = models.CharField('Nombre:', max_length=70)
    porcentaje = models.FloatField()
    base       = models.FloatField(default = 0)
    compras    = models.ForeignKey(to='contabilidad.puc',related_name='impuesto_compras', on_delete=models.PROTECT)
    ventas     = models.ForeignKey(to='contabilidad.puc',  related_name='impuesto_ventas',on_delete=models.PROTECT)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Impuestos."""

        verbose_name = 'Impuestos'
        verbose_name_plural = 'Impuestos'
        db_table = 'impuestos'

    def __str__(self):
        return self.nombre

class Retenciones(models.Model):
    RETEFUENTE = '06'
    ICA = '07'


    """Model definition for Impuestos."""
    TIPORETENCION_CHOICES = (
        (RETEFUENTE, 'Retención en la fuente'),
        (ICA, 'Impuesto de Industria y Comercio (ICA)'),
    )

    id            = models.AutoField(primary_key = True)
    tipoRetencion = models.CharField('Tipo de retención',max_length=5,choices=TIPORETENCION_CHOICES)
    nombre        = models.CharField('Nombre:', max_length=70)
    porcentaje    = models.FloatField()
    base          = models.FloatField(default = 0)
    compras       = models.ForeignKey(to='contabilidad.puc', related_name='retencion_compras', on_delete=models.PROTECT)
    ventas        = models.ForeignKey(to='contabilidad.puc', related_name='retencion_ventas', on_delete=models.PROTECT)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Impuestos."""

        verbose_name = 'Retenciones'
        verbose_name_plural = 'Retenciones'
        db_table = 'retenciones'

    def __str__(self):
       return self.nombre

class RetencionesProveedor(models.Model):
    """Model definition for RetencionesProveedor."""
    id         = models.AutoField(primary_key = True)
    tercero    = models.ForeignKey(Terceros, related_name="retencion_proveedor",on_delete=models.PROTECT)
    retencion  = models.ForeignKey(Retenciones, related_name="proveedor_retenciones",on_delete=models.PROTECT)
    fija       = models.BooleanField(default= False,blank=True, null=True)

    
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for RetencionesProveedor."""

        verbose_name = 'Retenciones proveedor'
        verbose_name_plural = 'Retenciones proveedores'
        db_table = 'retenciones_proveedor'

    def __str__(self):
        return self.retencion.nombre

class RetencionesClientes(models.Model):
    """Model definition for RetencionesClientes."""
    id         = models.AutoField(primary_key = True)
    tercero    = models.ForeignKey(Terceros, related_name="retencion_cliente",on_delete=models.PROTECT)
    retencion  = models.ForeignKey(Retenciones, related_name="cliente_retenciones",on_delete=models.PROTECT)
    fija       = models.BooleanField(default= False,blank=True, null=True)

    
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for RetencionesClientes."""

        verbose_name = 'Retenciones cliente'
        verbose_name_plural = 'Retenciones clientes'
        db_table = 'retenciones_clientes'

    def __str__(self):
        return self.retencion.nombre

    


class RetencionesEnGeneral(models.Model):
    """Model definition for RetencionIngreso."""


    MOVIMIENTO = 'MC'
    NOTA       = 'NTC'
    COMPRAS    = 'COM'
    VENTAS     = 'FAC'
    DEVOLUCION = 'DEV'

    TIPO_CHOICES = (
        (MOVIMIENTO, 'Movimiento Contable'),
        (NOTA, 'Nota Contable'),
        (COMPRAS, 'Compras'),
        (VENTAS, 'Ventas'),
        (DEVOLUCION, 'Devolución'),
    )


    # TODO: Define fields here
    id              = models.AutoField(primary_key=True)
    tipo            = models.CharField('Tipo:', choices=TIPO_CHOICES, max_length=50)
    docReferencia   = models.CharField('Documento referencia:', max_length=1000)
    retencion       = models.ForeignKey("configuracion.Retenciones", related_name="reteciones_generales",on_delete=models.PROTECT)
    base            = models.FloatField()
    tercero         = models.ForeignKey(Terceros, related_name="retencion_general_tercero",on_delete=models.PROTECT)
    porcentaje      = models.FloatField('porcentaje')
    fecha           = models.DateField('Fecha:', auto_now=False, auto_now_add=False)
    ventas          = models.BooleanField(default=False)
    compras         = models.BooleanField(default=False)
    total           = models.FloatField(default = 0)


    objects = RetencionesEnGeneralManager()

    class Meta:
        """Meta definition for RetencionIngreso."""

        verbose_name = 'Retencion en general'
        verbose_name_plural = 'Retenciones en general'
    

    def __str__(self):

        return self.docReferencia


class ImpuestosEnGeneral(models.Model):
    """Model definition for impuetos."""


    MOVIMIENTO = 'MC'
    NOTA       = 'NTC'
    COMPRAS    = 'COM'
    VENTAS     = 'FAC'
    DEVOLUCION = 'DEV'


    TIPO_CHOICES = (
        (MOVIMIENTO, 'Movimiento Contable'),
        (NOTA, 'Nota Contable'),
        (COMPRAS, 'Compras'),
        (VENTAS, 'Ventas'),
        (DEVOLUCION, 'Devolución'),
    )


    # TODO: Define fields here
    id              = models.AutoField(primary_key=True)
    tipo            = models.CharField('Tipo:', choices=TIPO_CHOICES, max_length=50)
    docReferencia   = models.CharField('Documento referencia:', max_length=1000)
    Impuesto        = models.ForeignKey("configuracion.Impuestos", related_name="reteciones_generales",on_delete=models.PROTECT)
    tercero         = models.ForeignKey(Terceros, related_name="impuesto_general_tercero",on_delete=models.PROTECT)
    base            = models.FloatField()
    porcentaje      = models.FloatField('porcentaje')
    fecha           = models.DateField('Fecha:', auto_now=False, auto_now_add=False)
    ventas          = models.BooleanField(default=False)
    compras         = models.BooleanField(default=False)
    total           = models.FloatField()


    objects = ImpuestosEnGeneralManager()
    class Meta:
        """Meta definition for Impuestos en general."""

        verbose_name = 'Impuestos en general'
        verbose_name_plural = 'Impuestos en general'
    

    def __str__(self):

        return self.docReferencia


class Notificacion(models.Model):

    # tipos de notificación
    NORMAL = 'NORMAL'
    PRECIOS_BAJOS = 'PRECIOS BAJOS'
    DESPACHOS = 'DESPACHOS'
    FACTURA = 'FACTURA'
    INGRESO = 'INGRESO'



    tipos_choices  =[
        ('NORMAL', NORMAL),
        ('PRECIOS_BAJOS', PRECIOS_BAJOS),
        ('DESPACHOS', DESPACHOS),
        ('FACTURA', FACTURA),
        ('INGRESO', INGRESO)
    ]

    # grupo 

    CONTABILIDAD = 'CONTABILIDAD'
    FACTURACION = 'FACTURACION'
    LOGISTICA = 'LOGISTICA'

    grupos_choices = [
        ('CONTABILIDAD', CONTABILIDAD),
        ('FACTURACIÓN', FACTURACION),
        ('LOGÍSTICA', LOGISTICA),
    ]

    id = models.AutoField( primary_key=True)
    usuario = models.ForeignKey(to="users.User", related_name="noti_user", on_delete=models.PROTECT)
    mensaje = models.TextField()
    grupo = models.CharField(max_length=255, choices=grupos_choices, blank=True, null=True)
    data = models.JSONField(null=True, blank=True)
    sender_user = models.ForeignKey(to="users.User", related_name="sender" ,on_delete=models.PROTECT)
    receiver_users = models.ManyToManyField(to="users.User", related_name="receiver_user",blank=True, null=True)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    tipo = models.CharField(max_length=255, choices=tipos_choices)
    vistas = models.ManyToManyField(to="users.User", related_name="user_view",blank=True, null=True)


    class Meta:
        """Meta definition for Notificaciones."""

        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'
        db_table = 'notificaciones'
    

    def __str__(self):

        return self.tipo


   

        

