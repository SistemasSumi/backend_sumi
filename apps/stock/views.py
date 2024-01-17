from django.shortcuts import render
from django.db.models import Sum,Case, When, Value, IntegerField,FloatField
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound
from .models import *
from .serializers import *
from apps.users.models import User
from apps.configuracion.models import Impuestos
from apps.contabilidad.models import asientoDetalle
from apps.contabilidad.functions import obtener_asiento
from apps.contabilidad.serializers import asientoSerializer

from .functions import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_ESTADO_CARTERA_PROVEEDOR(request):



    if request.method == "POST":

        from apps.stock.informes.proveedores import estado_cartera_proveedor

        proveedor = request.data['proveedor']
        corte   = request.data['fecha_corte']
        result = estado_cartera_proveedor(proveedor_id=proveedor,fecha_corte=corte)
       
        return Response(result)
    
@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def CERTIFICADO_RETENCION_PROVEEDOR(request):
    if request.method == "POST":
        from apps.stock.informes.proveedores import certificado_retencion_proveedor
        proveedor_id = request.data['proveedor_id']
        fecha_inicio   = request.data['fecha_inicio']
        fecha_fin   = request.data['fecha_fin']
        result = certificado_retencion_proveedor(proveedor_id,fecha_inicio,fecha_fin)
        return Response(result)
    
@csrf_exempt
@api_view(('GET',))
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def IF_CIERRE_INVENTARIO(request):



    if request.method == "GET":

        from apps.stock.informes.inventario import cierreInventario

      
        result = cierreInventario()
       
        return Response(result)
    
    

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_CXP_COMPRAS(request):



    if request.method == "POST":

        from apps.stock.informes.proveedores import cuentas_x_pagar

        proveedor = request.data['proveedor']
        corte   = request.data['fecha_corte']
        result = cuentas_x_pagar(proveedor_id=proveedor,fecha_corte=corte)
       
        return Response(result)


@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_INVENTARIO_GENERAL(request):



    if request.method == "POST":

        from apps.stock.informes.inventario import inventario_general

        bodega = request.data['bodega']
        tipo   = request.data['tipo']
       
        result = inventario_general(bodega,tipo)
       
        return Response(result)
    

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_INVENTARIO_VENCIDO(request):



    if request.method == "POST":

        from apps.stock.informes.inventario import generar_informe_vencimiento

        bodega = request.data['bodega']
        tipo   = request.data['tipo']
       
        result = generar_informe_vencimiento(bodega,tipo)
       
        return Response(result)
    

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_ROTACION_COMPRAS(request):



    if request.method == "POST":

        from apps.stock.informes.inventario import rotacion_productos_x_compras

        fecha_inicio = request.data['fecha_inicio']
        fecha_fin   = request.data['fecha_fin']
       
        result = rotacion_productos_x_compras(fecha_inicio,fecha_fin)
       
        return Response(result)

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_RETENCION_COMPRAS(request):



    if request.method == "POST":

        from apps.stock.informes.proveedores import consultar_retenciones

        fecha_inicio = request.data['fecha_inicio']
        fecha_fin   = request.data['fecha_final']

        print(fecha_inicio,fecha_fin)
       
        result = consultar_retenciones(fecha_inicio,fecha_fin)
       
        return Response(result)

@csrf_exempt
@api_view(('POST',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def IF_COMPRAS_DETALLADAS(request):



    if request.method == "POST":

        from apps.stock.informes.inventario import compras_detalladas

        proveedor    = request.data['proveedor']
        fecha_inicio = request.data['fecha_inicio']
        fecha_fin    = request.data['fecha_final']      
        result = compras_detalladas(proveedor,fecha_inicio,fecha_fin)
        return Response(result)


import openpyxl
@csrf_exempt
@api_view(('GET','POST'))
def SetProduc(request):

    if request.method == "GET":
        book = openpyxl.load_workbook('productos.xlsx',data_only=True)
        hoja = book.active

        celdas = hoja['A2':'R3245']

        lista_productos = []

        lista_p = []
        lista_k = []
        for fila in celdas:
            producto = [celda.value for celda in fila]
            lista_productos.append(producto)


        usuario = User.objects.get(id=1)
        imp = Impuestos.objects.get(id=1)
        for p in lista_productos:
            tipo = tipoProducto.objects.get(id = p[5])
            product = Productos()

            product.id       = p[0]
            product.nombre      =p[2]
            product.marca        =p[4]
            product.Filtro       =p[11]
            product.invima      =p[12]
            product.cum          =p[13]
            product.valorCompra  =str(p[9]).replace(",", ".")
            product.valorVenta   =str(p[6]).replace(",", ".")
            product.valorventa1    =str(p[7]).replace(",", ".")
            product.valorventa2     =str(p[8]).replace(",", ".")
            product.fv               =p[14]
            product.stock_inicial    =p[15]


            product.tipoProducto     = tipo

            if p[16] ==0:
                b = Bodega.objects.get(id=1)
                product.bodega = b
            if p[16] ==1:
                b = Bodega.objects.get(id=3)
                product.bodega = b
            if p[16] ==2:
                b = Bodega.objects.get(id=2)
                product.bodega = b


            if p[17] != '0':
                product.impuesto = imp

            product.codigoDeBarra   =p[1]
            product.unidad        =p[10]
            product.usuario = usuario

            product.nombreymarcaunico =p[3]


            lista_p.append(product)

        Productos.objects.bulk_create(lista_p)

        balances = Productos.objects.filter(stock_inicial__gt = 0)
        t = Terceros.objects.get(documento = "1221981200")
        for x in balances:

            k = Kardex()
            k.producto = x
            k.descripcion = "Saldo Inicial"
            k.tipo       = "SI"
            k.tercero    = t
            k.bodega     = x.bodega
            k.unidades   = x.stock_inicial
            k.balance    = x.stock_inicial
            k.precio     = x.valorCompra
            k.save()




@csrf_exempt
@api_view(('POST','GET'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AjusteInventarioView(request):

    if request.method == "GET":


        ajustes = AjusteStock.objects.filter().select_related('numeracion','usuario').prefetch_related('detalle_ajuste')

        serializers = AjusteSerializer(ajustes,many = True)
        return Response(serializers.data)
    if request.method == "POST":


        data    = request.data['data']
        entradas = request.data['entradas']
        salidas = request.data['salidas']

        result = crear_ajuste_desde_json(data,entradas,salidas,request.user)
       
        return Response(result)


@csrf_exempt
@api_view(('GET','POST'))
def SetInven(request):

    if request.method == "GET":
        book = openpyxl.load_workbook('inventario.xlsx',data_only=True)
        hoja = book.active

        celdas = hoja['A2':'F1012']

        lista_productos = []

        lista_p = []
        lista_k = []
        for fila in celdas:
            producto = [celda.value for celda in fila]
            lista_productos.append(producto)



        for p in lista_productos:
            try:
               x = Productos.objects.get(id=p[0])
            except Productos.DoesNotExist:
                print(p[0])



            i = Inventario()

            i.bodega = x.bodega
            i.idProducto = x
            i.vencimiento = p[1]
            i.valorCompra = p[3]
            i.unidades  =p[5]
            i.lote    =p[2]
            i.estado  =p[4]

            i.save()



@csrf_exempt
@api_view(('GET','POST'))
def getProductos(request):

    # TIPOS
    # getProductos_SinStock
    # getProductosConsumo__SinStock
    # getKardex
    # getInventario
    # getProductosConsumoStock
    # getProductosVentas

    if request.method == "GET":

        if request.GET.get('producto'):
            id = request.GET.get('producto')
            p = Productos.objects.select_related('tipoProducto','bodega').get(id = id)
            return Response(ProductosSerializer(p).data)


        if request.GET.get('getProductosVentas'):
            productos = getProductosVentas()
            return Response(ProductosSerializer(productos, many = True).data)

        if request.GET.get('consumo'):
            productos = getProductosConsumo__SinStock()
            return Response(ProductosSerializer(productos, many = True).data)

        if request.GET.get('getProductos_SinStock'):
            productos = getProductos_SinStock()
            return Response(ProductosSerializer(productos, many = True).data)

        if request.GET.get('id'):
            id = request.GET.get('id')
            print(id)
            inventario = getInventario(id)
            return Response(InventarioSerializer(inventario, many = True).data)





@csrf_exempt
@api_view(('GET',))
def getBodegas(request):


    if request.method == "GET":

        if request.GET.get('bodega'):
            bodega =  request.GET.get('bodega')
            tipo   =  request.GET.get('tipo')
            productos = getProductosBodegasYTipos(bodega,tipo)
            return Response(ProductosSerializer(productos, many = True).data)

        if request.GET.get('kardex'):
            producto =  request.GET.get('kardex')
            productos = getKardex(producto)
            return Response(KardexSerializer(productos, many = True).data)

        productos = getBodegasInventario()
        return Response(BodegaCompleteSerializer(productos, many = True).data)


@csrf_exempt
@api_view(('POST',))
def ordenCompraCorreo(request):
    if request.method == "POST":
        pdf          = request.data['orden']
        asunto       = request.data['asunto']
        nombre       = request.data['nombre']
        destinatario = request.data['destinatario']
        mensaje      = request.data['mensaje']

        enviarCorreoPDF(pdf,asunto,nombre,destinatario,mensaje,"compras")
    return Response({"data":"ok"})


@csrf_exempt
@api_view(('GET',))
def CXP(request):
    if request.method == "GET":
        c = GetCxp()
        return Response(CxPComprasSerializer(c,many = True).data)



@csrf_exempt
@api_view(('GET', 'POST','PUT'))
def ordenCompra(request):
    if request.method == "GET":

        if request.GET.get('id'):
            id    = request.GET.get('id')
            orden = GetOrdenCompra(id)
            return Response(OrdenDeCompraDetailSerializer(orden).data)
        else:
            orden = ListOrdenCompra()
            return Response(OrdenDeCompraBasicSerializer(orden, many = True).data)

    if request.method == "POST":

        orden = request.data['orden']
        detalle = request.data['detalle']

        ordenSave = registrar_OrdenDeCompra(True,orden,detalle)

        ordenReturn = GetOrdenCompra(ordenSave.id)
        return Response(OrdenDeCompraDetailSerializer(ordenReturn).data)

    if request.method == "PUT":

        orden = request.data['orden']
        detalle = request.data['detalle']

        ordenUpdate = registrar_OrdenDeCompra(False,orden,detalle)

        ordenReturn = GetOrdenCompra(ordenUpdate.id)
        return Response(OrdenDeCompraDetailSerializer(ordenReturn).data)



@csrf_exempt
@api_view(('POST', ))
def busquedaAvanzadaOrdenes(request):
    if request.method == 'POST':
        filtro = busquedaAvanzadaOrden(request.data)
        return Response(OrdenDeCompraBasicSerializer(filtro, many = True).data)


@csrf_exempt
@api_view(('POST', ))
def busquedaAvanzadaCuentasXPagar(request):
    if request.method == 'POST':
        filtro = busquedaAvanzadaCxp(request.data)
        return Response(CxPComprasSerializer(filtro, many = True).data)

@csrf_exempt
@api_view(('GET', 'POST', 'PUT'))
def ingresos(request):
    if request.method == "GET":

        if request.GET.get('id'):
            id      = request.GET.get('id')
            ingreso = getIngreso(id)
            return Response(IngresoSerializer(ingreso).data)
        if request.GET.get('oc'):
            id      = request.GET.get('oc')
            ingreso = getIngresoSegunOc(id)
            return Response(IngresoSerializer(ingreso).data)

    if request.method == "POST":

        ingresar = request.data['ingreso']
        detalle  = request.data['detalle']


        newIngreso = registrar_Ingreso(True, ingresar, detalle)

        ingresoReturn = getIngreso(id = newIngreso.id)
        return Response(IngresoSerializer(ingresoReturn).data)

    if request.method == "PUT":
        ingresar = request.data['ingreso']
        detalle  = request.data['detalle']

        actualizarIngreso = registrar_Ingreso(False, ingresar, detalle)

        ingresoReturn = Ingreso.objects.get(id = actualizarIngreso.id)
        return Response(IngresoSerializer(ingresoReturn).data)


@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def notaCredito(request):
    if request.method == 'GET':
        if request.GET.get('tercero'):
            tercero = request.GET.get('tercero')
            ingresos = obtenerIngresosProveedor(tercero)
            return Response(IngresoBasicSerializer(ingresos, many = True).data)

        if request.GET.get('productos'):
            ingreso   = request.GET.get('productos')
            productos = obtenerProductosSegunIngreso(ingreso)
            return Response(IngresoCompleteDetalleSerializer(productos, many = True).data)


        if request.GET.get('existenciaInventario'):
            idProducto  = request.GET.get('id')
            lote        = request.GET.get('lote')
            laboratorio = ""
            existencia  = getExistenciaSegunProductoLoteYLaboratorio(idProducto,lote,laboratorio)

            return Response(existencia)




        notaC = NotaCredito.objects.all().prefetch_related('detalle_NotaCredito').order_by("-id")
        return Response(NotaCreditoSerializer(notaC, many = True).data)


    if request.method == 'POST':
        notac = request.data['notaC']
        detalleNotaC = request.data['detalle']

        print(notac)
        print(detalleNotaC)

        guardarNotaC = registrar_notacredito(True, notac, detalleNotaC,request.user)

        notaCReturn = NotaCredito.objects.get(id = guardarNotaC.id)
        return Response(NotaCreditoSerializer(notaCReturn).data)


    if request.method == 'PUT':
        id   = request.data['id']
        nota = request.data['numeroNota']

        notaC = NotaCredito.objects.get(id = id)

        Contabilizar_NotaCredito(notaC,nota)
        return Response({"data":"ok"})



class ProductosApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]
    create_serializer_class = ProductosCreateSerializer
    update_serializer_class = ProductosUpdateSerializer

    def get(self, request, format=None):
        productos = Productos.objects.select_related('impuesto','tipoProducto','bodega','usuario').all()
        serializer = ProductosSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        from .functions import actualizar_productos
        serializer = self.create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # update = actualizar_productos()
        return Response(serializer.data)

    def put(self, request, format=None):
        from .functions import actualizar_productos
        instancia = Productos.objects.get(id=request.data['id'])
        serializer = self.update_serializer_class(instance=instancia, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # update = actualizar_productos()
        return Response(serializer.data)

    def delete(self, request, format=None):
        pass


class getBodegasAll(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = BodegaSerializer

    def get(self, request, format=None):
        marca = Bodega.objects.all()
        return Response(BodegaSerializer(marca, many = True).data)
class tipo(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes     = [IsAuthenticated]
    serializer_class         = tipoProductoSerializer

    def get(self, request, format=None):
        marca = tipoProducto.objects.all()
        return Response(tipoProductoSerializer(marca, many = True).data)



@csrf_exempt
@api_view(('GET','POST'))
def setProductosDefault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/productos_farmac.json',{})
        contaPuc = setProductosFarmacDefault(pc)
        return Response({"data":"ok"})


@csrf_exempt
@api_view(('GET','POST'))
def setOrdenesDefault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/ordenes_farmac.json',{})
        contaPuc = setOrdenesDefaultFarmac(pc)
        return Response({"data":"ok"})

@csrf_exempt
@api_view(('GET','POST'))
def setOrdenesDefaultOLD(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/orden_compra_viejas.json',{})
        contaPuc = setOrdenesDefaultFarmacVieja(pc)
        return Response({"data":"ok"})


@csrf_exempt
@api_view(('GET','POST'))
def setInventarioStock(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/inventario_farmac.json',{})
        contaPuc = setInventarioDefault(pc)
        return Response({"data":"ok"})

@csrf_exempt
@api_view(('GET','POST'))
def setIngresosDefault(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/ingresos.json',{})
        contaPuc = setIngresosDefaultFarmac(pc)
        return Response({"data":"ok"})
    

@csrf_exempt
@api_view(('GET','POST'))
def setBalanceDefaultFarmac(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/balance_farmac.json',{})
        contaPuc = setBalanceDefault(pc)
        return Response({"data":"ok"})

@csrf_exempt
@api_view(('GET','POST'))
def setIngresosDefaultOLD(request):
    if request.method == "GET":
        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/ingresos_viejos.json',{})
        contaPuc = setIngresosDefaultFarmacViejo(pc)
        return Response({"data":"ok"})

@csrf_exempt
@api_view(('GET','POST'))
def setCxpFarmac(request):
    if request.method == "GET":
        # CxPCompras.objects.all().delete()

        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/cuentas_x_pagar.json',{})
        contaPuc = setCxpDefaultFarmac(pc)
        return Response({"data":"ok"})
    

@csrf_exempt
@api_view(('GET','POST'))
def setEgresoFarmac(request):
    if request.method == "GET":
        # CxPCompras.objects.all().delete()

        pc =  generate_request('https://sumiprodelacosta.com/farmac_deploy/comprobantes_egreso.json',{})
        contaPuc = setPagosDefault(pc)
        return Response({"data":"ok"})


@csrf_exempt
@api_view(('GET','POST'))
def updateIngresoNum(request):
    if request.method == "GET":
        num = numeracion.objects.get(id = 3)

        ingresos = Ingreso.objects.all()

        for x in ingresos:
            x.numeracion = num
            x.numero = num.prefijo+'-'+str(x.consecutivo).zfill(4)
            x.save()
        return Response({"data":"ok"})



@csrf_exempt
@api_view(('GET','POST'))
def eliminarOrdenes(request):
    if request.method == "GET":
        OrdenDetalle.objects.all().delete()
        OrdenDeCompra.objects.all().delete()

        return Response({"data":"ok"})

@csrf_exempt
@api_view(('GET','POST'))
def eliminarProductos(request):
    if request.method == "GET":
        m = Productos.objects.all()
        for x in m:
            x.delete()

        return Response({"data":"ok"})

@api_view(('GET','POST'))
def getFacturasXProveedor(request):
    if request.method == "GET":
        id     = request.GET.get('tercero')
        fac    = obtenerFacturasProveedor(id)

        tercero = Terceros.objects.get(id = id)
        aFavor = asientoDetalle.objects.filter(tercero__id = tercero.id,cuenta__codigo = tercero.cuenta_saldo_a_proveedor.codigo ).aggregate(

                saldoAFavor=

                             Sum(
                                Case(

                                    When(debito__gt=0, then='debito'),
                                    When(debito__lt=0, then=0),
                                    default=0,
                                    output_field=FloatField(),
                                )
                            ) -
                            Sum(
                                Case(
                                    When(credito__gt=0, then='credito'),
                                    When(credito__lt=0, then=0),
                                    default=0,
                                    output_field=FloatField(),
                                )
                            )


        )
        if aFavor['saldoAFavor'] is None:
            aFavor['saldoAFavor'] = 0

        data = dict()
        data['facturas'] = CxPComprasSerializer(fac,many = True).data
        data['afavor']   = aFavor
        return Response(data)


@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Egreso(request):

    if request.method == "GET":
        pagos = PagosCompras.filter_ce({})
        return Response(PagoComprasSerializer(pagos, many = True).data)

    if request.method == "POST":
        data = request.data

        pago = crearPagosCompras(True,data['global'],data['detalle'])
        pago       = PagosCompras.objects.prefetch_related('detalle_compra').get(numero = pago.numero)
        conta      = obtener_asiento(pago.numero,'CE')
        data = dict()
        data['pago'] = PagoComprasInvoceSerializer(pago).data
        data['conta'] = asientoSerializer(conta).data
        return Response(data)

@csrf_exempt
@api_view(('GET','POST'))
def BusquedaAvanzadaCE(request):
    if request.method == "POST":
        
        obj = request.data 

        result = PagosCompras.filter_ce(obj)

     
        return Response(PagoComprasSerializer(result,many = True).data)



@csrf_exempt
@api_view(('GET', 'POST','PUT'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ImprimirEgreso(request):

    if request.method == "GET":

        numero     = request.GET.get('numero')
        tipo       = request.GET.get('tipo')
        pago       = PagosCompras.objects.prefetch_related('detalle_compra').get(numero = numero)
        conta      = obtener_asiento(numero,tipo)
        data = dict()
        data['pago'] = PagoComprasInvoceSerializer(pago).data
        data['conta'] = asientoSerializer(conta).data
        return Response(data)
    

@csrf_exempt
@api_view(('GET',))

def RotacionCompras(request):

    if request.method == "GET":

        query = rotacion_productos_x_compras(None,None)

        print(query)
        return Response(query)


@csrf_exempt
@api_view(('GET','POST'))

def Finiquitar(request):

    if request.method == "POST":
        ingreso = request.data['ingreso']
        print(ingreso)
        
        cxp = CxPCompras.objects.get(ingreso__id = ingreso)
        cxp.estado = True
        cxp.save()
        return Response('ok')

@csrf_exempt
@api_view(('GET','POST'))
def ReporteRetencionesGeneral(request):
    if request.method == "GET":
        # CxPCompras.objects.all().delete()

        pc =  consultar_retenciones('2023-06-01','2023-06-15')
        return Response(pc)




import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()






# class UnidadApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         = UnidadCreateSerializer

#     def get(self, request, format=None):
#         und = Unidad.objects.all()
#         return Response(UnidadCreateSerializer(und, many = True).data)

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def put(self, request, format=None):
#         pass

#     def delete(self, request, format=None):
#         pass

# class BodegaApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         =  BodegaCreateSerializer

#     def get(self, request, format=None):
#         bodega = Bodega.objects.all()
#         return Response(BodegaCreateSerializer(bodega, many = True).data)

#     def post(self, request, format=None):
#         print(self.request.data)
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def put(self, request, format=None):
#         pass

#     def delete(self, request, format=None):
#         pass

# class OrdenDeCompraApiView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes     = [IsAuthenticated]
#     serializer_class         = OrdenDeCompraCreateSerializer

#     def get(self, request, format=None):
#         orden = OrdenDeCompra.objects.getOrdenes()
#         return Response(OrdenDeCompraListSerializer(orden, many = True).data)

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         print(self.request.data)
#         serializer.is_valid(raise_exception=True)
#         import copy
#         orden = serializer.validated_data.copy()
#         print(orden)
#         productos = orden.pop('orden_detalle')

#         newOrden = OrdenDeCompra(**orden)
#         newOrden.save()

#         for p in productos:
#             newOrdenDetalle = OrdenDeCompraDetalle(orden = newOrden, **p)
#             newOrdenDetalle.save()

#         ordenGuardada = OrdenDeCompra.objects.getOrden(newOrden.id)
#         return Response(OrdenDeCompraListSerializer(ordenGuardada).data)

#     def put(self, request, format=None):
#         serializer = self.serializer_class(data=self.request.data)
#         print(self.request.data)
#         serializer.is_valid(raise_exception=True)
#         import copy
#         orden = serializer.validated_data.copy()
#         print(orden)
#         productos = orden.pop('orden_detalle')

#         updateOrden = OrdenDeCompra.objects.get(id=self.request.data['id'])
#         updateOrdenSerializer = OrdenDeCompraUpdateSerializer(updateOrden,self.request.data)
#         updateOrdenSerializer.is_valid(raise_exception=True)
#         updateOrdenSerializer.save()

#         detalleBorrar = OrdenDeCompraDetalle.objects.filter(orden = self.request.data['id'])
#         detalleBorrar.delete()

#         for p in productos:
#             newOrdenDetalle = OrdenDeCompraDetalle(orden = updateOrden, **p)
#             newOrdenDetalle.save()

#         ordenGuardada = OrdenDeCompra.objects.getOrden(self.request.data['id'])
#         return Response(OrdenDeCompraListSerializer(ordenGuardada).data)

#     def delete(self, request, format=None):
#         pass