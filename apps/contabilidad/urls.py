from django.urls import path
from  .views import *

app_name = 'apps.contabilidad'

urlpatterns = [
    # path('depa/', guardarDepa, name="EMPRESA"),
    path('puc/', PucApiView.as_view(), name="puc"),
    path('asiento/', getAsiento, name="asiento"),
    path('libroAux/', getLibroAux, name="asiento"),
    path('efectivo/', GetEfectivo, name="asiento"),
    path('setPuc/', setPucDefault, name="asiento"),
    path('saveMovimiento/', saveMovimiento, name="asiento"),
    path('imprimirMovimiento/', imprimirMovimiento, name="asiento"),
    path('setContabilidad/', setContaDeault, name="asiento"),
    path('borrarAsientos/', borrarAsientos, name="asiento"),
    path('balancePrueba/', ReporteBalancePrueba, name="asiento"),
    path('obtener/saldo/cuentas/', obtener_saldo_cuenta, name="asiento"),
    path('estadoFinanciero/', ReporteEstadoFinanciero, name="asiento"),
    path('busquedaAvanzadaCXPM/', BusquedaAvanzadaMovi, name="asiento"),
    path('conciliar/', conciliacionView, name="asiento"),
    path('conciliacion/save/', conciliacionSave, name="asiento"),

     # URL para la vista de traslado_view con ID opcional
    path('traslado/', traslado_view, name='traslado_list'),
    path('traslado/<int:traslado_id>/', traslado_view, name='traslado_detail'),

    path('pagos-caja-menor/', pagos_caja_menor_view, name='pagos-caja-menor'),
    path('pagos-caja-menor/<int:pago_id>/', pagos_caja_menor_view, name='pagos-caja-menor'),

    path('consultar/cajamenor/', ConsultarCaja, name='traslado_detail'),
    path('caja/menor/', CajaMenorView, name='traslado_detail'),
    path('caja/menor/fondo_disponible/', FondoDisponibleCajaMenor, name='traslado_detail'),


    # TODO REPORTES
    path('informes/clientes/abonosRecibidos/', IF_ABONOS_RECIBIDOS, name="asiento"),



    #TODO ELIMINAR TODO
    path('eliminar/detalle/contabilidad/', eliminarDetalle, name="asiento"),
    path('eliminar/asiento/contabilidad/', eliminarAsiento, name="asiento"),

    


    
]

