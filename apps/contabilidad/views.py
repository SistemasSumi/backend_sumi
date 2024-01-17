from django.shortcuts import render
from .serializers import *
from .models import *
from .functions import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .report import GenerarBalance,EstadoFinancieroReporte
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.db.models import F, Sum, Case, When, FloatField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.

import requests  

class PucApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = pucSerializer

    def get(self, request, format=None):
        p = puc.objects.listar_puc()
        return Response(pucSerializer(p, many = True).data)

    def post(self, request, format=None):
        print(request.data)
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        print(request.data['id'])
        p = puc.objects.get(id=request.data['id'])
        serializer = self.serializer_class(instance = p,data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None):
        pass

@csrf_exempt
@api_view(('GET',))
def getAsiento(request):

    if request.method == "GET":
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
            tipo   = request.GET.get('tipo')
            asientos = obtener_asiento(numero,tipo)
            return Response(asientoSerializer(asientos).data)
    
    return Response({"data":None})


@csrf_exempt
@api_view(('GET',))
def eliminarDetalle(request):

    if request.method == "GET":
        a = asientoDetalle.objects.all()
        i=0;
        for x in a:
            x.delete()
            i+=1
            print(i)
    return Response({"ok"})


@csrf_exempt
@api_view(('GET',))
def eliminarAsiento(request):

    if request.method == "GET":
        asiento.objects.all().delete()
        from apps.configuracion.models import RetencionesEnGeneral,ImpuestosEnGeneral
        RetencionesEnGeneral.objects.all().delete()
        ImpuestosEnGeneral.objects.all().delete()
    
    return Response({"ok"})

@csrf_exempt
@api_view(('GET','POST'))
def obtener_saldo_cuenta(request):
    if request.method == "GET":
        id     = request.GET.get('cuenta')
     
        saldo_a_favor = asientoDetalle.objects.filter(cuenta__id=id).aggregate(
            saldoAFavor= Sum(
                        Case(
                            When(cuenta__naturaleza='DEUDORA', then='debito'),
                            When(cuenta__naturaleza='ACREEDORA', then='credito'),
                            default=0,
                            output_field=FloatField(),
                        )
                    )
                    -
                    Sum(
                        Case(
                        
                            When(cuenta__naturaleza='DEUDORA', then='credito'),
                            When(cuenta__naturaleza='ACREEDORA', then='debito'),
                            default=0,
                            output_field=FloatField(),
                        )
                    ) 
                
                )['saldoAFavor']
        if saldo_a_favor is None:
            saldo_a_favor = 0

        return Response(saldo_a_favor)
    

@csrf_exempt
@api_view(['GET', 'POST', 'PUT'])
def pagos_caja_menor_view(request, pago_id=None):
    if request.method == 'GET':
        # Agrega aquí la lógica para obtener y mostrar detalles de un pago específico
        # según el ID proporcionado en 'pago_id'
        if pago_id is not None:
            pass
        else:
           pagos = PagoCajaMenor.objects.select_related('caja','tercero').all().order_by('-id')
           return Response(PagoCmSerializer(pagos,many= True).data)

    elif request.method == 'POST':
        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.data

        try:
            # Llamar al método para guardar el pago de caja menor
            pago = PagoCajaMenor.guardar_o_actualizar_pago(data, user=request.user)

            # Si el pago se guardó correctamente, retornar una respuesta con los detalles del pago
            return Response({'message': 'Pago de caja menor guardado correctamente.', 'numero_str': pago.numero_str})
        except Exception as e:
            # Si ocurre un error al guardar el pago, retornar una respuesta con el mensaje de error
            return Response({str(e)}, status=400)

    elif request.method == 'PUT':
        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.data

        try:
            # Llamar al método para actualizar el pago de caja menor
            pago = PagoCajaMenor.guardar_o_actualizar_pago(data, user=request.user,pago_id=pago_id)

            # Si el pago se actualizó correctamente, retornar una respuesta con los detalles del pago
            return Response({'message': 'Pago de caja menor actualizado correctamente.', 'numero_str': pago.numero_str})
        except Exception as e:
            # Si ocurre un error al actualizar el pago, retornar una respuesta con el mensaje de error
            return Response({str(e)}, status=400)

@csrf_exempt
@api_view(('GET',))
def GetEfectivo(request):

    if request.method == "GET":
        p = puc.objects.filter(formaPago=True)
        return Response(pucSerializer(p,many = True).data)
    
    return Response({"data":None})


@csrf_exempt
@api_view(('GET','POST','PUT'))
def conciliacionView(request):

    if request.GET.get('mes') and  request.GET.get('year'):
        mes   =  request.GET.get('mes')
        year  =  request.GET.get('year')

        result = reporteCierreContable(mes,year)
        # p = asientoDetalle.calcular_saldo_diferencia_movimientos(datos['mes'],datos['year'],float(datos['saldoBanco']),datos['cuenta'])
        return Response(result)
    

    if request.method == "POST":

        datos =  request.data
        print(datos)
        p = asientoDetalle.calcular_saldo_diferencia_movimientos(datos['mes'],datos['year'],float(datos['saldoBanco']),datos['cuenta'])
        return Response(p)
    
    if request.method == "PUT":

        datos =  request.data
        p = asientoDetalle.objects.get(id=datos['id'])
        p.conciliado = datos['estado']
        p.save()
        # p = asientoDetalle.calcular_saldo_diferencia_movimientos(datos['mes'],datos['year'],float(datos['saldoBanco']),datos['cuenta'])
        return Response({'OK'})
    
    return Response({"data":None})

@csrf_exempt
@api_view(('GET','POST',))
def conciliacionSave(request):


    if request.method == "GET":
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
            try:
                con = Conciliacion.objects.get(numero = numero)
                movimientos = asientoDetalle.objects.filter(
                    cuenta_id=con.cuenta.id,
                    fecha__year=con.year,
                    fecha__month=con.mes,
                    conciliado = True
                ).values('id','tipo','asiento__numero','tercero__nombreComercial','docReferencia','debito','fecha','credito','concepto').order_by('fecha')

                result = dict()

                result['con'] = ConciliacionSerializer(con).data
                print(result)
                result['movimientos'] = movimientos
                return Response(result)
            except:
                raise ValueError('Conciliacion no existe')

    
    if request.method == "POST":

        datos =  request.data

        con = Conciliacion.registrar_conciliacion(datos['mes'],datos['year'],datos['cuenta'],datos['saldoInicial'],datos['saldoBanco'])
        

        
        movimientos = asientoDetalle.objects.filter(
            cuenta_id=con.cuenta.id,
            fecha__year=con.year,
            fecha__month=con.mes,
            conciliado = True
        ).values('id','tipo','asiento__numero','tercero__nombreComercial','docReferencia','debito','fecha','credito','concepto').order_by('fecha')

        result = dict()

        result['con'] = ConciliacionSerializer(con).data
        print(result)
        result['movimientos'] = movimientos
        return Response(result)



@csrf_exempt
@api_view(('GET',))
def ConsultarCaja(request):

    if request.method == "GET":
        c = CajaMenor.obtener_caja()
        return Response(cajaSerializerConGastos(c).data)
    
    return Response({"data":None})


@csrf_exempt
@api_view(('GET',))
def CajaMenorView(request):

    if request.method == "GET":
        c = CajaMenor.abrir_caja()
        return Response(cajaSerializer(c).data)

    if request.method == "POST":

        caja_id = request.data['caja_id']

        c = CajaMenor.cerrar_caja(caja_id)
        return Response(cajaSerializer(c).data)
    
    return Response({"data":None})

@csrf_exempt
@api_view(('GET','POST'))
def FondoDisponibleCajaMenor(request):
    if request.method == "GET":
     
        saldo_a_favor = asientoDetalle.objects.filter(cuenta__codigo=110510).aggregate(
            saldoAFavor= Sum(
                        Case(
                            When(cuenta__naturaleza='DEUDORA', then='debito'),
                            When(cuenta__naturaleza='ACREEDORA', then='credito'),
                            default=0,
                            output_field=FloatField(),
                        )
                    )
                    -
                    Sum(
                        Case(
                        
                            When(cuenta__naturaleza='DEUDORA', then='credito'),
                            When(cuenta__naturaleza='ACREEDORA', then='debito'),
                            default=0,
                            output_field=FloatField(),
                        )
                    ) 
                
                )['saldoAFavor']
        if saldo_a_favor is None:
            saldo_a_favor = 0

        return Response(saldo_a_favor)



@csrf_exempt
@api_view(('GET','POST'))
def getLibroAux(request):

    if request.method == "POST":
        cuenta  = request.data['cuenta']
        tercero = request.data['tercero']
        inicio  = request.data['inicio']
        fin     = request.data['fin']
        
        libro = LibroAux(cuenta,inicio,fin,tercero)

        libro['detalle'] = libroAuxiliarSerializer(libro['detalle'], many = True).data
        return Response(libro)

@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveMovimiento(request):

    if request.method == "GET":
       
        movis = ComprobantesContable.filter_comprobantes({})
        return Response(ComprobanteSerializerList(movis,many = True).data)


    if request.method == "POST":
        movi    = request.data['movi']
        detalle = request.data['detalle']



        movimiento = guardarMovimientoContable(True,movi,detalle,request.user)
        
        movi =  ComprobantesContable.objects.select_related('numeracion','usuario').prefetch_related('comprobante_detalle').get(numero = movimiento.numero)
        
        return Response(ComprobanteSerializer(movi).data)


    if request.method == 'PUT':
        print("hola")
        movi    = request.data['movi']
        detalle = request.data['detalle']


        movimiento = guardarMovimientoContable(False,movi,detalle,request.user)
        
        movi =  ComprobantesContable.objects.select_related('numeracion','usuario').prefetch_related('comprobante_detalle').get(numero = movimiento.numero)
        
        return Response(ComprobanteSerializer(movi).data)







@csrf_exempt
@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def traslado_view(request, traslado_id=None):
    if request.method == 'GET':
        # Lógica para manejar la solicitud GET
        # Por ejemplo, obtener un traslado por ID
        if traslado_id is not None:
            try:
                print(traslado_id)
                traslado = Traslado.objects.get(pk=traslado_id)
                # Aquí puedes devolver los datos del traslado en la respuesta
                print(traslado)

                return Response(TrasladoSerializer(traslado).data)
            except Traslado.DoesNotExist:
                return Response({"error": "Traslado no encontrado"}, status=404)
        else:
            traslados = Traslado.objects.select_related('numeracion','usuario','cuenta_origen','cuenta_destino').all().order_by('-id')
            return Response(TrasladoSerializer(traslados, many = True).data)

        # O manejar una solicitud GET sin ID
        # Devolver todos los traslados, o realizar alguna otra lógica según tu caso

    elif request.method == 'POST':
        # Lógica para manejar la solicitud POST

        
        required_fields = ['numeracion', 'fecha', 'cuenta_origen', 'cuenta_destino', 'monto', 'concepto']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response(f"Los siguientes campos son obligatorios: {', '.join(missing_fields)}",status=400)



        # Obtener los datos del traslado del cuerpo de la solicitud
        data = request.data
        try:
            # Crear el traslado utilizando el método guardar_traslado()
            traslado = Traslado.guardar_traslado(data,request.user)
            # Devolver los datos del traslado creado en la respuesta
            return Response({"id": traslado.id, "numero": traslado.numero}, status=201)
        except Exception as e:
            return Response({str(e)}, status=400)

    elif request.method == 'PUT':
        # Lógica para manejar la solicitud POST
        required_fields = ['fecha', 'cuenta_origen', 'cuenta_destino', 'monto', 'concepto']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response(f"Los siguientes campos son obligatorios: {', '.join(missing_fields)}",status=400)
        

        # Obtener los datos del traslado del cuerpo de la solicitud
        data = request.data
        try:
            # Actualizar el traslado utilizando el método guardar_traslado() con el ID proporcionado
            traslado = Traslado.guardar_traslado(data,request.user, traslado_id)
            # Devolver los datos del traslado actualizado en la respuesta
            return Response({"id": traslado.id, "numero": traslado.numero}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    # Manejo para otros métodos HTTP, si es necesario
    return Response({"message": "Método no permitido"}, status=405)


@csrf_exempt
@api_view(('GET','POST'))
def imprimirMovimiento(request):
    if request.method == "GET":
        numero = request.GET.get('numero')
        movi =  ComprobantesContable.objects.select_related('numeracion','usuario').prefetch_related('comprobante_detalle').get(numero = numero)
       
        return Response(ComprobanteSerializer(movi).data)



@csrf_exempt
@api_view(('GET','POST'))
def BusquedaAvanzadaMovi(request):
    if request.method == "POST":
        
        obj = request.data 

        result = ComprobantesContable.filter_comprobantes(obj)

     
        return Response(ComprobanteSerializerList(result,many = True).data)



@csrf_exempt
@api_view(('GET','POST'))
def borrarAsientos(request):
    if request.method == "GET":
        
        e = asiento.objects.all()
        TAMANO_LOTE = 0
        for a in e:
            TAMANO_LOTE += 1
            print(TAMANO_LOTE)
            a.delete()
        #asiento.objects.all().delete()
       
        return Response('ok')
    


@csrf_exempt
@api_view(('GET','POST'))
def ReporteBalancePrueba(request):
    if request.method == "GET":
        inicio = request.GET.get('inicio')
        final  = request.GET.get('final')

        print(inicio)
        print(final)
        r = GenerarBalance(inicio,final)
       
        return Response(r)
    

@csrf_exempt
@api_view(('GET','POST'))
def ReporteEstadoFinanciero(request):
    if request.method == "GET":
        inicio = request.GET.get('inicio')
        final  = request.GET.get('final')

        print(inicio)
        print(final)
        r = EstadoFinancieroReporte(inicio,final)
       
        return Response(r)





@csrf_exempt
@api_view(('GET','POST'))
def setPucDefault(request):
    if request.method == "GET":
        
        pc =  generate_request('https://sumiprodelacosta.com/cuentas_farmac.json',{})
        contaPuc = savePucDefault(pc)
        return Response({"data":contaPuc})
    
def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()


import openpyxl
@csrf_exempt
@api_view(('GET','POST'))
def setContaDeault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/contabilidad.json',{})
        contaPuc = setContabilidadDefault(pc)
        return Response({"data":"ok"})



# TODO: INFORMES

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_ABONOS_RECIBIDOS(request):



    if request.method == "POST":

        from apps.contabilidad.informes.clientes import abonos_recibidos

        fecha_inicial = request.data['fecha_inicial']
        fecha_final   = request.data['fecha_final']
       
        

        result = abonos_recibidos(fecha_inicial,fecha_final)
       
        return Response(result)
    