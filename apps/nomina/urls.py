from django.urls import path
from  .views import *

app_name = 'apps.nomina'

urlpatterns = [

    path('conceptosDefault/', setTiposAndConceptosDefault, name="fac"),
    path('conceptos/', obtenerTiposConcepto, name="fac"),
    path('conceptosEmpleados/', obtenerConceptos, name="fac"),
  
    path('Salud/', Salud, name="fac"),
    path('pension/', Pension, name="fac"),
    path('arl/', ArlView, name="fac"),
    path('caja/', Caja, name="fac"),
    path('cesantias/', Cesantias, name="fac"),
  
  
    path('empleados/', empleado_view, name="fac"),
  

    
]