from rest_framework import serializers
from .validations import *
from .models import *
from apps.configuracion.models import *
from apps.contabilidad.models import *
from django.db import transaction
from apps.contabilidad.functions import EliminarAsiento, obtener_asiento



def saveDefaultConceptosAndTipos(archivo):
    for x in archivo:
        with transaction.atomic():
            tipo     = tiposDeConcepto.objects.get_or_create(nombre = x['tipoDeConcepto'], defaults={'nombre':x['tipoDeConcepto']})[0]
            print(x['concepto'])
            concepto = Concepto.objects.get_or_create(nombre = x['concepto'],tipo = tipo, defaults={'nombre':x['concepto'],'tipo':tipo})

           




def actualizarConcepto(concepto):
    try:
        c      = concepto['cuenta']
        contra = concepto['contrapartida']

        cuenta = puc.objects.get(id = c['id'])
        contra = puc.objects.get(id = contra['id'])


        concepto               = Concepto.objects.get(id = concepto['id'])
        concepto.cuenta        = cuenta
        concepto.contrapartida = contra
        concepto.save()

    except Exception as ex:
        print(ex)
        raise serializers.ValidationError(f'Error {ex}')

    


def obtenerConceptosSegunTipos():
    return tiposDeConcepto.objects.all().prefetch_related('tipos_concepto')


