from django.urls import path
from  .views import *

app_name = 'apps.docVentas'

urlpatterns = [

    path('setfacturas/', setFacturas, name="fac"),
    path('setfacturas1/', setFacturasActual, name="fac"),
    path('setNotas/', setnotasActual, name="fac"),
    path('setIngresos/', setIngresosFarmac, name="fac"),
    path('cotizaciones/', Cotizacion, name="fac"),
    path('cotizaciones/report/', CotizacionReport, name="fac"),
    path('cotizaciones/productos/eliminar/', EliminarProductoCotizacion, name="fac"),
    path('cotizaciones/productos/agregar/', AgregarProductoCotizacion, name="fac"),
    path('facturas/', Facturacion, name="fac"),
    path('facturas/busqueda/', busquedaAvanzadaFacturas, name="fac"),
    path('facturas/productos/eliminar/', EliminarProducto, name="fac"),
    path('facturas/productos/agregar/', AgregarProducto, name="fac"),
    path('facturas/despachos/', Despachos, name="fac"),
    path('facturas/recontabilizar/', Recontabilizar, name="fac"),
    path('facturas/invoce/', InvoceReport, name="fac"),
    path('facturas/invoce/pos/', PruebaPDF, name="fac"),
    path('facturas/invoce/xml/', pruebaXml, name="fac"),
    path('obtenerFacturas/', getFacturasXCliente, name="fac"),
    path('ingreso/', Ingreso, name="fac"),
    path('ingreso/imprimir/', ImprimirIngreso, name="fac"),
    path('ventas_x_vendedor/', VentasPorVendedor, name="fac"),
    path('facturas/invoce/envio/dian/', pruebaEnvioFactura, name="fac"),
    path('facturas/nc/envio/dian/', pruebaEnvioFacturaNC, name="fac"),
    path('facturas/invoce/xml/download/', descargarXMLFEView, name="fac"),
    path('proforma/a/factura/',proformaAFactura),
    path('proforma/busqueda/', busquedaAvanzadaProformas, name="fac"),
    path('cxc/', CXC, name="fac"),
    path('cxc/busqueda/', busquedaAvanzadaCI, name="fac"),
    path('notacredito/', notaCredito, name="fac"),


    #INFORMES
   
    path('clientes/estadoCartera/', IF_ESTADO_CARTERA_CLIENTES, name="fac"),
    path('clientes/carteraVencida/', IF_CARTERA_VENCIDA_CLIENTES, name="fac"),
    path('informes/inventario/rotacion/ventas/', IF_ROTACION_VENTAS, name="fac"),
    path('informes/ventas/', IF_VENTAS, name="fac"),
    path('informes/ventas/vendedor/', IF_VENTAS_X_VENDEDOR, name="fac"),
    path('informes/ventas/vendedor/individual', IF_VENTAS_X_VENDEDOR_INDIVIDUAL, name="fac"),
    path('informes/ventas/vendedor/general', IF_VENTAS_X_VENDEDOR_GENERAL, name="fac"),
    
]