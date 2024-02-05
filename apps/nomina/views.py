from django.shortcuts import render
from .functions import *
from django.db.models import Q
from .serializers import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


import requests  

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()



@csrf_exempt
@api_view(('GET','POST'))
def setTiposAndConceptosDefault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/conceptosyTipos.json',{})
        saveDefaultConceptosAndTipos(pc)
        return Response({"data":"ok"})
    


@csrf_exempt
@api_view(('GET','POST'))
def obtenerTiposConcepto(request):
    if request.method == "GET":
        tipos = obtenerConceptosSegunTipos()
        return Response(tiposConceptoSerializer(tipos, many=True).data)
    if request.method == "POST":
        concepto = request.data['concepto']
       
        actualizarConcepto(concepto)
        return Response({'data':'ok'})
    
@csrf_exempt
@api_view(('GET','POST'))
def obtenerConceptos(request):
    if request.method == "GET":
        conceptos  = Concepto.objects.filter(
            Q(tipo__nombre= 'Seguridad Social') | Q(tipo__nombre= 'Prestaciones Sociales')
        )
        return Response(ConceptoSerializer(conceptos, many=True).data)
    
@csrf_exempt
@api_view(('GET','POST'))
def obtenerConceptosIngresos(request):
    if request.method == "GET":
        conceptos  = Concepto.objects.filter(
            Q(tipo__nombre= 'Ingresos No Constitutivos de Salario') | Q(tipo__nombre= 'Ingresos Constitutivos de Salario') | Q(tipo__nombre= 'Deducciones')
        )
        return Response(ConceptoSerializer(conceptos, many=True).data)
    



@csrf_exempt
@api_view(('GET','POST'))
def Salud(request):
    if request.method == "GET":
        eps_id = request.GET.get('id')
        
        if eps_id:
            eps = Eps.objects.get(id=eps_id)
            serializer = EpsSerializer(eps)
            return Response(serializer.data)
        else:
            eps = Eps.objects.all()
            return Response(EpsSerializer(eps, many=True).data)

    if request.method == "POST":
        print(request.data)
        serializer = EpsSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':'ok'})

@csrf_exempt
@api_view(('GET','POST'))
def Pension(request):
    if request.method == "GET":
        pension_id = request.GET.get('id')
        if pension_id:
            pension = FondoPension.objects.get(id=pension_id)
            serializer = PensionSerializer(pension)
            return Response(serializer.data)
        else:
            pension = FondoPension.objects.all()
            return Response(PensionSerializer(pension, many=True).data)

    if request.method == "POST":
        print(request.data)
        serializer = PensionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':'ok'})

@csrf_exempt
@api_view(('GET','POST'))
def ArlView(request):
    if request.method == "GET":
        arl_id = request.GET.get('id')
        if arl_id:
            arl = Arl.objects.get(id=arl_id)
            serializer = ArlSerializer(arl)
            return Response(serializer.data)
        else:
            arl = Arl.objects.all()
            return Response(ArlSerializer(arl, many=True).data)
        # arl = Arl.objects.all()
        # return Response(ArlSerializer(arl, many=True).data)

    if request.method == "POST":
        print(request.data)
        serializer = ArlSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':'ok'})

@csrf_exempt
@api_view(('GET','POST','DELETE'))
def Caja(request):
    if request.method == "GET":
        caja_id = request.GET.get('id')
        if caja_id:
            caja = CajaCompensacion.objects.get(id=caja_id)
            serializer = CajaSerializer(caja)
            return Response(serializer.data)
        else:
            caja = CajaCompensacion.objects.all()
            return Response(CajaSerializer(caja, many=True).data)

    if request.method == "POST":
        print(request.data)
        serializer = CajaSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':'ok'})
    if request.method == "DELETE":
        caja_id = request.GET.get('id')
        if caja_id:
            try:
                caja = CajaCompensacion.objects.get(id=caja_id)
                caja.delete()
                return Response({'data': 'deleted'})
            except CajaCompensacion.DoesNotExist:
                return ({'error': 'Caja de compensación no encontrada'})
        else:
            return ({'error': 'ID no proporcionado'})
    

@csrf_exempt
@api_view(('GET','POST'))
def Cesantias(request):
    if request.method == "GET":
        cesantias_id = request.GET.get('id')
        if cesantias_id:
            fondo = FondoCesantias.objects.get(id=cesantias_id)
            serializer = CesantiaSerializer(fondo)
            return Response(serializer.data)
        else:
            fondo = FondoCesantias.objects.all()
            return Response(CesantiaSerializer(fondo, many=True).data)

    if request.method == "POST":
        print(request.data)
        serializer = CesantiaSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':'ok'})
    
@csrf_exempt
@api_view(('GET','POST'))
def Cesantias(request):
    if request.method == "GET":
        cesantias_id = request.GET.get('id')
        if cesantias_id:
            fondo = FondoCesantias.objects.get(id=cesantias_id)
            serializer = CesantiaSerializer(fondo)
            return Response(serializer.data)
        else:
            fondo = FondoCesantias.objects.all()
            return Response(CesantiaSerializer(fondo, many=True).data)

    if request.method == "POST":
        print(request.data)
        serializer = CesantiaSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':'ok'})
    
@csrf_exempt
@api_view(('GET','POST'))
def Deducciones(request):
    if request.method == "GET":
        deduccion_id = request.GET.get('id')
        if deduccion_id:
            deducciones = DeduccionRecurrente.objects.get(id=deduccion_id)
            serializer = DeduccionSerializer(deducciones)
            return Response(serializer.data)
        else:
            deducciones = DeduccionRecurrente.objects.all()
            return Response(DeduccionSerializer(deducciones, many=True).data)

    if request.method == "POST":
        try:
            print(request.data)
            serializer = DeduccionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(DeduccionSerializer(serializer).data)
        except Exception as e:
            # Devuelve un mensaje de error general
            return Response({'error': str(e)}, status=500)
    
    

@csrf_exempt
@api_view(('GET','POST'))
def Ingresos(request):
    if request.method == "GET":
        ingreso_id = request.GET.get('id')
        if ingreso_id:
            ingresos = IngresoRecurrente.objects.get(id=ingreso_id)
            serializer = IngresoSerializer(ingresos)
            return Response(serializer.data)
        else:
            ingresos = IngresoRecurrente.objects.all()
            return Response(IngresoSerializer(ingresos, many=True).data)

    if request.method == "POST":
        print(request.data)
        serializer = IngresoSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




@csrf_exempt
@api_view(['POST','GET','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def empleado_view(request):
    
    if request.method == 'GET':

        empleados = Empleado.objects.select_related('tercero','contrato').all()
        


        return Response(EmpleadoSerializer(empleados,many=True).data)
    
    if request.method == 'PUT':
        import json
        data = json.loads(request.body)
        empleado_id = data['id_empleado']
        
        empleado_actualizado = Empleado.actualizar_empleado_con_contrato_datos_personales(empleado_id, data, request.user)

        # empleados = Empleado.objects.select_related('tercero','contrato').all()
        
        serializer = EmpleadoSerializer(empleado_actualizado)
        serialized_data = serializer.data

        return Response(serialized_data)


    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
      
         
            # Validar campos obligatorios para el modelo Empleado
            campos_empleado_obligatorios = ['nombres', 'apellidos', 'tipoDocumento', 'documento', 'fechaNacimiento', 'correo', 'tercero']
            if not all(key in data for key in campos_empleado_obligatorios):
                return Response({"Faltan campos obligatorios para el Empleado"}, status=400)

            # Validar campos obligatorios para el modelo Contrato
            campos_contrato_obligatorios = ['salarioBase', 'eps', 'arl', 'fondoPension', 'fondoCesantias', 'cajaCompensacion', 'riesgo', 'fechaInicioContrato', 'fechaFinalContrato', 'noContrato', 'tipoContrato', 'tipoTrabajador']
            if not all(key in data for key in campos_contrato_obligatorios):
                return Response({"Faltan campos obligatorios para el Contrato"}, status=400)

            # Si todos los campos obligatorios están presentes, llamar al método crear_empleado_con_contrato
            empleado = Empleado.crear_empleado_con_contrato(data,request.user)
            return Response({"empleado_id": empleado.id}, status=201)

        except ValueError as e:
            return Response({ str(e)}, status=400)

    return Response({"Método no permitido"}, status=405)  

@csrf_exempt
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def empleadoContrato_view(request):
    
    if request.method == 'PUT':
        import json
        data = json.loads(request.body)
        
        contrato_id = data['id']
        contrato_actualizado = Contrato.actualizar_contrato(contrato_id,data,request.user)
        

        serializer = ContratoSerializer(contrato_actualizado)
        serialized_data = serializer.data

        return Response(serialized_data)




