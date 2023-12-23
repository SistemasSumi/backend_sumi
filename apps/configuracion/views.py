from django.shortcuts import render
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import *
from .serializers import *
from django.http import HttpResponse,FileResponse



from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .functions import *
# Create your views here.

import requests    
import base64
import xmltodict
import json



@csrf_exempt
@api_view(('GET','POST'))
def prueba(request):

    if request.method == "GET":
        xmlbase = ""
        with open("factura.xml", "rb") as file:
            encoded = base64.encodebytes(file.read()).decode("utf-8")
            xmlbase = encoded
        url = "https://webservice.facturatech.co/v2/BETA/WSV2DEMO.asmx"
        usuario = "SARPSOFT29122022"
        password = "1a747a245fbcf9eeeb3d0c843e767e4fa304b321d9955b7c0d08460c82eb4750"

        options = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        soapEnveloped = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <uploadInvoiceFile xmlns="http://webservice.facturatech.co/">
                                <username>{usuario}</username>
                                <password>{password}</password>
                                <xmlBase64>{xmlbase}</xmlBase64>
                                </uploadInvoiceFile>
                            </soap:Body>
                            </soap:Envelope>"""
            
        response = requests.post(url, data = soapEnveloped, headers = options)
        print(response.text)
        
        dictionary = xmltodict.parse(response.text)
     
        principal = dictionary['soap:Envelope']
        body = principal['soap:Body']
        uploadInvoiceFileResponse = body['uploadInvoiceFileResponse']
        Result = uploadInvoiceFileResponse['uploadInvoiceFileResult']
        print(Result)

        if int(Result['code']) > 400:
            print("Error al emitir fatura")
            print("--------------------------------------------")
            print("--------------------------------------------")
            print(Result['Msgerror'])
        else:
            print(Result['success'])
        

       
@csrf_exempt
@api_view(('GET','POST'))
def obtenerPDF(request):

    if request.method == "GET":
        
        url = "https://webservice.facturatech.co/v2/BETA/WSV2DEMO.asmx"
        usuario = "SARPSOFT29122022"
        password = "1a747a245fbcf9eeeb3d0c843e767e4fa304b321d9955b7c0d08460c82eb4750"
        prefijo = "TCFA"
        folio   = 25001

        options = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        soapEnveloped = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <downloadPDFFile xmlns="http://webservice.facturatech.co/">
                                <username>{usuario}</username>
                                <password>{password}</password>
                                <prefijo>{prefijo}</prefijo>
                                <folio>{folio}</folio>
                                </downloadPDFFile>
                            </soap:Body>
                            </soap:Envelope>"""
            
        response = requests.post(url, data = soapEnveloped, headers = options)
        print(response.text)
        
        dictionary = xmltodict.parse(response.text)
     
        principal = dictionary['soap:Envelope']
        body = principal['soap:Body']
        downloadPDFFileResponse  = body['downloadPDFFileResponse']
        Result = downloadPDFFileResponse['downloadPDFFileResult']
        print(Result)

        if int(Result['code']) > 400:
            print("Error al descar pdf de la  fatura")
            print("--------------------------------------------")
            print("--------------------------------------------")
            print(Result['Msgerror'])
        else:
            print(Result['resourceData'])
            pdf  = base64.b64decode(Result['resourceData'])
            return HttpResponse(pdf,content_type="application/pdf")
        

@csrf_exempt
@api_view(('GET','POST'))
def verificarStatus(request):

    if request.method == "GET":
        
        url = "https://webservice.facturatech.co/v2/BETA/WSV2DEMO.asmx"
        usuario = "SARPSOFT29122022"
        password = "1a747a245fbcf9eeeb3d0c843e767e4fa304b321d9955b7c0d08460c82eb4750"
        transaccionID = "ldfvfgzzxdaows439g4fuj3pw5k09thk"

        options = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        soapEnveloped = f"""<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                                <documentStatusFile xmlns="http://webservice.facturatech.co/">
                                <username>{usuario}</username>
                                <password>{password}</password>
                                <transaccionID>{transaccionID}</transaccionID>
                                </documentStatusFile>
                            </soap:Body>
                            </soap:Envelope>"""
            
        response = requests.post(url, data = soapEnveloped, headers = options)
        print(response.text)
        
        dictionary = xmltodict.parse(response.text)
     
        principal = dictionary['soap:Envelope']
        body = principal['soap:Body']
        documentStatusFileResponse   = body['documentStatusFileResponse']
        Result = documentStatusFileResponse ['documentStatusFileResult']
        print(Result)

        if int(Result['code']) > 400:
            print("Error al descar pdf de la  fatura")
            print("--------------------------------------------")
            print("--------------------------------------------")
            print(Result['Msgerror'])
        else:
            print(Result['status'])
            # pdf =Result['resourceData']
            # return HttpResponse(pdf,content_type="application/pdf")
        






import openpyxl
@csrf_exempt
@api_view(('GET','POST'))
def getRepor(request):

    if request.method == "GET":
        book = openpyxl.load_workbook('clientes.xlsx',data_only=True)
        hoja = book.active

        celdas = hoja['A2':'T229']

        lista_terceros = []

        lista_cliente = []
        for fila in celdas:
            tercero = [celda.value for celda in fila]
            lista_terceros.append(tercero)

        
        
        for t in lista_terceros:
            c = Terceros()
            if Terceros.objects.filter(documento=t[1]).exists():
                c = Terceros.objects.get(documento=t[1])
            departamento     = Departamentos.objects.get(id = 1)
            municipio        = Municipios.objects.get(id = 1)
            formaDePago      = FormaPago.objects.get(id = t[11])

            vendedor = VendedoresClientes.objects.get(id = t[14])
            c_cobrar = puc.objects.get(id = 1)
            c_saldo  = puc.objects.get(id = 1)

            c.tipoDocumento            = t[0]
            c.documento                = t[1]   
            c.dv                       = t[15]
            c.nombreComercial          = t[2]
            c.nombreContacto           = t[13]
            c.direccion                = t[3]
            c.departamento             = departamento
            c.municipio                = municipio
            c.telefonoContacto         = t[12]
            c.correoContacto           = t[13]
            c.correoFacturas           = t[6]
            c.vendedor  = vendedor
            c.cuenta_x_cobrar        = c_cobrar
            c.cuenta_saldo_a_cliente = c_saldo 
            c.formaPago                = formaDePago
            if t[1] == '1':
                c.tipoPersona              = '2'
            else:
                c.tipoPersona              = '1'
            if t[16] == '49':
                c.regimen              = 'No responsable del IVA'
            else:
                c.regimen              = 'Responsable del IVA'

          
            c.matriculaMercantil       = t[18]
            c.codigoPostal             = t[17]
            c.isCliente                = True
            c.isProveedor              = False
            c.isCompras                = False
            c.isContabilidad           = True
            if t[19] == '0':
                c.isElectronico           = True
            else:
                c.isPos = True

            c.save()
            print(c.nombreComercial)
            # lista_cliente.append(c)
        # Terceros.objects.bulk_create(lista_cliente)


       

@csrf_exempt
@api_view(('GET','POST','PUT'))
def guardarTercero(request):

    if request.method == "GET":
        
        if request.GET.get('id'):
            tercero = getTercero(request.GET.get('id'))
            print(TercerosListSerializer(tercero).data)
            return Response(TercerosListSerializer(tercero).data)
        elif request.GET.get('tipo'):
            tipo = request.GET.get('tipo')
            terceros = getTerceros(tipo)
            return Response(TercerosListSerializer(terceros, many = True).data)
        else:
            tipo = "TODOS"
            terceros = getTerceros(tipo)
            return Response(TercerosListSerializer(terceros, many = True).data)

    print(request.data)
    if request.method == "POST":
        tercero      = request.data['tercero']
        tercero = saveTercero(True,tercero)
        
        return Response(TercerosCreateSerializer(tercero).data)
    if request.method == "PUT":
        tercero      = request.data['tercero']
        tercero = saveTercero(False,tercero)
        return Response(TercerosCreateSerializer(tercero).data)


@csrf_exempt
@api_view(('GET',))
def GetTercerosCompras(request):
    terceros = getProveedoresCompras()
    return Response(TercerosListSerializer(terceros, many = True).data)


@csrf_exempt
@api_view(('GET','POST'))
def setProveedoresDefault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/proveedores_farmac.json',{})
        contaPuc = setDeaultTercerosProvedores(pc)
        return Response({"data":contaPuc})
    

@csrf_exempt
@api_view(('GET','POST'))
def setClientesDefault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/clientes.json',{})
        contaPuc = setDeaultTercerosClientes(pc)
        return Response({"data":contaPuc})
    
@csrf_exempt
@api_view(('GET','POST'))
def chart_compracion_ventas_compras(request):
    if request.method == "GET":
        from .Informes.compras_vs_ventas_chart import obtener_comparacion_ventas_compras_ingresos_por_mes
        pc =  obtener_comparacion_ventas_compras_ingresos_por_mes()
        return Response(pc)
    
@csrf_exempt
@api_view(('GET','POST'))
def chart_cxp(request):
    if request.method == "GET":
        from .Informes.cxp_chart import calcular_deuda
        pc =  calcular_deuda()
        return Response(pc)
    

@csrf_exempt
@api_view(('GET','POST'))
def chart_cxc(request):
    if request.method == "GET":
        from .Informes.cxc_chart import calcular_deuda_ventas
        pc =  calcular_deuda_ventas()
        return Response(pc)
    
@csrf_exempt
@api_view(('GET','POST'))
def setRetencionDefault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/retenciones.json',{})
        contaPuc = actualizarRetencion(pc)
        return Response({"data":contaPuc})
    


@csrf_exempt
@api_view(('GET','POST'))
def setProveedoresDefaultFormaPago(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/update_formaPago_proveedores.json',{})
        contaPuc = setDeaultTercerosProveedoresFormaPago(pc)
        return Response({"data":"ok"})

@csrf_exempt
@api_view(('GET',))
def getClientesElectronicosView(request):
    terceros = getClientesElectronicos()
    return Response(TercerosListSerializer(terceros ,many = True).data)

@csrf_exempt
@api_view(('GET',))
def GetClientesPosView(request):
    terceros = getClientesPos()
    return Response(TercerosListSerializer(terceros ,many = True).data)


def guardarDepa(request):
    depa =  generate_request('https://www.datos.gov.co/resource/xdk5-pm3f.json',{})
    for x in depa:
        depa = Departamentos.objects.get_or_create(
            codigo = x['c_digo_dane_del_departamento'],
            departamento = x['departamento']
        )
        print(depa)
    return Response(status=status.HTTP_204_NO_CONTENT)

def guardarMuni(request):
    depa =  generate_request('https://www.datos.gov.co/resource/xdk5-pm3f.json',{})
    for x in depa:
        depa = Departamentos.objects.get(codigo = x['c_digo_dane_del_departamento'])
        muni = Municipios.objects.get_or_create(
            departamento = depa,
            codigo = x['c_digo_dane_del_municipio'],
            municipio = x['municipio']
        )
        print(muni)
    return Response(status=status.HTTP_204_NO_CONTENT)



def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()



class DepartamentosApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = DepartamentosCreateSerializer

    def get(self, request, format=None):
        dpt = Departamentos.objects.all().prefetch_related('departamentos_municipios')
        return Response(DepartamentosCreateSerializer(dpt, many = True).data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass


class MunicipiosApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = MunicipiosCreateSerializer

    def get(self, request, format=None):
        mun = Municipios.objects.all()
        return Response(MunicipiosCreateSerializer(mun, many = True).data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass

class EmpresaApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = EmpresaCreateSerializer

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        print(self.request.data)
        serializer.is_valid(raise_exception=True)
        import copy
        empresa = serializer.validated_data.copy()
        print(empresa)
        datosFE = empresa.pop('empresa_datosFE')

        newEmpresa = Empresa(**empresa)
        newEmpresa.save()

        newDatosFE = DatosFacturacionElectronica(empresa = newEmpresa, **datosFE)
        newDatosFE.save()

        return Response(serializer.data)

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass


class NumeracionApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = NumeracionSerializer

    def get(self, request, format=None):
        if request.GET.get('tipo'):
            tipo = request.GET.get('tipo')
            num = obtenerNumeracion(tipo)
            return Response(NumeracionSerializer(num, many = True).data)
        else:
            num = numeracion.objects.all()
            return Response(NumeracionSerializer(num, many = True).data)

    def post(self, request, format=True):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass

class TercerosApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = TercerosCreateSerializer

    def get(self, request, format=None):
        tercero = Terceros.objects.all()
        return Response(TercerosListSerializer(tercero, many = True).data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass

class FormasApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = FormaPagoCreateSerializer

    def get(self, request, format=None):
        formas = FormaPago.objects.all()
        return Response(FormaPagoCreateSerializer(formas, many = True).data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        f = FormaPago.objects.get(id = request.data['id'])
        serializer = self.serializer_class(instance = f,data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None):
        pass


class ImpuestosApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = ImpuestosSerializer

    def get(self, request, format=None):
        ipt = Impuestos.objects.all()
        return Response(ImpuestosSerializer(ipt, many = True).data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        ipt = Impuestos.objects.get(id = request.data['id'])
        serializer = self.serializer_class(instance = ipt,data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None):
        pass


class RetencionesApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = RetencionesSerializer

    def get(self, request, format=None):
        rtf = Retenciones.objects.all()
        return Response(RetencionesSerializer(rtf, many = True).data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        rtf = Retenciones.objects.get(id = request.data['id'])
        serializer = self.serializer_class(instance = rtf,data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None):
        pass
   
class VendedoresApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = VendedoresSerializer

    def get(self, request, format=None):
        vendedores = VendedoresClientes.objects.all()
        return Response(VendedoresSerializer(vendedores, many = True).data)

    def post(self, request, format= None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, format=None):
        vnd = VendedoresClientes.objects.get(id = request.data['id'])
        serializer = self.serializer_class(instance = vnd,data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None):
        pass


@csrf_exempt
@api_view(('GET','POST'))
def descuentosProveedores(request):

    if request.method == "GET":
        idProveedor = request.GET.get('id')
        try:
            descuentos = PlazosDecuentosProveedores.objects.get(tercero__id = idProveedor)
        except PlazosDecuentosProveedores.DoesNotExist:
            descuentos = None

        return Response(PlazosDescuentosProveedorSerializer(descuentos).data)

    if request.method == "POST":
        data = request.data
        saveDescuentoProveedor(data)
        return Response({'ok'})
    






@csrf_exempt
@api_view(('GET','POST'))
def retencionesProveedores(request):

    if request.method == "GET":
        idProveedor = request.GET.get('id')
        retenciones = RetencionesProveedor.objects.filter(tercero__id = idProveedor)
        return Response(RetencionesProveedorSerializer(retenciones, many = True).data)

    if request.method == "POST":
        data = request.data
        saveRetencionProveedor(data)
        return Response({'ok'})
    
@csrf_exempt
@api_view(('GET','POST'))
def retencionesClientes(request):

    if request.method == "GET":
        idProveedor = request.GET.get('id')
        retenciones = RetencionesClientes.objects.filter(tercero__id = idProveedor)
        return Response(RetencionesClientesSerializer(retenciones, many = True).data)

    if request.method == "POST":
        data = request.data
        saveRetencionCliente(data)
        return Response({'ok'})
    

@csrf_exempt
@api_view(('GET','POST'))
def DatosDeContacto(request):

    if request.method == "GET":
        tercero = request.GET.get('id')
        contactos = DatosContacto.objects.filter(tercero__id = tercero)
        return Response(DatosContactoSerializer(contactos, many = True).data)

    if request.method == "POST":
        data = request.data
        saveContacto(data)
        return Response({'ok'})
    

@csrf_exempt
@api_view(('GET','POST'))
def DatosBancariosView(request):

    if request.method == "GET":
        tercero = request.GET.get('id')
        bancos  = DatosBancarios.objects.filter(tercero__id = tercero)
        return Response(DatosBancariosSerializer(bancos, many = True).data)

    if request.method == "POST":
        data = request.data
        saveBanco(data)
        return Response({'ok'})




