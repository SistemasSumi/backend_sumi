from django.db.models import F, Sum, Case, When,Value, Q,FloatField, Subquery, OuterRef
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from django.db import models
from datetime import date
from datetime import datetime
from apps.docVentas.models import CxcVentas,PagosVentas
from apps.configuracion.models import Terceros
from rest_framework import serializers 
import json
from django.db.models.functions import Coalesce



def abonos_recibidos(fecha_inicial, fecha_final):

    inicio  = datetime.strptime(fecha_inicial, "%Y-%m-%dT%H:%M:%S.%fZ")
    final   = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ")

    fecha_inicial = inicio.strftime("%Y-%m-%d")
    fecha_final   = final.strftime("%Y-%m-%d")


    print(fecha_inicial,fecha_final)

    informe = Terceros.objects.filter(
        isCliente=True,
        cxcventas_cliente__valorTotal__gt=F('cxcventas_cliente__valorAbono'),
    ).annotate(
        tipo_fac=Case(
            When(isElectronico=True, then=Value('Electronico')),
            default=Value('Pos'),
            output_field=models.CharField()
        ),
        saldo=Sum('cxcventas_cliente__valorTotal',output_field=FloatField()) - Sum('cxcventas_cliente__valorAbono',output_field=FloatField()),
        valorAbonado=Coalesce(
            Subquery(
                PagosVentas.objects.filter(
                    cliente=OuterRef('pk'),
                    fecha__range=(fecha_inicial, fecha_final)
                ).values('cliente').annotate(total_abonado=Sum('total')).values('total_abonado')[:1]
            ),
            0,
            output_field=FloatField()
        )
    ).values(
        'tipo_fac',
        'documento',
        'nombreComercial',
        'formaPago__nombre',
        'saldo',
        'valorAbonado'
    ).order_by('nombreComercial')

    data = dict()
    data['fecha_incial'] = fecha_inicial
    data['fecha_final']  = fecha_final
    data['abonos']  = informe
    return data



