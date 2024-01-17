from django.contrib import admin

from .models import *
# Register your models here.



@admin.register(Departamentos)
class DepartamentoAdmin(admin.ModelAdmin):
    '''Admin View of Departamento'''

    list_display = (
        'id',
        'codigo',
        'departamento',
    )
    list_filter = ('departamento',)
    search_fields = (
        'id',
        'codigo',
        'departamento',
    )
    ordering = ('id',)

@admin.register(ListaDePrecios)
class PreciosAdmin(admin.ModelAdmin):
    '''Admin View of Departamento'''

    list_display = (
        'id',
        'tipo',
        'precio1',
        'precio2',
        'precio3',
        'precioMinimo',
    )
    list_filter = ('tipo',)
    search_fields = ('tipo',)
    ordering = ('id',)



admin.site.register(Notificacion)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    '''Admin View for Empresa'''

    list_display = (
        'id',
        'logo',
        'slogan',
        'razon_social',
        'correo',
        'departamento',
        'municipio',
        'nit',
        'dv',
        'actividadEconomica',
        'nombreComercial',
        'tipoPersona',
        'obligaciones',
        'telefono',
        'registroMercantil',
        'correoContacto',
        'fecha_creacion',
        'fecha_modificacion',
        'estado',
    )
    list_filter = ('razon_social',)
    search_fields = (
        'id',
        'logo',
        'slogan',
        'razon_social',
        'correo',
        'departamento',
        'municipio',
        'nit',
        'dv',
        'actividadEconomica',
        'nombreComercial',
        'tipoPersona',
        'obligaciones',
        'telefono',
        'registroMercantil',
        'correoContacto',
        'fecha_creacion',
        'fecha_modificacion',
        'estado',
    )
    ordering = ('id',)

@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    '''Admin View of FormaPago'''

    list_display = (
        'id',
        'nombre',
        'plazo',
    )
    list_filter = ('nombre',)
    search_fields = (
        'id',
        'nombre',
        'plazo'
    )
    ordering = ('id',)


@admin.register(Impuestos)
class ImpuestosAdmin(admin.ModelAdmin):
    '''Admin View of Impuestos'''

    list_display = (
        'id',
        'nombre',
        'porcentaje',
        'base',
        'compras',
        'ventas'
    )
    list_filter = ('nombre',)
    search_fields = (
        'id',
        'nombre',
        'porcentaje',
        'base',
        'compras',
        'ventas'
    )
    ordering = ('id',)


@admin.register(Municipios)
class MunicipiosAdmin(admin.ModelAdmin):
    '''Admin View of Municipios'''

    list_display = (
        'id',
        'departamento',
        'codigo',
        'municipio'
    )
    list_filter = ('municipio',)
    search_fields = (
      
        'municipio',
    )
    ordering = ('id',)


@admin.register(numeracion)
class NumeracionAdmin(admin.ModelAdmin):
    '''Admin View of numeracion'''

    list_display = (
        'id',
        'tipoDocumento',
        'nombre',
        'prefijo',
        'proximaFactura',
        'desde',
        'hasta',
        'resolucion',
        'empresa',
        'fecha_vencimiento',
        'estado',
    )
    list_filter = ('tipoDocumento',)
    search_fields = (
        'id',
        'tipoDocumento',
        'nombre',
        'prefijo',
        'proximaFactura',
        'desde',
        'hasta',
        'resolucion',
        'empresa',
        'fecha_vencimiento',
        'estado',
    )
    ordering = ('id',)


@admin.register(PlazosDecuentosClientes)
class PlazoDtoClienteAdmin(admin.ModelAdmin):
    '''Admin View of PlazoDescuentoClientes'''

    list_display = (
        'id',
        'tercero',
        'quince',
        'treinta',
        'cuarentaYcinco',
        'sesenta',
        'noventa'
    )
    list_filter = ('tercero',)
    search_fields = (
        'id',
        'tercero',
        'quince',
        'treinta',
        'cuarentaYcinco',
        'sesenta',
        'noventa'
    )
    ordering = ('id',)


@admin.register(PlazosDecuentosProveedores)
class PlazoDtoProveedoresAdmin(admin.ModelAdmin):
    '''Admin View of PlazoDescuentoProveedores'''

    list_display = (
        'id',
        'tercero',
        'quince',
        'treinta',
        'cuarentaYcinco',
        'sesenta',
        'noventa'
    )
    list_filter = ('tercero',)
    search_fields = (
        'id',
        'tercero',
        'quince',
        'treinta',
        'cuarentaYcinco',
        'sesenta',
        'noventa'
    )
    ordering = ('id',)


@admin.register(Retenciones)
class RetencionesAdmin(admin.ModelAdmin):
    '''Admin View of Retenciones'''

    list_display = (
        'id',
        'nombre',
        'porcentaje',
        'base',
        'compras',
        'ventas'
    )
    list_filter = ('nombre',)
    search_fields = (
        'id',
        'nombre',
        'porcentaje',
        'base',
        'compras',
        'ventas'
    )
    ordering = ('id',)


@admin.register(RetencionesClientes)
class RetencionesClientesAdmin(admin.ModelAdmin):
    '''Admin View of RetencionesClientes'''

    list_display = (
        'id',
        'tercero',
        'retencion',
        'fija',
    )
    list_filter = ('tercero',)
    search_fields = (
        'id',
        'tercero',
        'retencion',
        'fija',
    )
    ordering = ('id',)


@admin.register(RetencionesProveedor)
class RetencionesProveedorAdmin(admin.ModelAdmin):
    '''Admin View of RetencionesProveedor'''

    list_display = (
        'id',
        'tercero',
        'retencion',
        'fija',
    )
    list_filter = ('tercero',)
    search_fields = (
        'id',
        'tercero',
        'retencion',
        'fija',
    )
    ordering = ('id',)


@admin.register(Terceros)
class TercerosAdmin(admin.ModelAdmin):
    '''Admin View of Retenciones'''

    list_display = (
        'id',
        'tipoDocumento',
        'documento',
        'dv',
        'nombreComercial',
        'nombreContacto',
        'direccion',
        'departamento',
        'municipio',
        'telefonoContacto',
        'correoContacto',
        'correoFacturas',
        'vendedor',
        'formaPago',
        'tipoPersona',
        'regimen',
        'obligaciones',
        'matriculaMercantil',
        'codigoPostal',
        'saldoAFavorProveedor',
        'saldoAFavorCliente',
        'isRetencion',
        'isCliente',
        'isProveedor',
        'isContabilidad',
        'isCompras',
        'isPos',
        'isElectronico',
        'cuenta_x_cobrar',
        'cuenta_x_pagar',
        'cuenta_saldo_a_cliente',
        'cuenta_saldo_a_proveedor',
        'montoCreditoProveedor',
        'montoCreditoClientes',
        'fecha_creacion',
        'fecha_modificacion',
        'estado'
    )
    list_filter = ('isCliente','isProveedor','listaPrecios','nombreComercial',)
    search_fields = (
        'documento',
        'nombreComercial',
    )
    ordering = ('id',)

@admin.register(VendedoresClientes)
class VendedoresClientesAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nombre',
        'usuario',
        'meta'
    )
    list_filter = ('nombre',)
    search_fields = (
        'id',
        'nombre',
        'usuario',
        'meta'
    )
    ordering = ('id',)
# @admin.register(DatosFacturacionElectronica)
# class DatosFacturacionElectronicaAdmin(admin.ModelAdmin):
#     '''Admin View for DatosFacturacionElectronica'''

#     exclude = ('__all__',)
#     list_filter = ('nombreComercial',)


@admin.register(RetencionesEnGeneral)
class RetencionesEnGeneralAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'docReferencia', 'retencion', 'base', 'porcentaje', 'fecha', 'ventas', 'compras', 'total')
    list_filter = ('tipo', 'ventas', 'compras','retencion')
    search_fields = ('docReferencia',)
    date_hierarchy = 'fecha'
    # Campos de solo lectura
    actions = ['marcar_ventas', 'marcar_compras']  # Acciones personalizadas

    def marcar_ventas(self, request, queryset):
        """Marca las retenciones seleccionadas como ventas."""
        queryset.update(ventas=True)

    marcar_ventas.short_description = "Marcar como ventas"

    def marcar_compras(self, request, queryset):
        """Marca las retenciones seleccionadas como compras."""
        queryset.update(compras=True)

    marcar_compras.short_description = "Marcar como compras"

@admin.register(ImpuestosEnGeneral)
class ImpuestosEnGeneralAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'docReferencia', 'Impuesto', 'base', 'porcentaje', 'fecha', 'ventas', 'compras', 'total')
    list_filter = ('tipo', 'ventas', 'compras','Impuesto')
    search_fields = ('docReferencia',)
    date_hierarchy = 'fecha'
    readonly_fields = ('total',)
    actions = ['marcar_ventas', 'marcar_compras']

    def marcar_ventas(self, request, queryset):
        """Marca los impuestos seleccionados como ventas."""
        queryset.update(ventas=True)

    marcar_ventas.short_description = "Marcar como ventas"

    def marcar_compras(self, request, queryset):
        """Marca los impuestos seleccionados como compras."""
        queryset.update(compras=True)

    marcar_compras.short_description = "Marcar como compras"