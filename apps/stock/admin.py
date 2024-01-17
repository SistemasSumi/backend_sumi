from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Bodega)
class bodegaAdmin(admin.ModelAdmin):
    '''Admin View for productos'''

    list_display = (
        'id',
        'nombre',
    )
    list_filter = ('nombre',)
    search_fields = (
        'id',
        'nombre',
    )
    ordering = ('id',)


@admin.register(tipoProducto)
class tipoProductoAdmin(admin.ModelAdmin):
    '''Admin View for productos'''

    list_display = (
        'id',
        'nombre',
        'c_tipo'
    )
    list_filter = ('nombre',)
    search_fields = (
        'id',
        'nombre',
        'c_tipo'
    )
    ordering = ('id',)


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    '''Admin View for productos'''

    list_display = (
        'id',
        'bodega',
        'idProducto',
        'vencimiento',
        'valorCompra',
        'unidades',
        'lote',
        'estado'
    )
    list_filter = ('vencimiento',)
    search_fields = (
    
        'idProducto__codigoDeBarra',
        'idProducto__nombreymarcaunico',
    
    )
    ordering = ('-id',)


@admin.register(Productos)
class productosAdmin(admin.ModelAdmin):
    '''Admin View for productos'''
    list_display = (
        'id',
        'nombre',
        'Filtro',
        'invima',
        'cum',
        'valorCompra',
        'valorVenta',
        'valorventa1',
        'valorventa2',
        'fv',
        'regulado',
        'valorRegulacion',
        'stock_inicial',
        'stock_min',
        'stock_max',
        'tipoProducto',
        'habilitado',
        'bodega',
        'impuesto',
        'codigoDeBarra',
        'unidad',
        'usuario',
        'creado',
        'modificado',
        'nombreymarcaunico',
    )
    list_filter = ('tipoProducto', 'bodega', 'Filtro')
    search_fields = (
        
        'codigoDeBarra',
      
    )
    ordering = ('id', )


@admin.register(Kardex)
class KardexAdmin(admin.ModelAdmin):
    '''Admin View for productos'''
    list_display = (
        'id',
        'descripcion',
        'tipo',
        'fecha',
        'producto',
        'tercero',
        'bodega',
        'unidades',
        'balance',
        'precio'
    )
    list_filter = ('producto', 'fecha')
    search_fields = (
        
        
        'producto__codigoDeBarra',
        
    )
    ordering = ('id',)


@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numeracion',
        'numero',
        'consecutivo',
        'prefijo',
        'proveedor',
        'fecha',
        'formaPago',
        'usuario',
        'observacion',
        'subtotal',
        'iva',
        'retencion',
        'descuento',
        'total',
        'ingresada',
    )
    list_filter = ('numeracion', )
    search_fields = (
        'id',
        'numeracion',
        'numero',
        'consecutivo',
        'prefijo',
        'proveedor',
        'fecha',
        'formaPago',
        'usuario',
        'observacion',
        'subtotal',
        'iva',
        'retencion',
        'descuento',
        'total',
    )
    ordering = ('-fecha',)


@admin.register(OrdenDetalle)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'orden',
        'producto',
        'cantidad',
        'valorUnidad',
        'descuento',
        'iva',
    )
    list_filter = ('producto',)
    search_fields = (
        'id',
        'orden',
        'producto',
        'cantidad',
        'valorUnidad',
        'descuento',
        'iva',
    )
    ordering = ('id',)


@admin.register(ImpuestoOrden)
class ImpuestoOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'orden',
        'impuesto',
        'base',
        'procentaje',
        'total',
    )
    list_filter = ('impuesto',)
    search_fields = (
        'id',
        'orden',
        'impuesto',
        'base',
        'procentaje',
        'total',
    )
    ordering = ('id',)


@admin.register(RetencionOrden)
class RetencionOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'orden',
        'retencion',
        'base',
        'porcentaje',
        'total',
    )
    list_filter = ('retencion',)
    search_fields = (
        'id',
        'orden',
        'retencion',
        'base',
        'porcentaje',
        'total',
    )
    ordering = ('id',)


@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    '''Admin View for Ingreso'''

    list_display = (
        'id',
        'numeracion',
        'numero',
        'consecutivo',
        'orden',
        'prefijo',
        'factura',
        'proveedor',
        'fecha',
        'formaPago',
        'usuario',
        'observacion',
        'subtotal',
        'iva',
        'retencion',
        'descuento',
        'total',
    )
    list_filter = ('proveedor__nombreComercial',)
    search_fields = (
        
        'numero',
        'orden__numero',
        'factura'
       
    )
    ordering = ('-id',)


@admin.register(IngresoDetalle)
class IngresoDetalleAdmin(admin.ModelAdmin):
    '''Admin View for IngresoDetalle'''

    list_display = (
        'id',
        'ingreso',
        'producto',
        'cantidad',
        'fechaVencimiento',
       
        'lote',
        'valorUnidad',
        'descuento',
        'iva',
    )
    list_filter = ('producto',)
    search_fields = (
        'codigoDeBarra',
    )
    ordering = ('id',)


@admin.register(ImpuestoIngreso)
class ImpuestoIngresoAdmin(admin.ModelAdmin):
    '''Admin View for ImpuestoIngreso'''

    list_display = (
        'id',
        'ingreso',
        'fecha',
        'impuesto',
        'base',
        'procentaje',
        'total',
    )
    list_filter = ('ingreso',)
    search_fields = (
        
        'ingreso__numero',
        
    )
    ordering = ('-id',)


@admin.register(RetencionIngreso)
class RetencionIngresoAdmin(admin.ModelAdmin):
    '''Admin View for RetencionIngreso'''

    list_display = (
        'id',
        'ingreso',
        'fecha',
        'retencion',

        'base',
        'procentaje',
        'total',
    )
    list_filter = ('ingreso',)
    search_fields = (
        
        'ingreso__numero',
        
    )
    ordering = ('-id',)


@admin.register(CxPCompras)
class CxPComprasAdmin(admin.ModelAdmin):
    '''Admin View for CxPCompras'''

    list_display = (
        'id',
        'ingreso',
        'factura',
        'formaPago',
        'fecha',
        'fechaVencimiento',
        'observacion',
        'proveedor',
        'estado',
        'base',
        'iva',
        'valorAbono',
        'reteFuente',
        'reteIca',
        'valorTotal',
    )
    list_filter = ('proveedor__nombreComercial',)
    search_fields = (
       
        'ingreso__orden__numero',
        'factura',
       
    )
    ordering = ('-id',)




class AjusteDetalleInline(admin.TabularInline):  # Opcionalmente puedes usar StackedInline en lugar de TabularInline
    model = AjusteDetalle
    extra = 1  # Número de formularios en blanco que se muestran para agregar detalles

class AjusteStockAdmin(admin.ModelAdmin):
    list_display = ('numero', 'consecutivo', 'observacion')
    inlines = [AjusteDetalleInline]
    search_fields = (
        'numero',
    )

admin.site.register(AjusteStock, AjusteStockAdmin)


@admin.register(PagosCompras)
class PagosComprasAdmin(admin.ModelAdmin):
    '''Admin View for PagosCompras'''

    list_display = (
        'id',
        'numeracion',
        'numero',
        'consecutivo',
        'prefijo',
        'tipoTransaccion',
        'usuario',
        'fecha',
        'concepto'
        
    )
    list_filter = ('numero',)
    search_fields = (
        'id',
        'numeracion',
        'numero',
        'consecutivo',
        'prefijo',
        'tipoTransaccion',
        'usuario',
        'fecha',
        'concepto',
        
    )
    ordering = ('id',)


admin.site.register(DetailPaymentInvoice)


@admin.register(NotaDebito)
class NotaDebitoAdmin(admin.ModelAdmin):
    '''Admin View for NotaDebito'''

    list_display = (
        'id',
        'tipoDeNota',
        'numero',
        'consecutivo',
        'prefijo',
        'numeracion',
        'factura',
        'ingreso',
        'observacion',
        'fecha',
        'valorTotal',
        'iva',
        'retencion',
        'proveedor',
        'usuario',
    )
    list_filter = ('numero',)
    search_fields = (
        'id',
        'tipoDeNota',
        'numero',
        'consecutivo',
        'prefijo',
        'numeracion',
        'factura',
        'ingreso',
        'observacion',
        'fecha',
        'valorTotal',
        'iva',
        'retencion',
        'proveedor',
        'usuario',
    )
    ordering = ('id',)


@admin.register(NotaDebitoDetalle)
class NotaDebitoDetalleAdmin(admin.ModelAdmin):
    '''Admin View for NotaDebitoDetalle'''

    list_display = (
        'id',
        'nota',
        'producto',
        'lote',
        'cantidad',
        'valorUnidad',
        'iva',
        'subtotal',
    )
    list_filter = ('producto',)
    search_fields = (
        'id',
        'nota',
        'producto',
        'lote',
        'cantidad',
        'valorUnidad',
        'iva',
        'subtotal',
    )
    ordering = ('id',)


@admin.register(NotaCredito)
class NotaCreditoAdmin(admin.ModelAdmin):
    '''Admin View for NotaCredito'''

    list_display = (
        'id',
        'numeracion',
        'prefijo',
        'consecutivo',
        'numero',
        'tipoNota',
        'tipoCorrecion',
        'ingreso',
        'proveedor',
        'factura',
        'contabilizado',
        'observacion',
        'numeroNota',
    )
    list_filter = ('tipoNota',)
    search_fields = (
        'id',
        'nuemracion',
        'prefijo',
        'consecutivo',
        'numero',
        'tipoNota',
        'tipoCorrecion',
        'ingreso',
        'proveedor',
        'factura',
        'contabilizado',
        'observacion',
        'numeroNota',
    )
    ordering = ('id',)


@admin.register(DetalleNotaCredito)
class DetalleNotaCreditoAdmin(admin.ModelAdmin):
    '''Admin View for DetalleNotaCredito'''

    list_display = (
        'id',
        'nota',
        'producto',
        'lote',
        'cantidad',
        'valorUnidad',
        'iva',
        'subtotal',
    )
    list_filter = ('producto',)
    search_fields = (
        'id',
        'nota',
        'producto',
        'lote',
        'cantidad',
        'valorUnidad',
        'iva',
        'subtotal',
    )
    ordering = ('id',)
