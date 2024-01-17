from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(asiento)
class AsientoAdmin(admin.ModelAdmin):
    '''Admin View of asiento'''
    list_display = (
        'id',
        'numero',
        'fecha',
        'mes',
        'anio',
        'empresa',
        'usuario',
        'totalDebito',
        'totalCredito'
    )
    list_filter = ('numero',)
    search_fields = (
        
        'numero',
        
    )
    ordering = ('id',)


@admin.register(asientoDetalle)
class AsientoDetalleAdmin(admin.ModelAdmin):
    '''Admin View of asientoDetalle'''
    list_display = (
        'id',
        'tipo',
        'asiento',
        'tercero',
        'cuenta',
        'debito',
        'credito',
        'fecha',
        'mes',
        'anio',
        'concepto'
    )
    list_filter = ('tipo','cuenta','fecha','asiento__numero')
    search_fields = (
        'asiento__numero',
        'concepto'
        
    )
    ordering = ('-id',)

admin.site.register(PagoCajaMenor)
admin.site.register(CajaMenor)
@admin.register(Traslado)
class TrasladoAdmin(admin.ModelAdmin):
    '''Admin View of Traslado'''
    list_display = (
        'id',
        'numeracion',
        'numero',
        'consecutivo',
        'fecha',
        'cuenta_origen',
        'cuenta_destino',
        'monto',
        'concepto',
        'usuario',
    )
    list_filter = ('numeracion', 'fecha', 'cuenta_origen', 'cuenta_destino')
    search_fields = (
        'numero',
        'consecutivo',
        'cuenta_origen__nombre',  # Suponiendo que el modelo cuenta_origen tiene un campo 'nombre'
        'cuenta_destino__nombre', # Suponiendo que el modelo cuenta_destino tiene un campo 'nombre'
    )
    ordering = ('-id',)


@admin.register(ComprobantesContable)
class ComprobantesContablesAdmin(admin.ModelAdmin):
    '''Admin View of ComprobantesContables'''
    list_display = (
        'id',
        'numeracion',
        'numero',
        'consecutivo',
      
        'usuario',
        'total',
      
        'fechaRegistro',
        'mes',
        'anio'
    )
    list_filter = ('anio','mes')
    search_fields = (
        'numero',
    )
    ordering = ('id',)


@admin.register(CombrobantesDetalleContable)
class CombrobantesDetalleContableAdmin(admin.ModelAdmin):
    '''Admin View of CombrobanteDetalleContable'''
    list_display = (
        'id',
        'comprobante',
        'tercero',
        'cuenta',
       
        'debito',
        'credito',
        'fechaMovi'
    )
    list_filter = ('tercero',)
    search_fields = (
        
        'comprobante',
        
    )
    ordering = ('id',)


@admin.register(puc)
class pucAdmin(admin.ModelAdmin):
    '''Admin View of puc'''
    list_display = (
        'id',
        'tipoDeCuenta',
        'naturaleza',
        'nombre',
        'codigo',
        'estadoFinanciero',
        'estadoResultado',
        'padre'
    )
    list_filter = ('tipoDeCuenta','codigo')
    search_fields = (
        'codigo',
       
       
    ),
    ordering = ('id', )

@admin.register(CuentaNecesaria)
class CuentaNecesariaAdmin(admin.ModelAdmin):
    '''Admin View for CuentaNecesaria'''

    list_display = (
        'id', 
        'cuenta', 
        'nombre', 
        'isCompra', 
        'isVenta' )
  
@admin.register(Conciliacion)
class ConciliacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'consecutivo', 'numero', 'cuenta', 'saldoAnterior', 'saldoFinal', 'mes', 'year', 'fechaCierre')
    search_fields = ('numero', 'mes', 'year', 'cuenta__codigo')
    list_filter = ('mes', 'year', 'cuenta')