from django.shortcuts import render
from .functions import *
from .reportes import *
from .serializers import *
from django.db.models import Sum,Case, When, Value, IntegerField,FloatField
from apps.contabilidad.models import asiento,asientoDetalle
from apps.contabilidad.serializers import  asientoSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.




from django.http import HttpResponse,FileResponse


import requests    
import base64
import xmltodict
import json


@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Facturacion(request):


    if request.method == "GET":
        if request.GET.get('tipo'):
            tipo =  request.GET.get('tipo')
            if tipo == "proformas":
                proformas = listadoProformas()
                return Response(proformaSerializer(proformas, many = True).data)
            if tipo == "ventas":
                facturas = listadoFacturas()
                return Response(FacturasSerializer(facturas, many = True).data)
            if tipo == "factura":
                id      = request.GET.get('id')
                factura = getFactura(id)
                return Response(CxcMoviSerializer(factura).data)
    
    
            
    if request.method == "POST":
        cxc = request.data['cxc']
        detalle = request.data['detalle']

        v = saveDocVenta(True,cxc,detalle,request.user)
        return Response(v)
    

    if request.method == "PUT":
        cxc = request.data['cxc']
        v = saveDocVenta(False,cxc,None,request.user)
        return Response(v)


@csrf_exempt
@api_view(('GET',))
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def InvoceReport(request):
    if request.method == "GET":
        if request.GET.get('id'):
            id = request.GET.get('id')
            cxc = getInvoce(id)
            return Response(InvoceSerializer(cxc).data)



@csrf_exempt
@api_view(( 'POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def  proformaAFactura(request):


    if request.method == "POST":
        data = request.data
        factura = saveProformasAFactura(data,request.user)
        return Response(factura)




@csrf_exempt
@api_view(( 'POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Despachos(request):
    if request.method == "POST":
        numero = request.data['numero']
        DespacharFactura(numero)
        return Response({'data':'ok'})
    

@csrf_exempt
@api_view(( 'POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def busquedaAvanzadaFacturas(request):
    if request.method == "POST":
     
        datos = request.data
        facturas = CxcMovi.filter_by_criterio_ventas(datos)
        return Response(FacturasSerializer(facturas, many = True).data)
    


@csrf_exempt
@api_view(( 'POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def busquedaAvanzadaProformas(request):
    if request.method == "POST":
     
        datos = request.data
        facturas = CxcMovi.filter_by_criterio_proformas(datos)
        return Response(proformaSerializer(facturas, many = True).data)


@csrf_exempt
@api_view(('GET',))
def CXC(request):
    if request.method == "GET":
        c = CxcVentas.filter_cxc({})
        return Response(CxcVentasSerializer(c,many = True).data)
    

@csrf_exempt
@api_view(('POST', ))
def busquedaAvanzadaCI(request):
    if request.method == 'POST':
        filtro = CxcVentas.filter_cxc(request.data)
        return Response(CxcVentasSerializer(filtro, many = True).data)


    
@csrf_exempt
@api_view(( 'POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def EliminarProducto(request):
    if request.method == "POST":
        id = request.data['id']
        eliminarProducto(id)
        return Response({'data':'ok'})

@csrf_exempt
@api_view(( 'POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AgregarProducto(request):
    if request.method == "POST":
        id      = request.data['factura']
        detalle = request.data['detalle']
        agregarProducto(id,detalle)
        return Response({'data':'ok'})
    

import base64
import json
@csrf_exempt
@api_view(( 'POST','GET'))
def PruebaPDF(request):
    if request.method == "GET":
        id  = request.GET.get('id')
        cxc = CxcMovi.objects.get(id = id)
        pdf = crearTicketPDF(cxc)
        pdf = pdf.output(cxc.numero+'.pdf','S').encode('latin-1')
        return HttpResponse(bytes(pdf), content_type='application/pdf')


@csrf_exempt
@api_view(( 'POST','GET'))
def pruebaXml(request):
    if request.method == "GET":
        # pdf = crear_xml_factura("TCFA-25002")
        return Response({'data':'ok'})
    

@csrf_exempt
@api_view(('GET','POST'))
def pruebaEnvioFactura(request):

    if request.method == "GET":
        numero  = request.GET.get('numero')
        factura = CxcMovi.objects.get(numero = numero)
        fe = obtenerPDFFactura(factura)
 
        return HttpResponse(fe,content_type="application/pdf")
        
    if request.method == "POST":
        numero  = request.data['numero']
        fe = enviarFactura(numero)
        return Response({'data':fe})




@csrf_exempt
@api_view(('GET','POST'))
def pruebaEnvioFacturaNC(request):

    # if request.method == "GET":
    #     numero  = request.GET.get('numero')
    #     factura = CxcMovi.objects.get(numero = numero)
    #     fe = obtenerPDFFactura(factura)
    #     print(fe)
    #     return HttpResponse(fe,content_type="application/pdf")
        
    if request.method == "POST":
        numero  = request.data['numero']
        nc = enviarNotaCredito(numero)
        # nota = NotaCreditoVentas.objects.get(numero = numero)
        # pdf = obtenerPDFFacturaNota(nota)
        return Response({'data':nc})



@csrf_exempt
@api_view(('GET','POST'))
def descargarXMLFEView(request):
    import base64
    import io

    if request.method == "GET":
        numero  = request.GET.get('numero')
       
        fe = descargarXMLFE(numero)
        try:
            # Decodificar la cadena Base64 en datos binarios
            archivo_binario = base64.b64decode(fe)

            # Configurar la respuesta HTTP para la descarga
            response = HttpResponse(archivo_binario, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename='+numero+'.xml'

            return response
        except Exception as e:
            # Manejar errores aquí (por ejemplo, si la cadena Base64 es inválida)
            return HttpResponse("Error al descargar el archivo: " + str(e))
        return HttpResponse(fe,content_type="application/pdf")
        
    if request.method == "POST":
        numero  = request.data['numero']
        nc = enviarNotaCredito(numero)
        # nota = NotaCreditoVentas.objects.get(numero = numero)
        # pdf = obtenerPDFFacturaNota(nota)
        return Response({'data':nc})


@csrf_exempt
@api_view(('GET','POST'))
def Recontabilizar(request):

    if request.method == "POST":
        numero = request.data['numero']
        cxc = CxcMovi.objects.get(numero = numero)
        detalle = CxcMoviDetalle.objects.filter(factura__id = cxc.id)
        conta  = contabilizarFacturas(cxc,detalle)
        return Response({'data':'ok'})
    

@api_view(('GET','POST'))
def getFacturasXCliente(request):
    if request.method == "GET":
        id     = request.GET.get('tercero')
        fac    = obtenerFacturasClientes(id)

        tercero = Terceros.objects.get(id = id)
        aFavor = asientoDetalle.objects.filter(tercero__id = tercero.id,cuenta__codigo = tercero.cuenta_saldo_a_cliente.codigo ).aggregate(
            
                saldoAFavor=Sum(
                                Case(
                                    When(credito__gt=0, then='credito'),
                                    When(credito__lt=0, then=0),
                                    default=0,
                                    output_field=FloatField(),
                                )
                            )
                            -
                            Sum(
                                Case(
                                
                                    When(debito__gt=0, then='debito'),
                                    When(debito__lt=0, then=0),
                                    default=0,
                                    output_field=FloatField(),
                                )
                            ) 
        )
        if aFavor['saldoAFavor'] is None:
            aFavor['saldoAFavor'] = 0
        
        data = dict()
        data['facturas'] = CxcVentasSerializer(fac,many = True).data
        data['afavor']   = aFavor
        return Response(data)



@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ImprimirIngreso(request):

    if request.method == "GET":

        numero     = request.GET.get('numero')
        tipo       = request.GET.get('tipo')
        pago       = PagosVentas.objects.prefetch_related('detalle_pago').get(numero = numero)
        conta      = obtener_asiento(numero,tipo)
        data = dict()
        data['pago']  = PagoVentasInvoceSerializer(pago).data
        data['conta'] = asientoSerializer(conta).data
        return Response(data)




@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Ingreso(request):

    if request.method == "GET":
        pagos = PagosVentas.objects.all().order_by('-id')[:20]
        return Response(PagoVentasSerializer(pagos, many = True).data)

    if request.method == "POST":
        data = request.data

        pago = crearPagosVenta(True,data['global'],data['detalle'])
        
        pago       = PagosVentas.objects.prefetch_related('detalle_pago').get(numero = pago.numero)
        conta      = obtener_asiento(pago.numero,"CI")
        data = dict()
        data['pago']  = PagoVentasInvoceSerializer(pago).data
        data['conta'] = asientoSerializer(conta).data
        return Response(data)


@csrf_exempt
@api_view(('GET',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def VentasPorVendedor(request):
    ventas = reporte_ventas_x_vendedor(request.user)
    return Response(ventas)


    
@csrf_exempt
@api_view(('GET','POST'))
def setFacturas(request):
    if request.method == "GET":
        # CxPCompras.objects.all().delete()

        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/cxcmovi.json',{})
        # contaPuc = registrarFacturaElectronicaJSON(pc)
        contaPuc = registrarFacturaProformasJSON(pc)
        return Response({"data":"ok"})
    
@csrf_exempt
@api_view(('GET','POST'))
def setFacturasActual(request):
    if request.method == "GET":
        # CxPCompras.objects.all().delete()

        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/cxcmovi_1.json',{})
        contaPuc = registrarFacturaPosJSON(pc)
        return Response({"data":"ok"})
    

@csrf_exempt
@api_view(('GET','POST'))
def setnotasActual(request):
    if request.method == "GET":
        # CxPCompras.objects.all().delete()

        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/notac.json',{})
        contaPuc = registrar_nota_credito_default(pc)
        return Response({"data":"ok"})



import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

@csrf_exempt
@api_view(('GET','POST'))
def setIngresosFarmac(request):
    if request.method == "GET":
        # CxPCompras.objects.all().delete()

        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/comprobantes_ingresos.json',{})
        contaPuc = setPagosDefault(pc)
        return Response({"data":"ok"})




# TODO: INFORMES


@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_ESTADO_CARTERA_CLIENTES(request):



    if request.method == "POST":

        from apps.docVentas.informes.clientes import estado_cartera_cliente

        cliente = request.data['cliente']
        corte   = request.data['fecha_corte']
        rtf     = request.data['retencion']
        

        result = estado_cartera_cliente(cliente_id=cliente,fecha_corte=corte,retencion=rtf)
       
        return Response(result)
    

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_ROTACION_VENTAS(request):



    if request.method == "POST":

        from apps.docVentas.informes.inventario import rotacion_productos_x_ventas

        fecha_inicio = request.data['fecha_inicio']
        fecha_fin    = request.data['fecha_fin']
       
        result = rotacion_productos_x_ventas(fecha_inicio,fecha_fin)
       
        return Response(result)
    

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_VENTAS(request):



    if request.method == "POST":

        from apps.docVentas.informes.ventas import ventas


        print(request.data)
        cliente      = request.data['cliente']
        tipo         = request.data['tipo']
        fecha_inicio = request.data['fecha_inicio']
        fecha_fin    = request.data['fecha_fin']
       
        result = ventas(cliente,tipo,fecha_inicio,fecha_fin)
       
        return Response(result)
    

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_VENTAS_X_VENDEDOR(request):



    if request.method == "POST":

        from apps.docVentas.informes.ventas import obtener_resumen_vendedores


        print(request.data)
        vendedores      = request.data['vendedores']
        fecha_inicio = request.data['fecha_inicio']
        fecha_fin    = request.data['fecha_fin']
       
        result = obtener_resumen_vendedores(vendedores,fecha_inicio,fecha_fin)
       
        return Response(result)


@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_VENTAS_X_VENDEDOR_INDIVIDUAL(request):



    if request.method == "POST":

        from apps.docVentas.informes.ventas import obtener_resumen_ventas_por_vendedor


        print(request.data)
        vendedor    = request.data['vendedor']
        fecha_inicio = request.data['fecha_inicio']
        fecha_fin    = request.data['fecha_fin']

        print(fecha_inicio)

        result = obtener_resumen_ventas_por_vendedor(vendedor,fecha_inicio,fecha_fin)
       

        resultado = dict()
        resultado['fecha_inicial'] = fecha_inicio
        resultado['fecha_final'] = fecha_fin
        resultado['ventas'] = result
        
        return Response(resultado)




@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_VENTAS_X_VENDEDOR_GENERAL(request):



    if request.method == "POST":

        from apps.docVentas.informes.ventas import obtener_resumen_ventas_por_vendedor


        print(request.data)
        Listvendedores    = request.data['vendedores']
        fecha_inicio = request.data['fecha_inicio']
        fecha_fin    = request.data['fecha_fin']

        print(fecha_inicio)

        vendedores = []

        for x in Listvendedores:
            print(x)
            result = dict()
            v = VendedoresClientes.objects.get(nombre = x)
            result['vendedor'] = x
            result['ventas'] = obtener_resumen_ventas_por_vendedor(v.id,fecha_inicio,fecha_fin)
            vendedores.append(result)

        resultado = dict()
        resultado['fecha_inicial'] = fecha_inicio
        resultado['fecha_final'] = fecha_fin
        resultado['vendedores'] = vendedores
        
        return Response(resultado)



@csrf_exempt
@api_view(('POST',))
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def IF_CARTERA_VENCIDA_CLIENTES(request):



    if request.method == "POST":

        from apps.docVentas.informes.clientes import cartera_vencida_cliente

        cliente = request.data['cliente']
        # corte   = request.data['fecha_corte']
        # rtf     = request.data['retencion']
        

        result = cartera_vencida_cliente(cliente_id=cliente)
       
        return Response(result)



@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def notaCredito(request):
    if request.method == 'GET':
        if request.GET.get('tercero'):
            tercero = request.GET.get('tercero')
            cxc = obtener_facturas_x_cliente(tercero)
            return Response(cxc)

        if request.GET.get('productos'):
            factura   = request.GET.get('productos')
            productos = obtener_productos_x_factura(factura)
            return Response(productos)


        notaC = NotaCreditoVentas.objects.all().prefetch_related('detalle_NotaCredito_venta').order_by("-id")[:20]
        return Response(NotaCreditoSerializer(notaC, many = True).data)


    if request.method == 'POST':
        notac = request.data['notaC']
        detalleNotaC = request.data['detalle']

        print(notac)
        print(detalleNotaC)

        guardarNotaC = registrar_notacredito(True, notac, detalleNotaC,request.user)

        notaCReturn = NotaCreditoVentas.objects.get(id = guardarNotaC.id)
        return Response(NotaCreditoSerializer(notaCReturn).data)


    # if request.method == 'PUT':
    #     id   = request.data['id']
    #     nota = request.data['numeroNota']

    #     notaC = NotaCredito.objects.get(id = id)

    #     Contabilizar_NotaCredito(notaC,nota)
    #     return Response({"data":"ok"})