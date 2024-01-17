from django.urls import path, include

from .views import *


from django.conf import settings

app_name = 'apps.stock'



urlpatterns = [
  
    path('setProductos/', setProductosDefault, name="productos"),
    path('eliminarOrdenes/', eliminarOrdenes, name="productos"),
    path('eliminarProductos/', eliminarProductos, name="productos"),
    path('setOrdenes/', setOrdenesDefault, name="productos"),
    path('setOrdenesOLD/', setOrdenesDefaultOLD, name="productos"),
    path('setIngresos/', setIngresosDefault, name="productos"),
    path('setIngresosOLD/', setIngresosDefaultOLD, name="productos"),
    path('setCXP/', setCxpFarmac, name="productos"),
    path('setNumIngresos/', updateIngresoNum, name="productos"),
    path('setInventario/', setInventarioStock, name="productos"),
    path('setBalance/', setBalanceDefaultFarmac, name="productos"),
    path('setEgresos/', setEgresoFarmac, name="productos"),
    path('getProductos/', getProductos, name="getProductos"),
    path('ordenCompra/', ordenCompra, name="ordenCompra"),
    path('ordenCompra/busqueda/', busquedaAvanzadaOrdenes, name="ordenCompra"),
    path('ordenCompra/correo/', ordenCompraCorreo, name="ordenCompra"),
    path('ingreso/', ingresos, name="ingresos"),
    path('bodegas/', getBodegas, name="bodegas"),
    path('bodegas/get/', getBodegasAll.as_view(), name="bodegas"),
    path('tipos/get/', tipo.as_view(), name="bodegas"),
    path('notacredito/', notaCredito, name="notaCredito"),
    path('productos/', ProductosApiView.as_view(), name="notaCredito"),
    path('cxp/',CXP, name="notaCredito"),
    path('cxp/finiquitar/',Finiquitar, name="notaCredito"),
    path('cxp/busqueda/',busquedaAvanzadaCuentasXPagar, name="notaCredito"),
    path('egreso/',Egreso, name="egreso"),
    path('egreso/imprimir/',ImprimirEgreso, name="egreso"),
    path('egreso/busqueda/',BusquedaAvanzadaCE, name="egreso"),
    path('obtenerFacturas/',getFacturasXProveedor, name="notaCredito"),
    path('rotacion/',RotacionCompras, name="notaCredito"),
    path('ajustes/',AjusteInventarioView, name="notaCredito"),
    path('reporte/RetencionGeneral/',ReporteRetencionesGeneral, name="notaCredito"),


    path('informes/compras/retenciones/', IF_RETENCION_COMPRAS, name="unidades"),
    path('informes/proveedores/estadoCartera/', IF_ESTADO_CARTERA_PROVEEDOR, name="unidades"),
    path('informes/proveedores/certificadoRetencion/', CERTIFICADO_RETENCION_PROVEEDOR, name="unidades"),
    path('informes/proveedores/cxp/', IF_CXP_COMPRAS, name="unidades"),
    path('informes/inventario/general/', IF_INVENTARIO_GENERAL, name="unidades"),
    path('informes/inventario/vencido/', IF_INVENTARIO_VENCIDO, name="unidades"),
    path('informes/inventario/rotacion/compras/', IF_ROTACION_COMPRAS, name="unidades"),
    path('informes/inventario/compras/detalladas/', IF_COMPRAS_DETALLADAS, name="unidades"),
    path('informes/inventario/cierre/', IF_CIERRE_INVENTARIO, name="unidades"),
    # path('marcas/', MarcaApiView.as_view(), name="marcas"),
    # path('bodegas/', BodegaApiView.as_view(), name="bodegas"),
    # path('orden/', OrdenDeCompraApiView.as_view(), name="ordenes"),



    ]

