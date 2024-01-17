from rest_framework import serializers
from django.db import transaction
import json
from .validations import *
from datetime import datetime
from django.utils import timezone
from apps.users.models import User
# from .validations import validarCliente,validarProveedor
from .models import *
from apps.configuracion.models import *
from apps.contabilidad.models import *
from apps.docVentas.models import CxcMovi
from .interfaces import *
from django.core.exceptions import ObjectDoesNotExist
# correos electronicos
import smtplib
import getpass
import time
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from django.db.models import Sum, Max,Value,Q,Subquery, OuterRef,IntegerField,F,Count

from django.db.models.functions import  Coalesce


def registrar_OrdenDeCompra(create, orden, ordenDetalle):
        ordenNew = OrdenDeCompra()
        ValidarOrden(orden)
        if create:
                # Asignación de variables de las Foreign Keys
                num        = numeracion.objects.get(id = orden['numeracion'])
                tercero    = Terceros.objects.get(id = orden['proveedor'])
                formaPago  = FormaPago.objects.get(id = orden['formaPago'])
                usuario    = User.objects.get(id = orden['usuario'])

                # Asugnación de variables en general
                ordenNew.numeracion        = num
                ordenNew.consecutivo       = num.proximaFactura
                ordenNew.prefijo           = num.prefijo
                ordenNew.numero            = num.prefijo+'-'+str(num.proximaFactura).zfill(4)
                ordenNew.proveedor         = tercero
                ordenNew.fecha             = orden['fecha']
                ordenNew.usuario           = usuario
                ordenNew.formaPago         = formaPago
                ordenNew.observacion       = orden['observacion']
                ordenNew.subtotal          = orden['subtotal']
                ordenNew.iva               = orden['iva']
                ordenNew.retencion         = orden['retencion']
                ordenNew.descuento         = orden['descuento']
                ordenNew.total             = orden['total']

                # Atomic que procesa los cambios y añade mas valoes a OrdenDetalle
                with transaction.atomic():
                        ordenNew.save()
                        detalle = []
                        # for que itera todo los campos de OrdenDetalle
                        for item in ordenDetalle:
                                p             = item['producto']
                                prod          = Productos.objects.get(id = p['id'])
                                
                                # DETALLE 
                                d             = OrdenDetalle()
                                d.orden       = ordenNew
                                d.producto    = prod
                                d.cantidad    = item['cantidad']
                                d.valorUnidad = item['valorUnidad']   
                                if item['descuento'] == None or item['descuento'] == '':
                                   d.descuento   = 0
                                else: 
                                   d.descuento   = item['descuento']   
                                if item['iva'] == None or item['iva'] == '':
                                   d.iva   = 0
                                else:
                                   d.iva   = item['iva']
                                # Añade los datos al arreglo "Detalle"
                                detalle.append(d)

                        # Hace una inserción masiva a OrdenDetalle                                
                        OrdenDetalle.objects.bulk_create(detalle)
                        num.proximaFactura += 1
                        num.save()
                return ordenNew
        else:
                # Consulta de la ID del modelo de OrdenDetalle con OrdenDeCompra
                try:
                     ordenNew = OrdenDeCompra.objects.get(id = orden['id'])
                except ordenNew.ObjectDoesNotExist as e:
                        raise serializers.ValidationError('La id por actualizar no existe')
                
                # Asignación de variables de las Foreign Keys
                num       = numeracion.objects.get(id = orden['numeracion'])
                tercero   = Terceros.objects.get(id = orden['proveedor'])
                formaPago = FormaPago.objects.get(id = orden['formaPago'])
                usuario   = User.objects.get(id = orden['usuario'])

                # Asugnación de variables en general
                ordenNew.numeracion        = num
                ordenNew.proveedor         = tercero
                ordenNew.fecha             = orden['fecha']
                ordenNew.usuario           = usuario
                ordenNew.formaPago         = formaPago
                ordenNew.observacion       = orden['observacion']
          
          
                

                ordenNew.subtotal          = orden['subtotal']
                ordenNew.iva               = orden['iva']
                ordenNew.retencion         = orden['retencion']
                ordenNew.descuento         = orden['descuento']
                ordenNew.total             = orden['total']

                # Atomic que procesa los cambios y añade mas valoes a OrdenDetalle
                with transaction.atomic():
                        ordenNew.save()
                        ordenD = OrdenDetalle.objects.filter(orden = orden['id'])
                        ordenD.delete()
                        detalle = []
                        # for que itera todo los campos de OrdenDetalle
                        for item in ordenDetalle:
                                d             = OrdenDetalle()
                                p             = item['producto']
                                prod          = Productos.objects.get(id = p['id'])

                                d.orden       = ordenNew
                                d.producto    = prod
                                d.cantidad    = item['cantidad']
                                d.valorUnidad = item['valorUnidad']   
                                if item['descuento'] == None or item['descuento'] == '':
                                   d.descuento   = 0
                                else: 
                                   d.descuento   = item['descuento']   
                                if item['iva'] == None or item['iva'] == '':
                                   d.iva   = 0
                                else:
                                   d.iva   = item['iva']
                                # Añade los datos al arreglo "Detalle"
                                detalle.append(d)
                        # Hace una inserción masiva a OrdenDetalle        
                        OrdenDetalle.objects.bulk_create(detalle)
                return ordenNew

def ListOrdenCompra():
        return  OrdenDeCompra.objects.all().select_related(
        'numeracion',
        'proveedor',
        'formaPago',
        'usuario'
        ).order_by('-fecha')[:50]


def busquedaAvanzadaOrden(data):
        
        if data['orden']:
                print(data['orden'])
                filtro =  OrdenDeCompra.objects.filter(numero__icontains = data['orden']).select_related(
                'numeracion',
                'proveedor',
                'formaPago',
                'usuario'
                ).order_by('-fecha','-consecutivo')
        
        if data['proveedor']:
                if data['orden']:
                        print('orden_proveedor')
                        filtro = filtro.filter(proveedor__id = data['proveedor'])
                else:
                        filtro =  OrdenDeCompra.objects.filter(proveedor__id = data['proveedor']).select_related(
                        'numeracion',
                        'proveedor',
                        'formaPago',
                        'usuario'
                        ).order_by('-fecha','-consecutivo')
        
        if data['formaDePago']:
                if data['orden'] or data['proveedor']:
                        print('formadepago',data['formaDePago'])
                        filtro = filtro.filter(formaPago__id = data['formaDePago'])
                        print(filtro)
                else:
                        filtro =  OrdenDeCompra.objects.filter(formaPago__id = data['formaDePago']).select_related(
                        'numeracion',
                        'proveedor',
                        'formaPago',
                        'usuario'
                        ).order_by('-fecha','-consecutivo')
        
        if data['fechaInicial']:
                inicio = datetime.strptime(data['fechaInicial']+'T00:00:00', '%Y-%m-%dT%H:%M:%S')
                fin    = datetime.strptime(data['fechaFinal']+'T23:59:59', '%Y-%m-%dT%H:%M:%S')

                print(inicio)
                print(fin)
                
                if data['orden'] or data['proveedor'] or data['formaDePago']:
                        filtro = filtro.filter(fecha__gte=inicio, fecha__lte=fin)
                else:
                        filtro =  OrdenDeCompra.objects.filter(fecha__gte=inicio, fecha__lte=fin).select_related(
                        'numeracion',
                        'proveedor',
                        'formaPago',
                        'usuario'
                        ).order_by('-fecha','-consecutivo')
        
        if  data['orden'] or data['proveedor'] or data['formaDePago'] or data['fechaInicial']:
                pass
        else:
                filtro =  OrdenDeCompra.objects.all().select_related(
                        'numeracion',
                        'proveedor',
                        'formaPago',
                        'usuario'
                        ).order_by('-numero','-fecha')[:50]

        return filtro


def busquedaAvanzadaCxp(data):
    filtro = CxPCompras.objects.prefetch_related(
        'ingreso',
        'formaPago',
        'proveedor'
    ).order_by('-fecha')
    
    condiciones = []
    
    if 'orden' in data and data['orden'] is not None:
        condiciones.append(Q(ingreso__orden__numero__icontains=data['orden']))
    
    if 'proveedor' in data and data['proveedor'] is not None:
        condiciones.append(Q(ingreso__proveedor__id=data['proveedor']))
    
    if 'factura' in data and data['factura'] is not None:
        condiciones.append(Q(factura__icontains=data['factura']))
    
    if 'estado' in data and data['estado'] is not None:
        condiciones.append(Q(estado=data['estado']))
    
    if 'formaDePago' in data and data['formaDePago'] is not None:
        condiciones.append(Q(formaPago__id=data['formaDePago']))
    
    if 'fechaInicial' in data and 'fechaFinal' in data:
        if data['fechaInicial'] is not None and data['fechaFinal'] is not None:
                inicio = datetime.strptime(data['fechaInicial'], '%Y-%m-%d').date()
                fin = datetime.strptime(data['fechaFinal'], '%Y-%m-%d').date()

                condiciones.append(Q(fecha__range=(inicio, fin)))
        
    if 'year' in data and data['year'] is not None:
        condiciones.append(Q(fecha__year=data['year']))
    
    if 'mes' in data and data['mes'] is not None:
        condiciones.append(Q(fecha__month=data['mes']))
    
    if not condiciones:
        filtro = filtro[:20]
    else:
        filtro = filtro.filter(*condiciones)
    
    return filtro


def GetOrdenCompra(id):
        return  OrdenDeCompra.objects.select_related(
                'numeracion',
                'proveedor',
                'formaPago',
                'usuario'
                ).prefetch_related(
                'detalle_orden'
                ).get(id = id)


def GetCxp():
        return  CxPCompras.objects.prefetch_related(
                'ingreso',
                'formaPago',
                'proveedor',
     
                ).filter().order_by('-fecha')[:20]

            
                  
def registrar_Ingreso(create, ingreso, ingresoDetalle):


        # SE CREA UNA NUEVA INSTANCIA AL MODELO INGRESO 

        NewIngreso = Ingreso()

        # SE VALIDA LA INFORMACIÓN ENVIADA POR EL CLIENTE WEB SERVICE HACIA EL MODELO INGRESO
        ValidarIngreso(ingreso)

        # SE VALIDA QUE EL INGRESO CONTENGA ALMENOS UN PRODUCTO
        ValidarDetalle(ingresoDetalle)

        # CONDICIÓN PARA VERIFICAR SI SE VA A CREAR O EDITAR UN INGRESO 
        if create:
                # SE HACE EL LLAMADO A LA TABLA NUMERACION, PARA LA RELACIÓN CON INGRESO
                num     = numeracion.objects.get(id = ingreso['numeracion'])

                # SE HACE EL LLAMADO A LA TABLA OrdenDeCompra, PARA LA RELACIÓN CON INGRESO
                orden   = OrdenDeCompra.objects.get(id = ingreso['orden'])
                # SE HACE EL LLAMADO A LA TABLA User, PARA LA RELACIÓN CON INGRESO
                usuario = User.objects.get(id = ingreso['usuario'])

                # CAPTURAMOS LOS DATOS ENVIADOS POR EL CLIENTE WS Y SE LO ASIGNAMOS A LA VARIABLE,
                # QUE HACE INSTANCIA AL MODELO INGRESO

                NewIngreso.numeracion        = num
                NewIngreso.consecutivo       = num.proximaFactura
                NewIngreso.prefijo           = num.prefijo
                NewIngreso.numero            = num.prefijo+'-'+str(num.proximaFactura).zfill(4)
                NewIngreso.factura           = ingreso['factura']
                NewIngreso.orden             = orden
                NewIngreso.proveedor         = orden.proveedor
                NewIngreso.fecha             = ingreso['fecha']
                NewIngreso.formaPago         = orden.formaPago
                NewIngreso.usuario           = usuario
                NewIngreso.subtotal          = ingreso['subtotal']
                NewIngreso.iva               = ingreso['iva']
                if ingreso['retencion'] is None or ingreso['retencion'] == '':
                        NewIngreso.retencion         = 0
                else:                        
                        NewIngreso.retencion         = ingreso['retencion']

                # VALIDAMOS SI EL INGRESO ENVIADO POR EL CLIENTE WS ES NULO O ESTA VACIO
                if ingreso['descuento'] is None or ingreso['descuento'] == '':
                        NewIngreso.descuento         = 0
                else:
                        NewIngreso.descuento         = ingreso['descuento']
                NewIngreso.total             = ingreso['total']

                

                # LUEGO DE ASIGNAR LOS DATOS DATOS DEL INGRESO CREAMOS UNA INSTANCIA AL MODELO CxPCompras 

                CuentaxP = CxPCompras()



                # ASIGNAMOS LOS DATOS A LA INSTANCIA CREADA DE CxPCompras RELACIONADO CON EL INGRESO
                CuentaxP.ingreso    = NewIngreso 
                CuentaxP.proveedor  = NewIngreso.proveedor
                CuentaxP.base       = NewIngreso.subtotal
                CuentaxP.iva        = NewIngreso.iva
                CuentaxP.reteFuente = NewIngreso.retencion  
                CuentaxP.valorTotal = NewIngreso.total  
                CuentaxP.reteIca    = 0 

                orden.ingresada = True

                with transaction.atomic():
                        # SE GUARDA EL INGRESO  CREADO
                        NewIngreso.save()
                        orden.save()
                        # SE CREA Y SE GUARDA UNA CUENTA X PAGAR RELACIONADA CON EL INGRESO ANTERIOR 
                        CuentaxP.save()

                        # SI EL PROVEEDOR TIENE RETENCIÓN SE VALIDARÁ QUE TENGA "isRetencion" EN TRUE
                        if NewIngreso.proveedor.isRetencion:

                                # SE HARÁ UN FILTRO PARA BUSCAR EL PROVEEDOR EN RETENCIONPROVEEDORES
                                retencion = RetencionesProveedor.objects.filter(tercero = NewIngreso.proveedor.id)
                                # SE RECORRERÁ LA RETENCION EXISTENTE
                                for r in retencion:
                                        # VALIDARÁ SI EL PROVEEDOR TIENE UNA RETENCIÓN FIJA. EN CASO DE NO TENER UNA RETENCIÓN FIJA, EL SUBTOTAL DEBE SER MAYOR A LA BASE DE LA RETENCIÓN
                                        reteIngreso = RetencionIngreso()
                                        if r.fija:
                                                # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                                                reteIngreso.ingreso    = NewIngreso
                                                reteIngreso.retencion  = r.retencion
                                                reteIngreso.base       = NewIngreso.subtotal - NewIngreso.descuento
                                                reteIngreso.procentaje = r.retencion.porcentaje
                                                reteIngreso.total      = reteIngreso.base * reteIngreso.procentaje / 100
                                                # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                                                reteIngreso.save()
                                        else:
                                               if r.retencion.base > 0 and NewIngreso.subtotal >= r.retencion.base:
                                                        # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                                                        reteIngreso.ingreso    = NewIngreso
                                                        reteIngreso.retencion  = r.retencion 
                                                        reteIngreso.base       = NewIngreso.subtotal -  NewIngreso.descuento
                                                        reteIngreso.procentaje = r.retencion.porcentaje
                                                        reteIngreso.total      = reteIngreso.base * reteIngreso.procentaje / 100
                                                        # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                                                        reteIngreso.save()

                        # SE CREA UNA LISTA DETALLE Y GUARDAMOS LOS DETALLES DEL INGRESO YA REGISTRADOS EN LA DB
                        detalleIngresosSave = []

                        # SE RECORRE LOS DETALLES O PRODUCTOS ENVIADOS POR EL CLIENTE WS AL SERVIDOR
                        for item in ingresoDetalle:
                            
                                # SE OBTIENE EL PRODUCTO DEL DETALLE A RECORRER
                                productoParcial       = item['producto']

                                # SE CREA UN OBJETO IngresoDetalle PARA LUEGO SER LLENADO Y GUARDADO
                                ingresoDetalleObject  = IngresoDetalle()    

                                # SE CREA UN OBJETO KARDEX QUE GUARDARA EL HISTORIAL DEL PROUDUCTO A INGRESAR
                                kardexObject          = Kardex()

                                # SE CONSULTA EL PRODUCTO A INGRESAR POR MEDIO DEL LA LLAVE PRIMARIA(ID)
                                product            = Productos.objects.get(id = productoParcial['id'])



                                # Añadiendo los datos de IngresoDetalle
                                ingresoDetalleObject.ingreso          = NewIngreso
                                ingresoDetalleObject.producto         = product
                                ingresoDetalleObject.cantidad         = item['cantidad']
                                ingresoDetalleObject.valorUnidad      = item['valorUnidad']
                                ingresoDetalleObject.lote             = item['lote']
                                # ingresoDetalleObject.laboratorio      = item['laboratorio']
                                ingresoDetalleObject.fechaVencimiento = item['fechaVencimiento']
                                                    
                                if item['iva'] == None or item['iva'] == '':
                                        ingresoDetalleObject.iva = 0
                                else:
                                        ingresoDetalleObject.iva = item['iva']


                                if item['descuento'] == None or item['descuento'] == '':
                                        ingresoDetalleObject.descuento = 0
                                else:
                                        ingresoDetalleObject.descuento = item['descuento']


                                ingresoDetalleObject.subtotal = ingresoDetalleObject.valorUnidad * ingresoDetalleObject.cantidad
                                ingresoDetalleObject.total    = ingresoDetalleObject.subtotal + (ingresoDetalleObject.iva * ingresoDetalleObject.cantidad )- (ingresoDetalleObject.descuento * ingresoDetalleObject.cantidad )
                                 
                                # Guarda los datos de ingreeso Detalle

                                ingresoDetalleObject.save()

                                detalleIngresosSave.append(ingresoDetalleObject)

                                # Ahora se llama los datos del kardex a registrar
                                kardexObject.descripcion = 'Ingreso No. '+ingresoDetalleObject.ingreso.numero
                                kardexObject.tipo        = 'IN'
                                kardexObject.producto    = ingresoDetalleObject.producto
                                kardexObject.tercero     = ingresoDetalleObject.ingreso.proveedor
                                kardexObject.bodega      = ingresoDetalleObject.producto.bodega
                                kardexObject.unidades    = ingresoDetalleObject.cantidad
                                kardexObject.balance     = ingresoDetalleObject.producto.stock_inicial + ingresoDetalleObject.cantidad
                                kardexObject.precio      = ingresoDetalleObject.valorUnidad

                                # Guarda los kardex de los productos
                                kardexObject.save()

                                # validando el inventario
                                if Inventario.objects.filter(
                                        idProducto  = ingresoDetalleObject.producto.id,
                                        lote        = ingresoDetalleObject.lote
                                        ).exists():

                                        # SE OBTIENE EL PRODUCTO PARA ACTUALIZAR SU CANTIDAD EN EL INVENTARIO
                                        producto = Inventario.objects.get(
                                                idProducto  = ingresoDetalleObject.producto.id,
                                                lote        = ingresoDetalleObject.lote)


                                        

                                        # SE ACTUALIZA EL INVENTARIO
                                        producto.unidades +=  ingresoDetalleObject.cantidad
                                        producto.save()

                                        

                                        product.valorCompra = Inventario.obtener_valor_compra_mas_alto(id_producto=producto.idProducto.id, lote=producto.lote)



                                        # SE ACTUALIZA EL PARAMETRO STOCK EN EL PRODUCTO
                                        product.stock_inicial += ingresoDetalleObject.cantidad
                                        product.save()

                                else:
                                        # Registra nuevo producto en el inventario
                                        newProductInv = Inventario()

                                        # Se agisnan los datos
                                        newProductInv.bodega      = ingresoDetalleObject.producto.bodega
                                        newProductInv.idProducto  = ingresoDetalleObject.producto
                                        newProductInv.vencimiento = ingresoDetalleObject.fechaVencimiento
                                        newProductInv.valorCompra = ingresoDetalleObject.valorUnidad
                                        newProductInv.unidades    = ingresoDetalleObject.cantidad
                                        newProductInv.lote        = ingresoDetalleObject.lote
                                        newProductInv.estado      = True                                             
                                      

                                        # Guarda los datos
                                        newProductInv.save()
                                        product.valorCompra = Inventario.obtener_valor_compra_mas_alto(id_producto=newProductInv.idProducto.id, lote=newProductInv.lote)

                                        product.stock_inicial += ingresoDetalleObject.cantidad
                                        product.save()
                                
                                



                        if NewIngreso.iva > 0:
                                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                                        impuestoIngreso = ImpuestoIngreso()
                                        impuestoIngreso.ingreso    = NewIngreso
                                        impuestoIngreso.impuesto   = imp
                                        impuestoIngreso.procentaje = imp.porcentaje
                                        totalIva = 0
                                        totalBase = 0
                                        for item in detalleIngresosSave:
                                                if item.iva > 0:
                                                        totalBase += (item.valorUnidad -  item.descuento) * item.cantidad
                                                        totalIva += item.iva * item.cantidad
                                        impuestoIngreso.base       = totalBase
                                        impuestoIngreso.total      = totalIva    
                                        impuestoIngreso.save()

                        # ENVIAMOS AL METODO Contabilizar_Ingreso EL INGRESO GUARDADO, EL DETALLE DEL INGRESO Y UN TERCERO
                        resultConta =  Contabilizar_Ingreso(
                                        NewIngreso,
                                        detalleIngresosSave,
                                        NewIngreso.proveedor)


                        # OBTENMOS EL ASIENTO DEVUELTO POR EL METODO ANTERIOR (Contabilizar_Ingreso) 
                        asiento               = resultConta['asiento']
                        # OBTENMOS EL DETALLE ASIENTO DEVUELTO POR EL METODO ANTERIOR (Contabilizar_Ingreso) 
                        detalleConta          = resultConta['detalle']


                        # VALIDAMOS QUE EXISTA ALMENOS 2 LINEAS A GUARDAR EN EL ASIENTO DETALLE

                        validarContabilidad(detalleConta)

                        # GUARDAMOS EL ASIENTO
                        asiento.save()

                        # RECORREMOS EL DETALLE DEL ASIENTO y GUARDAMOS EN LA DB
                        for x in detalleConta:
                                x.save()


                        # ACTUALIZAMOS LA NUMERACIÓN PARA AUMENTAR EL CONSECUTIVO SIGUIENTE
                        num.proximaFactura += 1
                        num.save()

                        # RETORNAMOS EL INGRESO GUARDADO LUEGO DE ESTAR  OK
                return NewIngreso                                           



def getIngreso(id):
        return  Ingreso.objects.select_related(
                'numeracion',
                'orden',
                'proveedor',
                'formaPago',
                'usuario'
                ).prefetch_related(
                'ingreso_detalle'
                ).get(id = id)

def getIngresoSegunOc(id:str):
        return  Ingreso.objects.select_related(
                'numeracion',
                'orden',
                'proveedor',
                'formaPago',
                'usuario'
                ).prefetch_related(
                'ingreso_detalle'
                ).get(orden__numero = id) 

def obtenerFacturasProveedor(IdTercero):
        TerceroCompras = CxPCompras.objects.prefetch_related(
                'ingreso',
                'formaPago',
                'proveedor',
     
                ).filter(proveedor__id = IdTercero, estado = False).order_by('fechaVencimiento')
        return TerceroCompras

def obtenerIngresosProveedor(IdTercero):
        Ingresos = Ingreso.objects.filter(proveedor__id = IdTercero).order_by("-id")
        return Ingresos

def obtenerProductosSegunIngreso(idIngreso):
        detalle = IngresoDetalle.objects.filter(ingreso__id = idIngreso)
        return detalle

def crearPagosCompras(create, pagoCompra, pagocompraDetalle):
       NewPago = PagosCompras()
#        ValidarPagoCompras(pagoCompra, pagocompraDetalle)
       if create:
                num       =  numeracion.objects.get(id = pagoCompra['numeracion'])
                usuario   = User.objects.get(id = pagoCompra['usuario'])
                cuenta    = puc.objects.get(id = pagoCompra['formaPago'])
                tercero   = Terceros.objects.get(id = pagoCompra['proveedor'])

                NewPago.numeracion      = num
                NewPago.usuario         = usuario
                NewPago.prefijo         = num.prefijo
                # NewPago.tipoTransaccion = pagoCompra['tipoTransaccion']
                NewPago.tipoTransaccion = NewPago.CON_FACTURA
                NewPago.prefijo         = num.prefijo
                NewPago.consecutivo     = num.proximaFactura
                NewPago.numero          = str(num.proximaFactura).rjust(4,'0') +"-"+ num.prefijo
                NewPago.fecha           = pagoCompra['fecha']
                NewPago.cuenta          = cuenta
                NewPago.proveedor       = tercero
                NewPago.observacion     = pagoCompra['observacion']
                

                
                detailPaymentInvoice = []
                detailPayment = []
                if NewPago.tipoTransaccion == NewPago.CON_FACTURA:
                        pass
                else:   
                     for item in pagocompraDetalle:
                                NewDetailNoInvoice = DetailPayment()

                                cuenta = puc.objects.get(id = item['cuenta'])

                                NewDetailNoInvoice.pago   = NewPago
                                NewDetailNoInvoice.cuenta = cuenta
                                NewDetailNoInvoice.valor  = item['valor']
                                if item['descuento'] is None or item['descuento'] == '':
                                        NewDetailNoInvoice.descuento = 0
                                else:
                                        NewDetailNoInvoice.descuento = item['descuento']
                                NewDetailNoInvoice.total =   item['total']  
                                detailPayment.append(NewDetailNoInvoice)                                    


                with transaction.atomic():
                        NewPago.save()


                        if NewPago.tipoTransaccion == NewPago.CON_FACTURA:
                                for item in pagocompraDetalle:
                                        NewDetail = DetailPaymentInvoice()

                                        cxp = CxPCompras.objects.get(ingreso__orden__numero = item['orden'])

                                        NewDetail.cxpCompra   = cxp
                                        NewDetail.ingreso     = cxp.ingreso
                                        NewDetail.pago        = NewPago
                                        NewDetail.factura     = cxp.factura
                                        NewDetail.orden       = cxp.ingreso.orden
                                        NewDetail.saldoAFavor = item['saldoFavor']
                                        if item['descuento'] is None or item['descuento'] == '':
                                                NewDetail.descuento = 0
                                        else:
                                                NewDetail.descuento = item['descuento']
                                        NewDetail.totalAbono = item['valorAbono']                                                                                
                                        NewDetail.saldo = (float(cxp.valorTotal) - float(cxp.valorAbono)) - (float(NewDetail.totalAbono) + float(NewDetail.saldoAFavor) + float(NewDetail.descuento))                                                                     
                                        NewDetail.save()
                                        detailPaymentInvoice.append(NewDetail)


                        if NewPago.tipoTransaccion == NewPago.CON_FACTURA:
                                for detalle in detailPaymentInvoice:
                                        
                                        factura = detalle.cxpCompra
                                        factura.valorAbono += (float(detalle.totalAbono) + float(detalle.saldoAFavor) + float(detalle.descuento))
                                        if factura.valorTotal <= factura.valorAbono:
                                                factura.estado = True
                                        factura.save()   
                                ContaFacturaPago = Contabilizar_PagoCompras(NewPago, detailPaymentInvoice ,pagoCompra)                                                                                      

                                asiento = ContaFacturaPago['asiento']
                                detalleConta = ContaFacturaPago['detalle']

                                validarContabilidad(detalleConta)
                                asiento.save()
                                for x in detalleConta:
                                        x.save()
                        else:
                                for detalle in detailPayment:
                                        detalle.save()   
                                ContaPagoCompra = Contabilizar_PagoCompras(NewPago, detailPayment, NewPago.proveedor,pagoCompra)    

                                asiento = ContaPagoCompra['asiento']
                                detalleConta = ContaPagoCompra['detalle']
                                validarContabilidad(detalleConta)
                                asiento.save()
                                for x in detalleConta:
                                        x.save()
                        num.proximaFactura += 1
                        num.save()
                return NewPago                        
       else:
                try:
                        pago = PagosCompras.objects.get(id = pagoCompra.id)
                except pago.ObjectDoesnotExist as e:
                        raise serializers.ValidationError("el ID a consultar no existe!")

                usuario = User.objects.get(id = pagoCompra['usuario'])
                cuenta = puc.objects.get(id = pagoCompra['cuenta'])

                pago.usuario = usuario
                pago.cuenta = cuenta
                if pagoCompra['descuento'] is None or pagoCompra['descuento'] == '':
                        pago.descuento = 0
                else:
                        pago.descuento = pagoCompra['descuento']
                if pagoCompra['totalSaldoFavor'] is None or pagoCompra['totalSaldoFavor'] == '':
                        pago.totalSaldoFavor = 0
                else: 
                        pago.totalSaldoFavor = pagoCompra['totalSaldoFavor']
                if pagoCompra['diferenciaBanco'] is None or pagoCompra['diferenciaBanco'] == '':
                        pago.diferenciaBanco = 0
                else:
                        pago.diferenciaBanco = pagoCompra['diferenciaBanco']
                pago.total           = pagoCompra['total']

                with transaction.atomic():
                        pago.save()
                        if pago.tipoTransaccion == NewPago.CON_FACTURA:       
                                detail  = DetailPaymentInvoice.objects.filter(pago__id = pago.id)
                                for item in detail:
                                        cxp = item.cxpCompra
                                        cxp.valorAbono -= item.totalAbono
                                        cxp.estado = False

                                        cxp.save()
                                        item.delete()
                                
                                for item in pagocompraDetalle:
                                        NewDetail = DetailPaymentInvoice()

                                        cxp = CxPCompras.objects.get(id = item['cxpCompra'])

                                        NewDetail.cxpCompra = cxp
                                        NewDetail.ingreso   = cxp.ingreso
                                        NewDetail.pago      = pago
                                        NewDetail.factura   = cxp.factura
                                        NewDetail.orden     = cxp.ingreso.orden
                                        if item['descuento'] is None or item['descuento'] == '':
                                                NewDetail.descuento = 0
                                        else:
                                                NewDetail.descuento = item['descuento']
                                        NewDetail.totalAbono = item['totalAbono']                                                                                
                                        NewDetail.saldo = (cxp.valorTotal - cxp.valorAbono) - NewDetail.totalAbono                                                                     
                                        
                                        NewDetail.save()
                                        factura = cxp
                                        factura.valorAbono += NewDetail.totalAbono
                                        if factura.valorTotal >= factura.valorAbono:
                                                factura.estado = True
                                        factura.save()    
                                
                        else:
                                detail  = DetailPayment.objects.filter(pago__id = pago.id)
                                detail.delete()
                                detailPayment = []     
                                for item in pagocompraDetalle:
                                        NewDetailNoInvoice = DetailPayment()

                                        cuenta = puc.objects.get(id = item['cuenta'])

                                        NewDetailNoInvoice.pago   = pago
                                        NewDetailNoInvoice.cuenta = cuenta
                                        NewDetailNoInvoice.valor  = item['valor']
                                        if item['descuento'] is None or item['descuento'] == '':
                                                NewDetailNoInvoice.descuento = 0
                                        else:
                                                NewDetailNoInvoice.descuento = item['descuento']
                                        NewDetailNoInvoice.total =   item['total']  
                                        detailPayment.append(NewDetailNoInvoice)

                                DetailPayment.objects.bulk_create(detailPayment)
                        
def registrar_notacredito(create, notaC, notaCDetalle,usuario):
        NewnotaC = NotaCredito()
        ValidarNotaC(notaC)
        if create:
                num     = numeracion.objects.get(id = notaC['numeracion'])
                ingreso = Ingreso.objects.get(id = notaC['ingreso'])

                NewnotaC.numeracion      = num
                NewnotaC.prefijo         = num.prefijo
                NewnotaC.consecutivo     = num.proximaFactura
                NewnotaC.numero          = num.prefijo +"-"+ str(num.proximaFactura).zfill(4)
                NewnotaC.ingreso         = ingreso
                NewnotaC.proveedor       = ingreso.proveedor
                NewnotaC.tipoNota        = NewnotaC.DEVOLUCION
                NewnotaC.factura         = ingreso.factura
                NewnotaC.fecha           = notaC['fecha']
                NewnotaC.observacion     = notaC['observacion']
                NewnotaC.subtotal        = notaC['subtotal']
                NewnotaC.usuario         = usuario   

                if notaC['iva'] is None or notaC['iva']  == '':
                        NewnotaC.iva = 0
                else:
                        NewnotaC.iva = notaC['iva']
                if notaC['retencion'] is None or notaC['retencion'] == '':
                        NewnotaC.retencion = 0
                else:
                        NewnotaC.retencion       = notaC['retencion']  

                NewnotaC.total  = notaC['total']   
                with transaction.atomic():
                        NewnotaC.save()
                        baseIva = 0
                        for item in notaCDetalle:
                                detalleNotaC = DetalleNotaCredito()

                                productoPar = item['producto']

                                producto = Productos.objects.get(id = productoPar['id'])
                                
                                detalleNotaC.nota        = NewnotaC
                                detalleNotaC.producto    = producto
                                detalleNotaC.cantidad    = item['cantidad']
                                detalleNotaC.lote        = item['lote']
                            
                                detalleNotaC.valorUnidad = item['valorUnidad']
                                if item['iva'] is None or item['iva'] == '':
                                        detalleNotaC.iva = 0
                                else:
                                        detalleNotaC.iva = item['iva']
                               

                                subtotal = (detalleNotaC.valorUnidad * detalleNotaC.cantidad) 

                                if detalleNotaC.iva > 0:
                                        baseIva += subtotal

                                detalleNotaC.subtotal =  subtotal 
                                detalleNotaC.save()
                                

                                producto.stock_inicial -= detalleNotaC.cantidad
                                producto.save()

                                if Inventario.objects.filter(
                                        idProducto  = detalleNotaC.producto.id,
                                        lote        = detalleNotaC.lote
                                        ).exists():

                                        inventarioEditar = Inventario.objects.get(idProducto = detalleNotaC.producto.id, lote = detalleNotaC.lote)
                                        inventarioEditar.unidades -= detalleNotaC.cantidad
                                        inventarioEditar.save()

                                        kardexInv             = Kardex()
                                        kardexInv.tercero     = NewnotaC.proveedor
                                        kardexInv.producto    = detalleNotaC.producto
                                        kardexInv.tipo        = 'NCC'
                                        kardexInv.descripcion = 'Nota Credito No. '+ NewnotaC.numero
                                        kardexInv.bodega      = detalleNotaC.producto.bodega
                                        kardexInv.unidades    = (0 - detalleNotaC.cantidad)
                                        kardexInv.balance     = producto.stock_inicial
                                        kardexInv.precio      = detalleNotaC.valorUnidad
                                        
                                        kardexInv.save()

                   
                        # LLAMA A LA FACTURA A MODIFICAR
                        cxp = CxPCompras.objects.get(factura = NewnotaC.factura, ingreso = NewnotaC.ingreso.id)
                        # VALIDA SI LA RETENCIÓN DE LA FACTURA SEA MAYÓR A 0
                        if cxp.reteFuente > 0:
                                # FILTRA LAS RETENCIONES EXISTENTES DEL PROVEEDOR Y APLICA LAS RETENCIONES
                                retencion:RetencionIngreso = RetencionIngreso.objects.filter(ingreso__id = cxp.ingreso.id)
                                Base               = NewnotaC.subtotal
                                for r in retencion:
                                        r.base            -=  Base
                                        r.total           -=  NewnotaC.retencion
                                        r.save()
                                        
                                cxp.base           = (cxp.base - Base)
                                cxp.reteFuente     = (cxp.reteFuente - NewnotaC.retencion)
                                
                        
                        if NewnotaC.iva > 0:
                                imp:ImpuestoIngreso = ImpuestoIngreso.objects.filter(ingreso__id = cxp.ingreso.id)
                                for i in imp:
                                        i.base            -=  baseIva
                                        i.total           -=  NewnotaC.iva
                                        i.save()
                                cxp.iva = (cxp.iva - NewnotaC.iva)


                        saldoFactura = cxp.valorTotal - cxp.valorAbono
                        NuevoSaldofactura = 0
                        NuevoSaldoAFavor  = 0
                        if saldoFactura < NewnotaC.total:
                                NuevoSaldoAFavor  = NewnotaC.total - saldoFactura
                                NuevoSaldofactura = NewnotaC.total - NuevoSaldoAFavor

                                cxp.valorTotal -= NuevoSaldofactura
                        else:
                                cxp.valorTotal -= NewnotaC.total
                
                        num = NewnotaC.numeracion 
                        num.proximaFactura += 1
                        num.save()
                        cxp.save()

                return NewnotaC                        
        else:
           pass

# METODO DE CONTABILIDAD V

def Contabilizar_Ingreso(ingreso:Ingreso, detalleIngreso, tercero:Terceros):
        empresa = Empresa.objects.get(id = 1)


        movi = asiento()
        movi.numero       =  ingreso.numero
        movi.fecha        =  ingreso.fecha
        movi.empresa      =  empresa
        movi.tipo         =  'COM'
        movi.concepto     =  "Compra segun OC N°: "+ str(ingreso.orden.numero)
        movi.usuario      =  ingreso.usuario
        movi.totalDebito  = 0
        movi.totalCredito = 0
        movi.docReferencia = ingreso.orden.numero
        listaDetalleAsiento = []

        lineaTercero = asientoDetalle()
        lineaTercero.asiento  = movi
        lineaTercero.tercero  = tercero
        lineaTercero.cuenta   = tercero.cuenta_x_pagar
        lineaTercero.credito  = ingreso.total
        lineaTercero.tipo     =  'COM'

        listaDetalleAsiento.append(lineaTercero)


        for rtf in RetencionIngreso.objects.filter(ingreso__id = ingreso.id):
                lineasRetencion = asientoDetalle()
                lineasRetencion.asiento  = movi
                lineasRetencion.tercero  = tercero
                lineasRetencion.cuenta   = rtf.retencion.compras
                lineasRetencion.credito  = rtf.total
                lineasRetencion.tipo     =  'COM'
                listaDetalleAsiento.append(lineasRetencion)




        if ingreso.descuento > 0:
              if CuentaNecesaria.objects.filter(nombre = "DESCUENTOS COMPRAS").exists():   
                        desc = CuentaNecesaria.objects.get(nombre = "DESCUENTOS COMPRAS")
                        detalleDescuento = asientoDetalle()
        
                        detalleDescuento.asiento = movi
                        detalleDescuento.tercero = tercero
                        detalleDescuento.tipo         =  'COM'
                        detalleDescuento.cuenta  = desc.cuenta 
                        detalleDescuento.credito = ingreso.descuento
                        listaDetalleAsiento.append(detalleDescuento)
        
        
        for imp in  ImpuestoIngreso.objects.filter(ingreso__id = ingreso.id):
                detalle = asientoDetalle()
                detalle.asiento  = movi
                detalle.tercero  = tercero
                detalle.cuenta   = imp.impuesto.compras
                detalle.tipo         =  'COM'
                detalle.debito   = imp.total
                listaDetalleAsiento.append(detalle)

                

        tiposDeMercancia = dict()
        for x in detalleIngreso:
                if x.producto.tipoProducto.nombre in tiposDeMercancia:
                        nombre = x.producto.tipoProducto.nombre
                        tiposDeMercancia[nombre].valor += x.subtotal 
                else:
                        nombre = x.producto.tipoProducto.nombre

                        objecto:tiposMercancia = tiposMercancia(x.producto.tipoProducto,x.producto.tipoProducto.c_tipo,x.subtotal)

                        tiposDeMercancia[nombre] = objecto
                

        for j in tiposDeMercancia:
                detalle = asientoDetalle()
                detalle.asiento  = movi
                detalle.tercero  = tercero
                detalle.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipo

                detalle.tipo         =  'COM'
                detalle.debito   = tiposDeMercancia[j].valor
                listaDetalleAsiento.append(detalle)


        resultado = dict()
        resultado["asiento"] = movi
        resultado["detalle"] = listaDetalleAsiento


       


        return resultado
     
def Contabilizar_PagoCompras(pagoCompras:PagosCompras, Detalle, compra):
        empresa = Empresa.objects.get(id = 1)
        tercero = pagoCompras.proveedor
        movi = asiento()
        movi.numero  = pagoCompras.numero
        movi.fecha   = pagoCompras.fecha
        movi.empresa = empresa
        movi.tipo         =  'CE'
        
        facturas = []
        for x in Detalle:
                facturas.append(x.factura)
        movi.concepto     = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
        movi.usuario      = pagoCompras.usuario
        movi.totalDebito  = 0
        movi.totalCredito = 0

        listaDetalleCompraAsiento = []

        

        if pagoCompras.tipoTransaccion == pagoCompras.CON_FACTURA:

                lineaTercero = asientoDetalle()
                lineaTercero.asiento = movi
                lineaTercero.cuenta  = tercero.cuenta_x_pagar
                lineaTercero.tercero = tercero
                lineaTercero.tipo     =  'CE'
             
                lineaTercero.concepto= 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                lineaTercero.debito  = compra['totalAbono'] + compra['totalDescuento'] + compra['totalSaldoAFavor']
                listaDetalleCompraAsiento.append(lineaTercero)

                if compra['totalSaldoAFavor'] > 0:
                        lineaDetalle          = asientoDetalle()
                        lineaDetalle.asiento  = movi
                        lineaDetalle.cuenta   = tercero.cuenta_saldo_a_proveedor
                        lineaDetalle.tercero  = tercero
                        lineaDetalle.tipo     =  'CE'
                        lineaDetalle.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                        lineaDetalle.credito  = compra['totalSaldoAFavor']
                        listaDetalleCompraAsiento.append(lineaDetalle)


                if compra['totalAbono'] > 0:
                        lineaDetalle  = asientoDetalle()
                        lineaDetalle.asiento  = movi
                        lineaDetalle.cuenta   = pagoCompras.cuenta
                        lineaDetalle.tercero  = tercero
                        lineaDetalle.tipo     =  'CE'
                        lineaDetalle.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                        lineaDetalle.credito  = compra['totalAbono'] + compra['diferencia']
                        listaDetalleCompraAsiento.append(lineaDetalle)


         
                if compra['totalDescuento'] > 0:
                       if CuentaNecesaria.objects.filter(nombre = "DESCUENTOS COMPRAS").exists():   
                                desc = CuentaNecesaria.objects.get(nombre = "DESCUENTOS COMPRAS")
                                detalleDescuento = asientoDetalle()
                
                                detalleDescuento.asiento = movi
                                detalleDescuento.tercero = tercero
                                detalleDescuento.tipo     =  'CE'
                                detalleDescuento.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                                detalleDescuento.cuenta  = desc.cuenta 
                                detalleDescuento.credito  = compra['totalDescuento']
                                listaDetalleCompraAsiento.append(detalleDescuento)

                if compra['diferencia'] > 0:
                        lineaDetalle          = asientoDetalle()
                        lineaDetalle.asiento  = movi
                        lineaDetalle.cuenta   = tercero.cuenta_saldo_a_proveedor
                        lineaDetalle.tercero  = tercero
                        lineaDetalle.tipo     =  'CE'
                        lineaDetalle.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                        lineaDetalle.debito  = compra['diferencia']
                        listaDetalleCompraAsiento.append(lineaDetalle)
        
                              
        else:
                


                lineas = dict()
                for x in Detalle:
                        if x.cuenta.nombre in lineas:
                                nombre = x.cuenta.nombre
                                lineas[nombre].valor += x.total
                        else:
                                nombre = x.cuenta.nombre
                                objecto: pagosCuentas = pagosCuentas(x.cuenta, x.total)
                                lineas[nombre] = objecto

                for z in lineas:
                        lineaDetalle = asientoDetalle()
                        lineaDetalle.asiento = movi
                        lineaDetalle.tercero = tercero
                        lineaDetalle.cuenta  = lineas[z].cuenta
                        lineaDetalle.debito  = lineas[z].valor

                        lineaDetalle.credito = (pagoCompras.total - lineas[z].valor)
                        listaDetalleCompraAsiento.append(lineaDetalle)


        pagoCompras.concepto = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
        pagoCompras.save()
        resultado = dict()
        resultado['asiento'] = movi
        resultado['detalle'] = listaDetalleCompraAsiento 


        return resultado


def Contabilizar_NotaCredito(nota:NotaCredito, numeroNota:str):
        empresa = Empresa.objects.get(id = 1)

        movi               = asiento()
        movi.numero        = nota.numero
        movi.fecha         = nota.fecha
        movi.empresa       = empresa
        movi.tipo          =  'NOCD'
        movi.docReferencia = nota.ingreso.factura
        movi.concepto     = 'Nota Credito Correspondiente a la FAC N° '+str(nota.factura)
        movi.usuario      = nota.usuario
        movi.totalDebito  = 0
        movi.totalCredito = 0

        listaDetalleCompraAsiento = []
        cxp = CxPCompras.objects.get(factura = nota.factura, ingreso = nota.ingreso.id)
        

        saldoFactura = (cxp.valorTotal+nota.total) - cxp.valorAbono
        AProveedor = 0
        NuevoSaldoAFavor  = 0
        
        if saldoFactura < nota.total:
                NuevoSaldoAFavor  = nota.total - saldoFactura
                AProveedor        = nota.total - NuevoSaldoAFavor

        ListaDeProductos = DetalleNotaCredito.objects.filter(nota__id = nota.id) 


        
               
        if NuevoSaldoAFavor > 0:

                proveedor = asientoDetalle()
                proveedor.asiento = movi
                proveedor.cuenta  = nota.proveedor.cuenta_x_pagar
                proveedor.tercero = nota.proveedor
                proveedor.debito  = AProveedor
                proveedor.docReferencia = nota.ingreso.factura

                listaDetalleCompraAsiento.append(proveedor)


                saldoAfavor = asientoDetalle()
                saldoAfavor.asiento = movi
                saldoAfavor.cuenta  = nota.proveedor.cuenta_saldo_a_proveedor
                saldoAfavor.tercero = nota.proveedor
                saldoAfavor.debito  = NuevoSaldoAFavor
                saldoAfavor.docReferencia = nota.ingreso.factura

                listaDetalleCompraAsiento.append(saldoAfavor)

                

             
        else:
                proveedor = asientoDetalle()
                proveedor.asiento = movi
                proveedor.cuenta  = nota.proveedor.cuenta_x_pagar
                proveedor.tercero = nota.proveedor
                proveedor.debito  = nota.total
                proveedor.docReferencia = nota.ingreso.factura

                listaDetalleCompraAsiento.append(proveedor)


        if nota.retencion > 0:
                r = RetencionesProveedor.objects.filter(tercero__id = nota.proveedor.id)
                Base  = nota.subtotal
                for x in r:
                        rtf = asientoDetalle()
                        rtf.asiento = movi
                        rtf.cuenta  = x.retencion.compras
                        rtf.tercero = nota.proveedor
                        rtf.docReferencia = nota.ingreso.factura
                        rtf.debito  = Base * x.retencion.porcentaje / 100
                        listaDetalleCompraAsiento.append(rtf)

        
        if nota.iva > 0:
             
                for imp in  ImpuestoIngreso.objects.filter(ingreso__id = nota.ingreso.id):
                        detalle         = asientoDetalle()
                        detalle.asiento = movi
                        detalle.tercero = nota.proveedor
                        detalle.cuenta  = imp.impuesto.ventas
                        detalle.credito = nota.iva
                        detalle.docReferencia = nota.ingreso.factura

                        listaDetalleCompraAsiento.append(detalle)




        tiposDeMercancia = dict()
        for x in ListaDeProductos:
                if x.producto.tipoProducto.nombre in tiposDeMercancia:
                        nombre = x.producto.tipoProducto.nombre
                        tiposDeMercancia[nombre].valor += x.subtotal 
                else:
                        nombre = x.producto.tipoProducto.nombre

                        objecto:tiposMercancia = tiposMercancia(x.producto.tipoProducto,x.producto.tipoProducto.c_tipo,x.subtotal)

                        tiposDeMercancia[nombre] = objecto
                

        for j in tiposDeMercancia:
                detalle = asientoDetalle()
                detalle.asiento  = movi
                detalle.tercero  = nota.proveedor
                detalle.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipo
                detalle.docReferencia = nota.ingreso.factura

                detalle.credito   = tiposDeMercancia[j].valor
                listaDetalleCompraAsiento.append(detalle)


        
                
        with transaction.atomic():
                if NuevoSaldoAFavor > 0:
                        p = nota.proveedor
                        p.saldoAFavorProveedor += NuevoSaldoAFavor
                        p.save()
                nota.numeroNota     = numeroNota
                nota.contabilizado  = True
                nota.save()
                movi.save()
                
                for x in listaDetalleCompraAsiento:
                        x.save()



def getProductos_SinStock():
        return Productos.objects.all().exclude(bodega=3).select_related('tipoProducto','bodega').order_by('nombreymarcaunico') 
    
def getProductosVentas():
        return Productos.objects.filter(stock_inicial__gt = 0).exclude(bodega=3).select_related('tipoProducto','bodega','impuesto').order_by('nombre') 


def getProductosConsumo__SinStock():
        return Productos.objects.filter(bodega = 3).select_related('tipoProducto','bodega').order_by('nombre') 


def getProductosConsumoStock():
        return Productos.objects.filter(bodega = 3,stock_inicial__gt = 0).select_related('tipoProducto','bodega').order_by('nombre')


def getKardex(idproducto):
    
    p = Productos.objects.get(id = idproducto)

    print(p.codigoDeBarra)
    return Kardex.objects.filter(producto__id=idproducto).select_related('producto','tercero','bodega')


def getInventario(idproducto):
    return Inventario.objects.filter(idProducto=idproducto,unidades__gt = 0).select_related('idProducto','bodega').order_by('vencimiento')



def getBodegasInventario():
        return Bodega.objects.prefetch_related('bodega_tiposP','bodega_tiposP__productos_tipo_producto').all()

def getProductosBodegasYTipos(bodega:any,tipo:any):
        return Productos.objects.select_related(
                'impuesto',
                'impuesto__compras',
                'impuesto__ventas',
                'tipoProducto',
                'tipoProducto__c_tipo',
                'tipoProducto__bodega',
                'bodega',
                'usuario').filter(bodega__id = bodega, tipoProducto__id = tipo)



def getExistenciaSegunProductoLoteYLaboratorio(idproducto:int,lote:str,laboratorio:str):
        print(idproducto)
        print(lote)
        print(laboratorio)
        return Inventario.objects.filter(idProducto__id = idproducto,lote = lote).values('unidades')[0]
      


from base64 import b64decode
def enviarCorreoPDF(pdf,asunto,nombre,destinatario, msj, tipo):
        
        
        # LISTADO DE CORREOS SUMIPROD DE LA COSTA S.A.S.
        correos  = dict()
        password = dict()

        correos = {
                "compras":"compras@sumiprodelacosta.com",
                "contabilidad":"contabilidad@sumiprodelacosta.com"
        }
        password = {
                "compras":"Compras123456.",
                "contabilidad":"Contabilidad2023*"
        }
        
        mensaje            = MIMEMultipart()
        mensaje['from']    = correos[tipo]
        mensaje['to']      = destinatario
        mensaje['Subject'] = asunto

        firma = open_html(tipo)

        mensaje.attach(MIMEText(msj,'plain'))
        mensaje.attach(MIMEText(firma,'html'))
        
        adjunto = email.mime.base.MIMEBase('application', 'octet-stream')
     

        deco = b64decode(pdf)
        
        f = open("file.pdf", 'wb')
        f.write(deco)
        f.close()


        archivo = open("file.pdf", 'rb')
      
        adjunto.set_payload((archivo).read())
        encoders.encode_base64(adjunto)

        adjunto.add_header('Content-Disposition', "attachment; filename= %s" % nombre+".pdf")

        mensaje.attach(adjunto)
        archivo.close()
   
        server = smtplib.SMTP('smtp.hostinger.com: 587')
        server.starttls()

        server.login(correos[tipo] ,password[tipo])
        
        texto = mensaje.as_string()
        server.sendmail(correos[tipo],destinatario, texto)
        server.quit()


def open_html(tipo):
    html_data: str = ""
    with open("correosTemplates/"+tipo+".html", mode="r", encoding="utf-8") as data:
        html_data = data.read().replace("\n", "")
    return html_data




def setProductosFarmacDefault(archivo):
        listado = []
        for x in archivo['productos']:
                p = Productos()

                if x['tipoProducto'] == 0:
                        print(x['ubicacion'])
                        bodega = Bodega.objects.get(id = 1)
                        t = x['ubicacion']
                        tipoP   = tipoProducto.objects.get(nombre = t)
                elif x['tipoProducto'] == 2:
                        print(x['ubicacion'])

                        bodega = Bodega.objects.get(id = 2)
                        t = x['ubicacion']+'*'
                        tipoP   = tipoProducto.objects.get(nombre = t)
                else:
                        print(x['ubicacion'])

                        bodega = Bodega.objects.get(id = 3)
                        t = x['ubicacion']
                        tipoP   = tipoProducto.objects.get(nombre = t)

                p.nombre = x['Nombre']

                print(p.nombre)
                if 'filtro' in x:
                        p.Filtro = x['filtro'].upper()
                else:
                        p.Filtro = "INSUMOS"
                p.invima = x['invima']
                p.cum    = x['cum']
                valor_compra = str(x['Valorcompra']).replace(',', '.')
                p.valorCompra = float(valor_compra)
                p.fv  = x['FV']
                p.stock_inicial = 0
                p.stock_min = 0
                p.stock_max = 0

                p.bodega  = bodega
                p.tipoProducto = tipoP

                if x['iva'] > 0:
                        p.impuesto = Impuestos.objects.get(id=1)
                p.codigoDeBarra = x['codigodebarra']
                p.unidad  = x['unidad'].upper()
                p.usuario = User.objects.get(pk=1)
                p.nombreymarcaunico = x['nombreYmarcaUnico']
                p.laboratorio = x['marca']
                listado.append(p)
        
        Productos.objects.bulk_create(listado)
        return True



def setOrdenesDefaultFarmac(archivo):
     
        with transaction.atomic():
                for x in archivo:
                        print(x['proveedor'])
                        ordenNew   = OrdenDeCompra()  
                        num        = numeracion.objects.get(id = x['numeracion'])
                        tercero    = Terceros.objects.get(nombreComercial = x['proveedor'])
                        if x['formaPago'] == "CAJA MENOR":
                                formaPago  = FormaPago.objects.get(nombre = "CONTADO")
                        else:
                                formaPago  = FormaPago.objects.get(nombre = x['formaPago'])

                        usuario    = User.objects.get(id = 1)

                        # Asugnación de variables en general
                        ordenNew.numeracion        = num
                        ordenNew.consecutivo       = x['consecutivo']
                        ordenNew.prefijo           = num.prefijo
                        ordenNew.numero            = num.prefijo+'-'+str(x['consecutivo']).zfill(4)
                        ordenNew.proveedor         = tercero
                        ordenNew.fecha             = x['fecha']
                        ordenNew.usuario           = usuario
                        ordenNew.formaPago         = formaPago
                        # ordenNew.observacion       = orden['observacion']
                        ordenNew.subtotal          = x['subtotal']
                        ordenNew.iva               = x['iva']
                        ordenNew.retencion         = x['retencion']
                        ordenNew.descuento         = x['descuento']
                        ordenNew.ingresada         = x['ingresada']
                        ordenNew.total             = ordenNew.subtotal - ordenNew.descuento + ordenNew.iva - ordenNew.retencion

                        ordenNew.save()


                        detalle = []
                        for item in x['productos']:
                                p             = item['producto']
                                print(p)
                                prod          = Productos.objects.get(codigoDeBarra = p)
                                
                                # DETALLE 
                                d             = OrdenDetalle()
                                d.orden       = ordenNew
                                d.producto    = prod
                                d.cantidad    = item['cantidad']
                                d.valorUnidad = item['valorUnidad']   
                                if item['descuento'] == None or item['descuento'] == '':
                                   d.descuento   = 0
                                else: 
                                   d.descuento   = item['descuento']   
                                if item['iva'] == None or item['iva'] == '':
                                   d.iva   = 0
                                else:
                                   d.iva   = item['iva']
                                # Añade los datos al arreglo "Detalle"
                                detalle.append(d)

                        # Hace una inserción masiva a OrdenDetalle                                
                        OrdenDetalle.objects.bulk_create(detalle)

def setOrdenesDefaultFarmacVieja(archivo):
     
        with transaction.atomic():
                for x in archivo:
                        if x['consecutivo'] != 1071 and x['consecutivo'] != 291 :
                                print(x['consecutivo'])
                                print(x['proveedor'])
                                print(x['formaPago'])
                                ordenNew   = OrdenDeCompra()  
                                num        = numeracion.objects.get(id = x['numeracion'])
                                tercero    = Terceros.objects.get(nombreComercial = x['proveedor'])
                                if x['formaPago'] == "CAJA MENOR":
                                        formaPago  = FormaPago.objects.get(nombre = "CONTADO")
                                else:
                                        formaPago  = FormaPago.objects.get(nombre = x['formaPago'])

                                usuario    = User.objects.get(id = 1)

                                # Asugnación de variables en general
                                ordenNew.numeracion        = num
                                ordenNew.consecutivo       = x['consecutivo']
                                ordenNew.prefijo           = num.prefijo
                                ordenNew.numero            = x['consecutivo']
                                ordenNew.proveedor         = tercero
                                ordenNew.fecha             = x['fecha']
                                ordenNew.usuario           = usuario
                                ordenNew.formaPago         = formaPago
                                # ordenNew.observacion       = orden['observacion']
                                ordenNew.subtotal          = x['subtotal']
                                if 'iva' in x:
                                        ordenNew.iva               = x['iva']
                                else:
                                        ordenNew.iva               = 0
                                ordenNew.retencion         = x['retencion']
                                ordenNew.descuento         = x['descuento']
                                ordenNew.ingresada         = x['ingresada']
                                ordenNew.total             = ordenNew.subtotal - ordenNew.descuento + ordenNew.iva - ordenNew.retencion

                                ordenNew.save()


                                detalle = []
                                for item in x['productos']:
                                        p             = item['producto']
                                        prod          = Productos.objects.get(codigoDeBarra = p)
                                        
                                        # DETALLE 
                                        d             = OrdenDetalle()
                                        d.orden       = ordenNew
                                        d.producto    = prod
                                        d.cantidad    = item['cantidad']
                                        d.valorUnidad = item['valorUnidad']   
                                        if item['descuento'] == None or item['descuento'] == '':
                                                d.descuento   = 0
                                        else: 
                                                d.descuento   = item['descuento']   
                                        if item['iva'] == None or item['iva'] == '':
                                                d.iva   = 0
                                        else:
                                                d.iva   = item['iva']
                                        # Añade los datos al arreglo "Detalle"
                                        detalle.append(d)

                                # Hace una inserción masiva a OrdenDetalle                                
                                OrdenDetalle.objects.bulk_create(detalle)



def setIngresosDefaultFarmac(archivo):
        with transaction.atomic():
                for x in archivo:
                        # print(x)
                        NewIngreso = Ingreso()
                        num     = numeracion.objects.get(id = x['numeracion'])
                        orden   = OrdenDeCompra.objects.get(numero = x['orden'])


                        NewIngreso.numeracion        = num
                        NewIngreso.consecutivo       = x['consecutivo']
                        NewIngreso.prefijo           = num.prefijo
                        NewIngreso.numero            = num.prefijo+'-'+str(x['consecutivo']).zfill(4)
                        NewIngreso.factura           = x['factura']
                        NewIngreso.orden             = orden
                        NewIngreso.proveedor         = orden.proveedor
                        NewIngreso.fecha             = x['fecha']
                        NewIngreso.formaPago         = orden.formaPago
                        NewIngreso.usuario           = User.objects.get(pk=1)
                        NewIngreso.subtotal          = orden.subtotal
                        NewIngreso.iva               = orden.iva
                        NewIngreso.retencion         = orden.retencion
                        NewIngreso.descuento         = orden.descuento
                        NewIngreso.total             = orden.total

                        


  
                       

                        NewIngreso.save()
                     
                        detalleIngresosSave = []

                        for item in x['productos']:
                            
                                # SE OBTIENE EL PRODUCTO DEL DETALLE A RECORRER
                                productoParcial       = item['producto']

                                # SE CREA UN OBJETO IngresoDetalle PARA LUEGO SER LLENADO Y GUARDADO
                                ingresoDetalleObject  = IngresoDetalle()    

                               

                                # SE CONSULTA EL PRODUCTO A INGRESAR POR MEDIO DEL LA LLAVE PRIMARIA(ID)
                                product            = Productos.objects.get(codigoDeBarra = productoParcial)



                                # Añadiendo los datos de IngresoDetalle
                                ingresoDetalleObject.ingreso          = NewIngreso
                                ingresoDetalleObject.producto         = product
                                ingresoDetalleObject.cantidad         = item['cantidad']
                                ingresoDetalleObject.valorUnidad      = item['valorUnidad']
                                ingresoDetalleObject.lote             = item['lote']
                             
                                ingresoDetalleObject.fechaVencimiento = item['vence']
                                                    
                                if item['iva'] == None or item['iva'] == '':
                                        ingresoDetalleObject.iva = 0
                                else:
                                        ingresoDetalleObject.iva = item['iva']


                                if item['descuento'] == None or item['descuento'] == '':
                                        ingresoDetalleObject.descuento = 0
                                else:
                                        ingresoDetalleObject.descuento = item['descuento']


                                ingresoDetalleObject.subtotal = ingresoDetalleObject.valorUnidad * ingresoDetalleObject.cantidad
                                ingresoDetalleObject.total    = ingresoDetalleObject.subtotal + (ingresoDetalleObject.iva * ingresoDetalleObject.cantidad )- (ingresoDetalleObject.descuento * ingresoDetalleObject.cantidad )

                                ingresoDetalleObject.save()

                                detalleIngresosSave.append(ingresoDetalleObject)
                                 
                

                        if NewIngreso.iva > 0:
                                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                                        impuestoIngreso = ImpuestoIngreso()
                                        impuestoIngreso.ingreso    = NewIngreso
                                        impuestoIngreso.impuesto   = imp
                                        impuestoIngreso.procentaje = imp.porcentaje
                                        totalIva = 0
                                        totalBase = 0
                                        for item in detalleIngresosSave:
                                                if item.iva > 0:
                                                        totalBase += (item.valorUnidad -  item.descuento) * item.cantidad
                                                        totalIva += item.iva * item.cantidad
                                        impuestoIngreso.base       = totalBase
                                        impuestoIngreso.total      = totalIva    
                                        impuestoIngreso.save()


                        if NewIngreso.retencion > 0:


                                tercero = NewIngreso.proveedor
                                tercero.isRetefuente = True
                                tercero.save()

                                rtfProveedor = RetencionesProveedor()
                                

                                retencion = RetencionesProveedor.objects.filter(tercero = NewIngreso.proveedor.id)
                                # SE RECORRERÁ LA RETENCION EXISTENTE
                                for r in retencion:
                                        # VALIDARÁ SI EL PROVEEDOR TIENE UNA RETENCIÓN FIJA. EN CASO DE NO TENER UNA RETENCIÓN FIJA, EL SUBTOTAL DEBE SER MAYOR A LA BASE DE LA RETENCIÓN
                                        reteIngreso = RetencionIngreso()
                                        if r.fija:
                                                # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                                                reteIngreso.ingreso    = NewIngreso
                                                reteIngreso.retencion  = r.retencion
                                                reteIngreso.base       = NewIngreso.subtotal - NewIngreso.descuento
                                                reteIngreso.procentaje = r.retencion.porcentaje
                                                reteIngreso.total      = reteIngreso.base * reteIngreso.procentaje / 100
                                                # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                                                reteIngreso.save()
                                        else:
                                                if r.retencion.base > 0 and NewIngreso.subtotal >= r.retencion.base:
                                                        # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                                                        reteIngreso.ingreso    = NewIngreso
                                                        reteIngreso.retencion  = r.retencion 
                                                        reteIngreso.base       = NewIngreso.subtotal -  NewIngreso.descuento
                                                        reteIngreso.procentaje = r.retencion.porcentaje
                                                        reteIngreso.total      = reteIngreso.base * reteIngreso.procentaje / 100
                                                                # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                                                        reteIngreso.save()
        

def setIngresosDefaultFarmacViejo(archivo):
        with transaction.atomic():
                for x in archivo:
                        
                                # print(x['orden'])
                                NewIngreso = Ingreso()
                                num     = numeracion.objects.get(id = x['numeracion'])
                                if x['orden'] != 463:
                                        try:
                                                orden   = OrdenDeCompra.objects.filter(numero = x['orden'])

                                                if orden:
                                                        orden = orden[0]
                                                
                                                        
                                                        


                                                        NewIngreso.numeracion        = num
                                                        NewIngreso.consecutivo       = x['consecutivo']
                                                        NewIngreso.prefijo           = num.prefijo
                                                        NewIngreso.numero            = x['consecutivo']
                                                        NewIngreso.factura           = x['factura']
                                                        NewIngreso.orden             = orden
                                                        NewIngreso.proveedor         = orden.proveedor
                                                        NewIngreso.fecha             = x['fecha']
                                                        NewIngreso.formaPago         = orden.formaPago
                                                        NewIngreso.usuario           = User.objects.get(pk=1)
                                                        NewIngreso.subtotal          = orden.subtotal
                                                        NewIngreso.iva               = orden.iva
                                                        NewIngreso.retencion         = orden.retencion
                                                        NewIngreso.descuento         = orden.descuento
                                                        NewIngreso.total             = orden.total

                                                        


                                                        

                                                        NewIngreso.save()
                                                        # CuentaxP.save()

                                                        detalleIngresosSave = []

                                                        for item in x['productos']:
                                                        
                                                                # SE OBTIENE EL PRODUCTO DEL DETALLE A RECORRER
                                                                productoParcial       = item['producto']

                                                                # SE CREA UN OBJETO IngresoDetalle PARA LUEGO SER LLENADO Y GUARDADO
                                                                ingresoDetalleObject  = IngresoDetalle()    

                                                        

                                                                # SE CONSULTA EL PRODUCTO A INGRESAR POR MEDIO DEL LA LLAVE PRIMARIA(ID)
                                                                product            = Productos.objects.get(codigoDeBarra = productoParcial)



                                                                # Añadiendo los datos de IngresoDetalle
                                                                ingresoDetalleObject.ingreso          = NewIngreso
                                                                ingresoDetalleObject.producto         = product
                                                                ingresoDetalleObject.cantidad         = item['cantidad']
                                                                ingresoDetalleObject.valorUnidad      = item['valorUnidad']
                                                                ingresoDetalleObject.lote             = item['lote']
                                                        
                                                                ingresoDetalleObject.fechaVencimiento = item['vence']
                                                                                
                                                                if item['iva'] == None or item['iva'] == '':
                                                                        ingresoDetalleObject.iva = 0
                                                                else:
                                                                        ingresoDetalleObject.iva = item['iva']


                                                                if item['descuento'] == None or item['descuento'] == '':
                                                                        ingresoDetalleObject.descuento = 0
                                                                else:
                                                                        ingresoDetalleObject.descuento = item['descuento']


                                                                ingresoDetalleObject.subtotal = ingresoDetalleObject.valorUnidad * ingresoDetalleObject.cantidad
                                                                ingresoDetalleObject.total    = ingresoDetalleObject.subtotal + (ingresoDetalleObject.iva * ingresoDetalleObject.cantidad )- (ingresoDetalleObject.descuento * ingresoDetalleObject.cantidad )

                                                                ingresoDetalleObject.save()

                                                                detalleIngresosSave.append(ingresoDetalleObject)
                                                                
                                                

                                                        if NewIngreso.iva > 0:
                                                                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                                                                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                                                                        impuestoIngreso = ImpuestoIngreso()
                                                                        impuestoIngreso.ingreso    = NewIngreso
                                                                        impuestoIngreso.impuesto   = imp
                                                                        impuestoIngreso.procentaje = imp.porcentaje
                                                                        totalIva = 0
                                                                        totalBase = 0
                                                                        for item in detalleIngresosSave:
                                                                                if item.iva > 0:
                                                                                        totalBase += (item.valorUnidad -  item.descuento) * item.cantidad
                                                                                        totalIva += item.iva * item.cantidad
                                                                        impuestoIngreso.base       = totalBase
                                                                        impuestoIngreso.total      = totalIva    
                                                                        impuestoIngreso.save()


                                                        if NewIngreso.retencion > 0:


                                                                tercero = NewIngreso.proveedor
                                                                tercero.isRetefuente = True
                                                                tercero.save()

                                                                rtfProveedor = RetencionesProveedor()
                                                                

                                                                retencion = RetencionesProveedor.objects.filter(tercero = NewIngreso.proveedor.id)
                                                                # SE RECORRERÁ LA RETENCION EXISTENTE
                                                                for r in retencion:
                                                                        # VALIDARÁ SI EL PROVEEDOR TIENE UNA RETENCIÓN FIJA. EN CASO DE NO TENER UNA RETENCIÓN FIJA, EL SUBTOTAL DEBE SER MAYOR A LA BASE DE LA RETENCIÓN
                                                                        reteIngreso = RetencionIngreso()
                                                                        if r.fija:
                                                                                # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                                                                                reteIngreso.ingreso    = NewIngreso
                                                                                reteIngreso.retencion  = r.retencion
                                                                                reteIngreso.base       = NewIngreso.subtotal - NewIngreso.descuento
                                                                                reteIngreso.procentaje = r.retencion.porcentaje
                                                                                reteIngreso.total      = reteIngreso.base * reteIngreso.procentaje / 100
                                                                                # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                                                                                reteIngreso.save()
                                                                        else:
                                                                                if r.retencion.base > 0 and NewIngreso.subtotal >= r.retencion.base:
                                                                                        # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                                                                                        reteIngreso.ingreso    = NewIngreso
                                                                                        reteIngreso.retencion  = r.retencion 
                                                                                        reteIngreso.base       = NewIngreso.subtotal -  NewIngreso.descuento
                                                                                        reteIngreso.procentaje = r.retencion.porcentaje
                                                                                        reteIngreso.total      = reteIngreso.base * reteIngreso.procentaje / 100
                                                                                                # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                                                                                        reteIngreso.save()
                                                else:
                                                       print("No se encontró ninguna orden válida con el número especificado",x['orden'])
                                        except ObjectDoesNotExist:
                                                print("No se encontró ninguna orden válida con el número especificado",x['orden'])

                                        except Exception as e:
                                                # print(e,)
                                                raise ValueError(e,x['orden'],'rechazada')
                                
                

def setCxpDefaultFarmac(archivo):
        with transaction.atomic():
                c_x_p = []
                for x in archivo:
                        
                        
                        try:
                                ingreso   = Ingreso.objects.get(orden__numero = x['orden'])

                        

                                CuentaxP = CxPCompras()
                                CuentaxP.ingreso    = ingreso 
                                CuentaxP.proveedor  = ingreso.proveedor
                                CuentaxP.base       = x['base']
                                CuentaxP.iva        = x['iva']
                                CuentaxP.reteFuente = x['reteFuente'] 
                                CuentaxP.valorTotal = x['valorTotal'] 
                                CuentaxP.valorAbono = x['valorAbono'] 
                                CuentaxP.estado     = x['estado'] 
                                
                                CuentaxP.reteIca    = 0 

                                CuentaxP.save()


                                # if CuentaxP.iva > 0:
                

                                #         imp = Impuestos()
                                #         if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                                #                 imp = Impuestos.objects.get(nombre = "IVA (19%)")


                                #         ImpuestosEnGeneral.objects.create_impuesto(
                                #         tipo=ImpuestosEnGeneral.COMPRAS, 
                                #         doc_referencia=CuentaxP.ingreso.orden.numero, 
                                #         impuesto=imp, 
                                #         tercero = CuentaxP.ingreso.proveedor,
                                #         base= CuentaxP.iva / (19/100), 
                                #         porcentaje=imp.porcentaje, 
                                #         total=CuentaxP.iva, 
                                #         fecha=CuentaxP.fecha,
                                #         ventas=False,
                                #         compras=True
                                #         )

                                # if CuentaxP.reteFuente > 0:
                                

                                #         # RETEFUENTE = '06'
                                #         # ICA = '07
                                #         if CuentaxP.reteFuente > 0:
                                #                 r = Retenciones.objects.get(tipoRetencion = '06', porcentaje = 2.5)

                                #                 RetencionesEnGeneral.objects.create_retencion(
                                #                         tipo=RetencionesEnGeneral.COMPRAS, 
                                #                         doc_referencia=CuentaxP.ingreso.orden.numero, 
                                #                         retencion= r, 
                                #                         tercero = CuentaxP.ingreso.proveedor,                           
                                #                         base=CuentaxP.base, 
                                #                         porcentaje=r.porcentaje, 
                                #                         total=CuentaxP.reteFuente, 
                                #                         fecha=CuentaxP.fecha,
                                #                         ventas=False,
                                #                         compras=True
                                #                 )

                                                


                        except Exception as e:
                                print(e,x['orden'],'rechazada')

                                
        
                

        




def setInventarioDefault(archivo):
        

        with transaction.atomic():

                for x in archivo:
                        print(x)
                        iv = Inventario()
                        p = Productos.objects.get(codigoDeBarra = x['codigodebarra'])

                        
                        iv.estado = x['estado']
                        iv.idProducto = p
                        iv.bodega = p.bodega
                        iv.lote = x['Lote']
                        iv.unidades = x['Unidades']
                        iv.vencimiento = x['vence']
                        iv.valorCompra = x['Valorcompraunidad']

                        p.stock_inicial += iv.unidades

                        iv.save()


                        valor_compra = Inventario.obtener_valor_compra_mas_alto(id_producto=p.id, lote=iv.lote)
                        p.valorCompra = valor_compra

                        p.save()


def  setBalanceDefault(archivo):

        with transaction.atomic():
                print("empezo el proceso rey")
                lista= []
                for x in archivo:
                        # print(x)
                        k = Kardex()
                        try:
                                     p = Productos.objects.get(codigoDeBarra = x['codigodebarra'])
                        except:
                                print(x['codigodebarra'])

                        try:
                                t =  Terceros.objects.get(nombreComercial = x['tercero'])
                        except:
                                t =  Terceros.objects.get(nombreComercial = 'N/A')
                        
                        k.tipo = x['tipo']
                        if x['balance'] is not None and x['balance'] != 'NULL':
                                k.balance = int(x['balance'])
                        else:
                                k.balance = 0 
                        k.bodega = p.bodega
                        k.producto = p
                        k.precio = float(str(x['precio']).replace(',', '.'))
                        k.descripcion = x['decripcion']
                        if x['unidades'] is not None and x['unidades'] != 'NULL':
                                k.unidades = int(x['unidades'])
                        else:
                                k.unidades = 0 
                        k.fecha = x['fecha']
                        k.tercero = t
                        lista.append(k)
                print("proceso terminado mi compae")
                Kardex.objects.bulk_create(lista)     

                      


def setPagosDefault(archivo):
        with transaction.atomic():
        # Guardar en el modelo PagosCompras
                usuario    = User.objects.get(id = 1)

                num = numeracion.objects.get(id = 5)

                for data in archivo:
                        numero_split = data['numero'].split('-'),
                        cuenta = 0
                        numero_split = numero_split[0]
                        print(numero_split)

                        if 'cuenta' in data:
                                if data['cuenta']:
                                        cuenta=puc.objects.get(codigo = data['cuenta'])
                                else:
                                        cuenta=puc.objects.get(codigo = 110505)
                        else:
                                
                                cuenta=puc.objects.get(codigo = 110505)

                        pagos_compras = PagosCompras(
                                numeracion=num,
                                numero=data['numero'],


                                consecutivo=numero_split[0],
                                prefijo=numero_split[1],
                                tipoTransaccion=PagosCompras.CON_FACTURA,
                                usuario=usuario,
                                proveedor=Terceros.objects.get(nombreComercial = data['proveedor']),
                                fecha=data['fecha'],
                                cuenta = cuenta,
                                concepto=data['concepto'],
                                observacion=data['observacion'],
                        )
                        pagos_compras.save()

                        # Guardar en el modelo DetailPaymentInvoice
                        detalles_pago = data['facturas']
                        for detalle in detalles_pago:
                                print(detalle['orden'])
                                cxp = CxPCompras.objects.get(ingreso__orden__numero = detalle['orden'])

                                detail_payment_invoice = DetailPaymentInvoice(
                                        ingreso=cxp.ingreso,
                                        pago=pagos_compras,
                                        factura=cxp.factura,
                                        orden=cxp.ingreso.orden,
                                        cxpCompra=cxp,
                                        descuento=detalle['valorDescuento'],
                                        saldoAFavor=0,
                                        saldo=(cxp.valorTotal - cxp.valorAbono),
                                        totalAbono=detalle['valabono'],
                                        )
                                detail_payment_invoice.save()
                
                        # print(numero_split)


def rotacion_productos_x_compras(fecha_inicio,fecha_fin):

        fecha_inicio = '2023-05-1'
        fecha_fin    = '2023-05-31'


        proveedor_subquery = Terceros.objects.filter(
                ingreso_proveedor__ingreso_detalle__producto__id=OuterRef('id')
        ).order_by('-ingreso_proveedor__fecha').values('nombreComercial')[:1]


        cliente_subquery = Terceros.objects.filter(
                cliente_factura__detalle_factura__producto__id=OuterRef('id')
        ).order_by('-cliente_factura__fecha').values('nombreComercial')[:1]


        
        ultima_compra_subquery = Ingreso.objects.filter(
                ingreso_detalle__producto__id=OuterRef('id')
        ).order_by('-fecha').values('fecha')[:1]


        ultima_venta_subquery = CxcMovi.objects.filter(
                detalle_factura__producto__id=OuterRef('id')
        ).order_by('-fecha').values('fecha')[:1]




        query = Productos.objects.filter(
                ingreso_producto__ingreso__fecha__range=[fecha_inicio, fecha_fin]
        ).annotate(
        
                tipoDeProducto=F('tipoProducto__nombre')
        ).annotate(
                rotacion_compras=Coalesce(Sum('ingreso_producto__cantidad', filter=Q(ingreso_producto__ingreso__fecha__range=[fecha_inicio, fecha_fin])), 0),
                rotacion_x_ventas=Coalesce(Sum('cxcmovidetalle__cantidad', filter=Q(cxcmovidetalle__factura__fecha__range=[fecha_inicio, fecha_fin])), 0),
                existencia=Coalesce(Sum('inventario_producto__unidades', output_field=IntegerField()), 0),
                num_lotes=Coalesce(Count('inventario_producto__lote',filter=Q(inventario_producto__lote__gt=0), output_field=IntegerField()), 0),
                ultima_compra=Subquery(ultima_compra_subquery),
                proveedor=Subquery(proveedor_subquery),
                ultima_venta=Subquery(ultima_venta_subquery),
                cliente=Value(''),  # Reemplaza con el valor deseado
        ).values(
                'codigoDeBarra',
                'nombreymarcaunico',
                'laboratorio',
                'tipoDeProducto',
                'rotacion_compras',
                'rotacion_x_ventas',
                'existencia',
                'num_lotes',
                'ultima_compra',
                'proveedor',
                'ultima_venta',
                'cliente',
        ).order_by('nombreymarcaunico')

        return query





def consultar_retenciones(fecha_inicio, fecha_final):
    retenciones = RetencionesEnGeneral.objects.filter(
        fecha__range=(fecha_inicio, fecha_final),
        compras=True
    ).exclude(tipo=RetencionesEnGeneral.DEVOLUCION).values(
        'retencion__nombre', 'tercero__nombreComercial'
    ).annotate(
        suma_bases=Sum('base'),
        suma_retenciones=Sum('total')
    )

    devoluciones_rtf = RetencionesEnGeneral.objects.filter(
        fecha__range=(fecha_inicio, fecha_final),
        compras=True,
        tipo=RetencionesEnGeneral.DEVOLUCION
    ).values(
        'retencion__nombre', 'tercero__nombreComercial'
    ).annotate(
        suma_bases=Sum('base'),
        suma_retenciones=Sum('total')
    )

    resultado_dict = {
        "fecha_inicio": fecha_inicio,
        "fecha_final": fecha_final,
        "resultados": {
            "retenciones": []
        },
        "total_bases": 0.0,
        "total_retenciones": 0.0
    }

    total_bases = 0.0
    total_retenciones = 0.0

    for resultado in retenciones:
        retencion_nombre = resultado["retencion__nombre"]
        tercero_nombre = resultado["tercero__nombreComercial"]
        base = resultado["suma_bases"]
        retencion = resultado["suma_retenciones"]

        detalle_retencion = {
            "tercero": tercero_nombre,
            "base": base,
            "retencion": retencion
        }

        retencion_encontrada = False

        # Buscar si la retención ya está en la lista de retenciones
        for retencion_actual in resultado_dict["resultados"]["retenciones"]:
            if retencion_actual["nombre"] == retencion_nombre:
                retencion_actual["detalle"].append(detalle_retencion)
                retencion_encontrada = True
                break

        # Si la retención no está en la lista, se agrega como nueva
        if not retencion_encontrada:
            nueva_retencion = {
                "nombre": retencion_nombre,
                "detalle": [detalle_retencion]
            }
            resultado_dict["resultados"]["retenciones"].append(nueva_retencion)

        total_bases += base
        total_retenciones += retencion

    for resultado in devoluciones_rtf:
        retencion_nombre = "DEV " + resultado["retencion__nombre"]
        tercero_nombre = resultado["tercero__nombreComercial"]
        base = resultado["suma_bases"] * -1  # Valor negativo
        retencion = resultado["suma_retenciones"] * -1  # Valor negativo

        detalle_devolucion = {
            "tercero": tercero_nombre,
            "base": base,
            "retencion": retencion
        }

        devolucion_encontrada = False

        # Buscar si la devolución ya está en la lista de retenciones
        for retencion_actual in resultado_dict["resultados"]["retenciones"]:
            if retencion_actual["nombre"] == retencion_nombre:
                retencion_actual["detalle"].append(detalle_devolucion)
                devolucion_encontrada = True
                break

        # Si la devolución no está en la lista, se agrega como nueva devolución
        if not devolucion_encontrada:
            nueva_devolucion = {
                "nombre": retencion_nombre,
                "detalle": [detalle_devolucion]
            }
            resultado_dict["resultados"]["retenciones"].append(nueva_devolucion)

        total_bases += base
        total_retenciones += retencion

    resultado_dict["total_bases"] = total_bases
    resultado_dict["total_retenciones"] = total_retenciones

    return resultado_dict



def crear_ajuste_desde_json(json_data,entradas,salidas,usuario):
    try:
        data = json_data

        # Procesa los datos JSON y crea un nuevo ajuste
        numeracion_id = data.get('numeracion')
        observacion = data.get('observacion')

        num     = numeracion.objects.get(id = numeracion_id)
        print(num.nombre)
 
       
        # Crea un nuevo ajuste
        ajuste:AjusteStock = AjusteStock()


        ajuste.numeracion        = num
        ajuste.consecutivo       = num.proximaFactura
        ajuste.prefijo           = num.prefijo
        ajuste.numero            = num.prefijo+'-'+str(num.proximaFactura).zfill(4)
        
        print(f'Usuario actual: {usuario.username} ({usuario.id})')
        ajuste.usuario = usuario
        ajuste.observacion = observacion
        print(ajuste)

        
    
        with transaction.atomic():
                ajuste.save()
                proveedor = Terceros.objects.get(nombreComercial = 'N/A')
                # Procesa los detalles
                listadoDetalle = []
                
                for detalle_data in salidas:
                        producto = detalle_data.get('producto')
                        tipoAjuste = detalle_data.get('tipoAjuste')

                        producto =  Productos.objects.get(id= producto['id'])


                        cantidad = detalle_data.get('cantidad')
                        costo = detalle_data.get('costo')
                        lote = detalle_data.get('lote')
                        fecha_vencimiento = detalle_data.get('fechaVencimiento').rstrip('Z')
                        
                        existencia = detalle_data.get('existencia')
                        
                   

                        detalle =AjusteDetalle()

                        detalle.ajuste           = ajuste
                        detalle.producto         = producto
                        detalle.cantidad         = int(cantidad)
                        detalle.costo            = float(costo)
                        detalle.isSalida         = True
                        detalle.tipoAjuste       = tipoAjuste
                        detalle.lote             = lote
                        detalle.existencia       = existencia
                        fecha_obj = datetime.fromisoformat(fecha_vencimiento)
                        detalle.fechaVencimiento = fecha_obj.date()
                        detalle.total            = detalle.costo * detalle.cantidad


                        
                        producto.stock_inicial -=  int(detalle.cantidad)
                        kardexObject          = Kardex()
                                # Ahora se llama los datos del kardex a registrar
                        kardexObject.descripcion = 'Ajuste No. '+ajuste.numero
                        kardexObject.tipo        = 'AJU'
                        kardexObject.producto    = detalle.producto
                        kardexObject.tercero     = proveedor
                        kardexObject.bodega      = detalle.producto.bodega
                        kardexObject.unidades    = (0 - detalle.cantidad)
                        kardexObject.balance     = detalle.producto.stock_inicial
                        kardexObject.precio      = detalle.costo

                        # Guarda los kardex de los productos
                        kardexObject.save()

                        # validando el inventario
                        if Inventario.objects.filter(
                                idProducto  = detalle.producto.id,
                                lote        = detalle.lote
                                ).exists():

                                # SE OBTIENE EL PRODUCTO PARA ACTUALIZAR SU CANTIDAD EN EL INVENTARIO
                                inv = Inventario.objects.get(
                                        idProducto  = detalle.producto.id,
                                        lote        = detalle.lote)


                                

                                # SE ACTUALIZA EL INVENTARIO
                                inv.unidades -=  int(detalle.cantidad)
                
                                inv.save()

                                

                                producto.valorCompra = detalle.costo

                        producto.save()
                        detalle.save()


                for detalle_data in entradas:

                        producto = detalle_data.get('producto')
                        tipoAjuste = detalle_data.get('tipoAjuste')

                        producto =  Productos.objects.get(id= producto['id'])
                        cantidad = detalle_data.get('cantidad')
                        costo = detalle_data.get('costo')
                        lote = detalle_data.get('lote')
                        fecha_vencimiento = detalle_data.get('fechaVencimiento').rstrip('Z')
                        existencia = detalle_data.get('existencia')
                       

                        detalle =AjusteDetalle()

                        detalle.ajuste           = ajuste
                        detalle.tipoAjuste       = tipoAjuste
                        detalle.producto         = producto
                        detalle.cantidad         = int(cantidad)
                        detalle.costo            = float(costo)
                        detalle.lote             = lote
                        detalle.isEntrada        = True
                        detalle.existencia       = existencia
                        fecha_obj = datetime.fromisoformat(fecha_vencimiento)
                        detalle.fechaVencimiento = fecha_obj.date()
                        detalle.total            = detalle.costo * detalle.cantidad


                      
                        producto.stock_inicial += int(detalle.cantidad)
                        kardexObject          = Kardex()
                                # Ahora se llama los datos del kardex a registrar
                        kardexObject.descripcion = 'Ajuste No. '+ajuste.numero
                        kardexObject.tipo        = 'AJU'
                        kardexObject.producto    = detalle.producto
                        kardexObject.tercero     = proveedor
                        kardexObject.bodega      = detalle.producto.bodega
                        kardexObject.unidades    = detalle.cantidad
                        kardexObject.balance     = detalle.producto.stock_inicial
                        kardexObject.precio      = detalle.costo

                        # Guarda los kardex de los productos
                        kardexObject.save()

                        # validando el inventario
                        if Inventario.objects.filter(
                                idProducto  = detalle.producto.id,
                                lote        = detalle.lote
                                ).exists():

                                # SE OBTIENE EL PRODUCTO PARA ACTUALIZAR SU CANTIDAD EN EL INVENTARIO
                                inv = Inventario.objects.get(
                                        idProducto  = detalle.producto.id,
                                        lote        = detalle.lote)


                                

                                # SE ACTUALIZA EL INVENTARIO
                                inv.unidades +=  int(detalle.cantidad)
                
                                inv.save()

                                

                                producto.valorCompra = Inventario.obtener_valor_compra_mas_alto(id_producto=producto.id, lote=detalle.lote)



                                
                                

                        else:
                                # Registra nuevo producto en el inventario
                                newProductInv = Inventario()

                                # Se agisnan los datos
                                newProductInv.bodega      = detalle.producto.bodega
                                newProductInv.idProducto  = detalle.producto
                                newProductInv.vencimiento = detalle.fechaVencimiento
                                newProductInv.valorCompra = detalle.costo
                                newProductInv.unidades    = detalle.cantidad
                                newProductInv.lote        = detalle.lote
                                newProductInv.estado      = True                                             
                                

                                # Guarda los datos
                                newProductInv.save()
                                producto.valorCompra = detalle.costo
                                      


                      



                                

                        producto.save()

                        detalle.save()
                        listadoDetalle.append(detalle)




              
                        

                producto.save()

                detalle.save()
                listadoDetalle.append(detalle)





                # ContaAjuste = contabilizar_ajuste(ajuste, listadoDetalle,proveedor)    

                # asiento = ContaAjuste['asiento']
                # detalleConta = ContaAjuste['detalle']
                # validarContabilidad(detalleConta)
                # asiento.save()
                # for x in detalleConta:
                #         x.save()
                num.proximaFactura += 1
                num.save()

                
                return f'Ajuste N° {ajuste.numero} registrado correctamente'
    except Exception as e:
        return f'Error al registrar el ajuste: {str(e)}'





def contabilizar_ajuste(ajuste:AjusteStock,detalle,tercero):
        empresa = Empresa.objects.get(id = 1)


        movi = asiento()
        movi.numero       =  ajuste.numero
        movi.fecha        =  ajuste.fecha
        movi.empresa      =  empresa
        movi.tipo         =  'AJU'
        if ajuste.tipoAjuste != ajuste.SALIDA_POR_AVERIA_O_VENCIMIENTO:
                movi.concepto     =  "Entrada de inventario según Ajuste N°: "+ str(ajuste.numero)
        else:
                movi.concepto     =  "Salida de inventario según Ajuste N°: "+ str(ajuste.numero)
               
        movi.usuario      =  ajuste.usuario
        movi.totalDebito  = 0
        movi.totalCredito = 0
        movi.docReferencia = ajuste.numero
        listaDetalleAsiento = []




                

        tiposDeMercancia = dict()
        for x in detalle:
                if x.producto.tipoProducto.nombre in tiposDeMercancia:
                        nombre = x.producto.tipoProducto.nombre
                        tiposDeMercancia[nombre].valor += x.costo 
                else:
                        nombre = x.producto.tipoProducto.nombre

                        objecto:tiposMercancia = tiposMercancia(x.producto.tipoProducto,x.producto.tipoProducto.c_tipo,x.costo)

                        tiposDeMercancia[nombre] = objecto
                
        if ajuste.tipoAjuste != ajuste.SALIDA_POR_AVERIA_O_VENCIMIENTO:
                
                if ajuste.tipoAjuste == ajuste.ENTRADA_POR_SOBRANTES:
                        for j in tiposDeMercancia:
                                detalle_debito = asientoDetalle()

                                detalle_debito.asiento  = movi
                                detalle_debito.tercero  = tercero
                                detalle_debito.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipo
                                detalle_debito.concepto =  movi.concepto
                                detalle_debito.docReferencia = movi.docReferencia
                                detalle_debito.tipo         =  'AJU'
                                detalle_debito.debito   = tiposDeMercancia[j].valor
                                listaDetalleAsiento.append(detalle_debito)


                                detalle_credito = asientoDetalle()

                                detalle_credito.asiento  = movi
                                detalle_credito.tercero  = tercero
                                detalle_credito.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_ingreso
                                detalle_credito.concepto =  movi.concepto
                                detalle_credito.docReferencia = movi.docReferencia
                                detalle_credito.tipo         =  'AJU'
                                detalle_credito.credito   = tiposDeMercancia[j].valor
                                listaDetalleAsiento.append(detalle_credito)
                else:
                        for j in tiposDeMercancia:
                                detalle_debito = asientoDetalle()

                                detalle_debito.asiento  = movi
                                detalle_debito.tercero  = tercero
                                detalle_debito.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipo
                                detalle_debito.concepto =  movi.concepto
                                detalle_debito.docReferencia = movi.docReferencia
                                detalle_debito.tipo         =  'AJU'
                                detalle_debito.debito   = tiposDeMercancia[j].valor
                                listaDetalleAsiento.append(detalle_debito)


                                detalle_credito = asientoDetalle()

                                detalle_credito.asiento  = movi
                                detalle_credito.tercero  = tercero
                                detalle_credito.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipo
                                detalle_credito.concepto =  movi.concepto
                                detalle_credito.docReferencia = movi.docReferencia
                                detalle_credito.tipo         =  'AJU'
                                detalle_credito.credito   = tiposDeMercancia[j].valor
                                listaDetalleAsiento.append(detalle_credito)
        else:
               
                for j in tiposDeMercancia:
                        detalle_debito = asientoDetalle()

                        detalle_debito.asiento  = movi
                        detalle_debito.tercero  = tercero
                        detalle_debito.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_gasto
                        detalle_debito.concepto =  movi.concepto
                        detalle_debito.docReferencia = movi.docReferencia
                        detalle_debito.tipo         =  'AJU'
                        detalle_debito.debito   = tiposDeMercancia[j].valor
                        listaDetalleAsiento.append(detalle_debito)


                        detalle_credito = asientoDetalle()

                        detalle_credito.asiento  = movi
                        detalle_credito.tercero  = tercero
                        detalle_credito.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipoS
                        detalle_credito.concepto =  movi.concepto
                        detalle_credito.docReferencia = movi.docReferencia
                        detalle_credito.tipo         =  'AJU'
                        detalle_credito.credito   = tiposDeMercancia[j].valor
                        listaDetalleAsiento.append(detalle_credito)
        
        resultado = dict()
        resultado["asiento"] = movi
        resultado["detalle"] = listaDetalleAsiento


       


        return resultado



#ws

def actualizar_productos():
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        channel_layer.send("productos", {
                "type": "update.producto",
                "data": "Hello there!",
        })
        print("eVIADO")    