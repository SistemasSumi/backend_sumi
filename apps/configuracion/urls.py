from django.urls import path
from  .views import *

app_name = 'apps.configuracion'

urlpatterns = [
    path('prueba/', prueba, name="EMPRESA"),
    path('pdf/', obtenerPDF, name="EMPRESA"),
    path('rtf/', setRetencionDefault, name="EMPRESA"),
    path('status/', verificarStatus, name="EMPRESA"),
    path('repor/', getRepor, name="EMPRESA"),
    path('depa/', guardarDepa, name="EMPRESA"),
    path('muni/', guardarMuni, name="EMPRESA"),
    path('terceros/', guardarTercero, name="EMPRESA"),
    path('terceros/setDefault/', setProveedoresDefault, name="EMPRESA"),
    path('terceros/setDefault/clientes/', setClientesDefault, name="EMPRESA"),
    path('terceros/setDefault/formaPago/', setProveedoresDefaultFormaPago, name="EMPRESA"),
    path('terceros/proveedores/compras/', GetTercerosCompras, name="EMPRESA"),
    path('terceros/clientes/electronicos/', getClientesElectronicosView, name="EMPRESA"),
    path('terceros/clientes/pos/', GetClientesPosView, name="EMPRESA"),
    path('departamentos/',DepartamentosApiView.as_view()),
    path('municipios/',MunicipiosApiView.as_view()),
    path('formasDePago/',FormasApiView.as_view()),
    path('impuestos/',ImpuestosApiView.as_view()),
    path('retenciones/',RetencionesApiView.as_view()),
    path('empresa/',EmpresaApiView.as_view()),
    path('numeracion/',NumeracionApiView.as_view()),
    # path('terceros/',TercerosApiView.as_view()),
    path('vendedores/',VendedoresApiView.as_view()),
    path('descuentosProveedor/',descuentosProveedores),
    path('retencionesProveedor/',retencionesProveedores),
    path('retencionesCliente/',retencionesClientes),
    path('datosContacto/',DatosDeContacto),
    path('datosBancarios/',DatosBancariosView),




    path('chart_vertical_compras_vs_ventas/',chart_compracion_ventas_compras),
    path('chart_cxp/',chart_cxp),
    path('chart_cxc/',chart_cxc),
   
    
]