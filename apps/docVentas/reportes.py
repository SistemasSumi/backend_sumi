from .models import CxcMovi,CxcVentas
import datetime
import calendar
from apps.configuracion.models import VendedoresClientes
from django.db.models import Sum,Case, When, Value, IntegerField,FloatField,F

from .serializers import ventas_x_vendedor

def reporte_ventas_x_vendedor(user):
    fecha_inicial = obtener_fecha_inicial_mes_actual()
    fecha_final   = obtener_fecha_final_mes_actual()

    vendedor = VendedoresClientes.objects.filter(usuario__id = user.pk)[0]
  



    resumen = (CxcVentas.objects.filter(cliente__vendedor__id = vendedor.id, fecha__range=[fecha_inicial, fecha_final])
                .exclude(cliente__vendedor__meta=0)
                .values('cliente__vendedor__nombre')
                .annotate(
                    monto_total=Sum('valorTotal')+Sum('reteFuente')+Sum('reteIca')+Sum('valorDescuento'),
                    meta_vendedor=F('cliente__vendedor__meta'),
                    avatar=F('cliente__vendedor__usuario__avatar_url'),
                    porcentaje=(Sum('valorTotal') / F('cliente__vendedor__meta')) * 100
                )[0]
            )

  

    ventas = CxcVentas.objects.filter(
        fecha__gte = fecha_inicial,
        fecha__lte = fecha_final, 
        cliente__vendedor__id = vendedor.id
    ).values('cliente__nombreComercial').annotate(
        total = Sum('valorTotal')+Sum('reteFuente')+Sum('reteIca')+Sum('valorDescuento')
    )

   

    data = dict()
    serializer = ventas_x_vendedor(ventas, many=True)
    data['ventas'] = serializer.data
    data['resumen'] = resumen

    return data


def obtener_fecha_inicial_mes_actual():
    today     = datetime.date.today()
    first_day = datetime.date(today.year, today.month, 1)

    return first_day


def obtener_fecha_final_mes_actual():
    today     = datetime.date.today()
    last_day  = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

    return last_day