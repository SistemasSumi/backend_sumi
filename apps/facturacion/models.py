from django.db import models
from apps.users.models import User


# class TimeLine(models.Model):
#     """Model definition for TimeLine."""

#     # TODO: Define fields here
#     fecha_creacion     = models.DateTimeField('fecha Creacion:', auto_now=True)
#     fecha_modificacion = models.DateTimeField('fecha Creacion:', auto_now_add=True)
#     usuario            = models.ForeignKey(User, on_delete=models.PROTECT)
#     empresa            = models.ForeignKey("configuracion.Empresa", on_delete=models.PROTECT)
#     estado             = models.BooleanField(default = True)

#     class Meta:
#         """Meta definition for TimeLine."""
#         abstract = True
        


# class CxcMovi(TimeLine,models.Model):
#     """Model definition for CxcMovi."""

#     TIPOSPERSONA_CHOICES = (
#         (1, 'Electronica'),
#         (2, 'POS'),
#     )


#     # TODO: Define fields here
#     id               = models.AutoField(primary_key = True)
#     tercero          = models.ForeignKey("configuracion.Terceros",models.PROTECT)
#     valor            = models.FloatField()
#     fecha            = models.DateField('Fecha de vencimiento', auto_now=True, auto_now_add=False)
#     fechaVencimiento = models.DateField('Fecha de vencimiento', auto_now=False, auto_now_add=False)
#     abono            = models.FloatField()
#     descuento        = models.FloatField()
#     valorLetras      = models.CharField('Valor en letras', max_length=250)
#     observacion      = models.CharField('Observacion', max_length=250)
#     formaPago        = models.CharField('Forma de pago', max_length=250)
#     usuario          = models.ForeignKey("users.User",models.PROTECT)
#     xmlEstado        = models.BooleanField(default = False)
#     cufe             = models.CharField('cufe', max_length=350, blank=True, null=True)
#     qr               = models.CharField('qr', max_length=350, blank=True, null=True)
#     statusFac        = models.CharField('qr', max_length=350, blank=True, null=True)
#     valorReteFuente  = models.FloatField()
#     valorReteIca     = models.FloatField()
#     valorReteCree    = models.FloatField()
#     tipoFactura      = models.IntegerField(choices=TIPOSPERSONA_CHOICES)
#     correoEnviado    = models.BooleanField(default = False)

#     class Meta:
#         """Meta definition for CxcMovi."""

#         verbose_name = 'CxcMovi'
#         verbose_name_plural = 'CxcMovi'

#     def __str__(self): 
#         return f'{self.id}, {self.fechaCreacion}'

# class CxcMoviDetalle(models.Model):
#     """Model definition for CxcMoviDetalle."""

#     # TODO: Define fields here
#     id        = models.AutoField(primary_key = True)
#     factura   = models.ForeignKey(CxcMovi, on_delete=models.PROTECT)
#     producto  = models.ForeignKey("inventario.Productos", on_delete=models.PROTECT)
#     valor     = models.FloatField()
#     cantidad  = models.IntegerField()
#     descuento = models.FloatField()
#     lote      = models.CharField('lote', max_length=50)
#     iva       = models.FloatField()


#     class Meta:
#         """Meta definition for CxcMoviDetalle."""

#         verbose_name = 'CxcMoviDetalle'
#         verbose_name_plural = 'CxcMoviDetalles'

#     def __str__(self): 
#         return f'{self.id}, {self.producto.nombre}'




# class DetalleCotizacionFarmac(models.Model):
#     id           = models.AutoField(primary_key = True)
#     codigo       = models.CharField('codigo', max_length = 50 )
#     producto    = models.CharField('codigo', max_length = 250 )
#     id_producto  = models.ForeignKey(Productos, on_delete = models.PROTECT,null = True, blank = True)
#     precio       = models.DecimalField('Precio:',null=True,blank=True,max_digits=15,decimal_places=2)
#     iva          = models.DecimalField('iva:',null=True,blank=True,max_digits=15,decimal_places=2)
#     total        = models.DecimalField('Total:',null=True,blank=True,max_digits=15,decimal_places=2)
#     descuento    = models.DecimalField('descuento:',null=False,blank=False,max_digits=11,decimal_places=2)
#     cantidad     = models.IntegerField('Cantidad:',null=False, blank=False)


#     class Meta:
#         verbose_name        = "detalle_cotizacion"
#         verbose_name_plural = "detalle_cotizaciones"
#         db_table            = "detalle_cotizacion"
    
#     def __str__(self): 
#         return f'{self.idProducto}, {self.cantidad}'