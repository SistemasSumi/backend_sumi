from django.contrib import admin
from .models import *
@admin.register(CxcMovi)
class bodegaAdmin(admin.ModelAdmin):
    '''Admin View for cxc'''

    list_display = (
        'id',
        'numeracion',
        'consecutivo',
        'numero',
        'prefijo',
        'cliente',
        'valor',
        'fecha',
        'fechaVencimiento',
        'abono',
        'descuento',
        'valorDomicilio',
        'valorLetras',
        'observacion',
        'formaPago',
        'vendedor',
        'pagada',
        'usuario',
        'xmlEstado',
        'cufe',
        'qr',
        'statusFac',
        'valorIva',
        'valorReteFuente',
        'subtotal',
        'despachado',
        'correoEnviado',
    )
    list_filter = ('numeracion__tipoDocumento',)
    search_fields = (
        'numero',
        'cliente__nombreComercial',
    )
    ordering = ('id',)


admin.site.site_header = 'Administración de SarpSoft'
admin.site.site_title = 'Admin Notas de SarpSoft'
class DetalleNotaCreditoInline(admin.TabularInline):
    model = DetalleNotaCreditoVentas
    extra = 1

@admin.register(NotaCreditoVentas)
class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipoNota','cxc','isElectronica','enviadaDian', 'fecha', 'cliente', 'total')
    list_filter = ('tipoNota', 'fecha', 'cliente','isElectronica','enviadaDian')
    search_fields = ('numero', 'cxc__numero')
    inlines = [DetalleNotaCreditoInline]

@admin.register(DetalleNotaCreditoVentas)
class DetalleNotaCreditoAdmin(admin.ModelAdmin):
    list_display = ('nota', 'producto', 'lote', 'cantidad', 'valorUnidad', 'subtotal')
    list_filter = ('producto', 'lote')
    search_fields = ('nota__numero', 'producto__nombre')


@admin.register(CxcMoviDetalle)
class CxcMoviDetalleAdmin(admin.ModelAdmin):
    '''Admin View for Impuestos'''

    list_display = (
        'factura',
        'id',
        'producto',
        'valorCompra',
        'valor',
        'cantidad',
        'vence',
        'descuento',
        'lote',
     
        'subtotal',
        'descuento',
        'iva',
        'total',
    )
    list_filter = ('factura__numero',)
 
    search_fields = ('factura__numero',)
 
    ordering = ('id',)


@admin.register(ImpuestoCxc)
class ImpuestoCxcDetalleAdmin(admin.ModelAdmin):
    '''Admin View for Impuestos'''

    list_display = (
        'factura',
        'id',
        'impuesto',
        'base',
        'procentaje',
        'total',
       
    )
    list_filter = ('factura__numero',)
 
    search_fields = ('factura__numero',)
   
    ordering = ('id',)



@admin.register(RetencionCxc)
class RetencionCxcDetalleAdmin(admin.ModelAdmin):
    '''Admin View for Impuestos'''

    list_display = (
        'factura',
        'id',
        'retencion',
        'base',
        'procentaje',
        'total',
       
    )
    list_filter = ('factura__numero',)
 
    search_fields = ('factura__numero',)

    ordering = ('id',)

admin.site.register(PagosVentas)
admin.site.register(DetailPaymentInvoiceVentas)

@admin.register(CxcVentas)
class RetencionCxcDetalleAdmin(admin.ModelAdmin):
    '''Admin View for Impuestos'''

    list_display = (
        'id',   
        'cxc',  
        'factura',   
        'formaPago',   
        'fecha',   
        'fechaVencimiento',  
        'observacion',   
        'cliente',   
        'estado',   
        'notacredito',   
        'notadebito',   
        'base',   
        'iva',   
        'valorAbono',   
        'reteFuente',   
        'reteIca',   
        'valorTotal',   

       
    )
    list_filter = ('cxc__numero',)
 
    search_fields = ('cxc__numero',)

    ordering = ('id',)

class DetalleCotizacionInformalInline(admin.TabularInline):
    model = NuevaCotizacionDetalle
    extra = 1  # Puedes ajustar la cantidad de formularios en línea que se muestran

@admin.register(NuevaCotizacion)
class CotizacionInformalAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'fecha', 'valor', 'usuario')
    list_filter = ('fecha', 'usuario')
    search_fields = ('numero', 'cliente')
    date_hierarchy = 'fecha'
    inlines = [DetalleCotizacionInformalInline]