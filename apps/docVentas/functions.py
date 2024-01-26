from rest_framework import serializers
from django.db import transaction
from .validations import *
from .models import *
from apps.configuracion.models import *
from apps.stock.models import *
from apps.contabilidad.functions import EliminarAsiento, obtener_asiento
from apps.contabilidad.models import puc, asiento,asientoDetalle,CuentaNecesaria
from django.db.models import Q
from .interfaces import tiposMercancia,GenerateRequestFE,GenerateRequestNC
from datetime import date, timedelta

import requests    
import base64
import xmltodict
import json


def listadoProformas():
    obj = {}
    return CxcMovi.filter_by_criterio_proformas(obj)

def listadoFacturas():
    obj = {}
    return CxcMovi.filter_by_criterio_ventas(obj)

def listadoCotizaciones():
    obj = {}
    return NuevaCotizacion.filter_by_criterio_cotizaciones(obj)




def saveProformasAFactura(data,usuario):
    ValidarConversionProformas(data)
    return CxcMovi.convertir_proformas_a_factura(data,usuario)



def getFactura(id):
    cxc = CxcMovi.objects.select_related(
        'numeracion',
        'cliente',
        'formaPago',
        'vendedor',
        'usuario',
        ).prefetch_related('detalle_factura').get(id = id)
    return cxc

def getInvoce(id):
    cxc = CxcMovi.objects.select_related(
        'numeracion',
        'cliente',
        'formaPago',
        'vendedor',
        'usuario',
        ).prefetch_related('detalle_factura','impuesto_cxc','retencion_cxc').get(id = id)
    return cxc

def getCotizacion(id):
    cot = NuevaCotizacion.objects.select_related(
        'numeracion',
        'cliente',
        'formaPago',
        'vendedor',
        'usuario',
        ).prefetch_related('factura_cotizacion').get(id = id)
    return cot



def saveDocCotizacion(create,docVenta,detalle,usuario):
    newVenta = NuevaCotizacion()
    
    if create:
        # SE HACE EL LLAMADO A LA TABLA NUMERACION, PARA LA RELACIÓN CON LA VENTA
        num       = numeracion.objects.get(id = docVenta['numeracion'])
        cliente   = Terceros.objects.get(id   = docVenta['cliente'])
        formaPago = FormaPago.objects.get(id  = docVenta['formaPago'])
        vendedor  = VendedoresClientes.objects.get(id  = docVenta['vendedor'])
        


        newVenta.numeracion      = num
        newVenta.consecutivo     = num.proximaFactura
        newVenta.prefijo         = num.prefijo
        newVenta.numero          = num.prefijo+'-'+str(num.proximaFactura).zfill(4)
        newVenta.cliente         = cliente
        newVenta.formaPago       = formaPago
        newVenta.fecha           = date.today()
        newVenta.observacion     = docVenta['observacion']
        newVenta.valorLetras     = ""
        newVenta.vendedor        = vendedor
        newVenta.usuario         = usuario
        newVenta.subtotal        = docVenta['subtotal']
        newVenta.valorReteFuente = docVenta['valorRetenciones']
        newVenta.valorDomicilio  = docVenta['valorDomicilio']
        newVenta.valorIva        = docVenta['valorIva']
        newVenta.descuento       = docVenta['descuento']
        newVenta.valor           = docVenta['valor']
        newVenta.valor           += newVenta.valorDomicilio


        with transaction.atomic():
            newVenta.save()

            detalleFacturaSave = []
            for item in detalle:
                productoParcial      = item['producto']
                facturaDetalleObject = NuevaCotizacionDetalle() 
                kardexObject         = Kardex()
                product              = Productos.objects.get(id = productoParcial['id'])

                facturaDetalleObject.factura          = newVenta
                facturaDetalleObject.producto         = product
                facturaDetalleObject.cantidad         = item['cantidad']
                facturaDetalleObject.valor            = item['valor']
                facturaDetalleObject.valorCompra      = item['valorCompra']
                facturaDetalleObject.lote             = item['lote']
                
                # facturaDetalleObject.vence            = item['vence']

                if item['iva'] == None or item['iva'] == '':
                        facturaDetalleObject.iva = 0
                else:
                        facturaDetalleObject.iva = item['iva']
                
                if item['descuento'] == None or item['descuento'] == '':
                        facturaDetalleObject.descuento = 0
                else:
                        facturaDetalleObject.descuento = item['descuento']
                
                facturaDetalleObject.subtotal = item['subtotal']
                facturaDetalleObject.total    = item['total']

                facturaDetalleObject.save()

                detalleFacturaSave.append(facturaDetalleObject)

            num.proximaFactura += 1
            num.save()

def saveDocVenta(create,docVenta,detalle,usuario):
    newVenta = CxcMovi()
    newCxc   = CxcVentas()
    if create:
        # SE HACE EL LLAMADO A LA TABLA NUMERACION, PARA LA RELACIÓN CON LA VENTA
        num       = numeracion.objects.get(id = docVenta['numeracion'])
        cliente   = Terceros.objects.get(id   = docVenta['cliente'])
        formaPago = FormaPago.objects.get(id  = docVenta['formaPago'])
        vendedor  = VendedoresClientes.objects.get(id  = docVenta['vendedor'])
        


        newVenta.numeracion      = num
        newVenta.consecutivo     = num.proximaFactura
        newVenta.prefijo         = num.prefijo
        newVenta.numero          = num.prefijo+'-'+str(num.proximaFactura).zfill(4)
        newVenta.cliente         = cliente
        newVenta.formaPago       = formaPago
        newVenta.fecha           = date.today()
        newVenta.observacion     = docVenta['observacion']
        newVenta.valorLetras     = ""
        newVenta.vendedor        = vendedor
        newVenta.usuario         = usuario
        newVenta.subtotal        = docVenta['subtotal']
        newVenta.valorReteFuente = docVenta['valorRetenciones']
        newVenta.valorDomicilio  = docVenta['valorDomicilio']
        newVenta.valorIva        = docVenta['valorIva']
        newVenta.descuento       = docVenta['descuento']
        newVenta.valor           = docVenta['valor']
        newVenta.valor           += newVenta.valorDomicilio


        with transaction.atomic():
            if num.tipoDocumento == numeracion.FACTURA_ELECTRONICA: 
                newVenta.isElectronica = True
            newVenta.save()

            if newVenta.valorReteFuente > 0:
                retencion = RetencionesClientes.objects.filter(tercero__id = cliente.id)
                for r in retencion:
                    reteFac = RetencionCxc()
                    if r.fija:
                        reteFac.factura    = newVenta
                        reteFac.retencion  = r.retencion
                        reteFac.base       = newVenta.subtotal - newVenta.descuento
                        reteFac.procentaje = r.retencion.porcentaje
                        reteFac.total      = reteFac.base * reteFac.procentaje / 100
                        # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                        reteFac.save()
                    else:
                        if r.retencion.base > 0 and (newVenta.subtotal - newVenta.descuento) >= r.retencion.base:
                            # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                            reteFac.factura    = newVenta
                            reteFac.retencion  = r.retencion 
                            reteFac.base       = newVenta.subtotal -  newVenta.descuento
                            reteFac.procentaje = r.retencion.porcentaje
                            reteFac.total      = reteFac.base * reteFac.procentaje / 100
                            # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                            reteFac.save()
        
            
           

            detalleFacturaSave = []
            for item in detalle:
                productoParcial      = item['producto']
                facturaDetalleObject = CxcMoviDetalle() 
                kardexObject         = Kardex()
                product              = Productos.objects.get(id = productoParcial['id'])

                ValidarInventario(product,item['lote'],item['cantidad'])
                facturaDetalleObject.factura          = newVenta
                facturaDetalleObject.producto         = product
                facturaDetalleObject.cantidad         = item['cantidad']
                facturaDetalleObject.valor            = item['valor']
                facturaDetalleObject.valorCompra      = item['valorCompra']
                facturaDetalleObject.lote             = item['lote']
                
                facturaDetalleObject.vence            = item['vence']

                if item['iva'] == None or item['iva'] == '':
                        facturaDetalleObject.iva = 0
                else:
                        facturaDetalleObject.iva = item['iva']
                
                if item['descuento'] == None or item['descuento'] == '':
                        facturaDetalleObject.descuento = 0
                else:
                        facturaDetalleObject.descuento = item['descuento']
                
                facturaDetalleObject.subtotal = item['subtotal']
                facturaDetalleObject.total    = item['total']

                facturaDetalleObject.save()

                detalleFacturaSave.append(facturaDetalleObject)

                if num.tipoDocumento == num.PROFORMA:
                    kardexObject.descripcion = 'Profoma No. '+facturaDetalleObject.factura.numero
                    kardexObject.tipo        = 'PF'
                else:
                    kardexObject.descripcion = 'Factura No. '+facturaDetalleObject.factura.numero
                    kardexObject.tipo        = 'FA'
                
                
                kardexObject.producto    = facturaDetalleObject.producto
                kardexObject.tercero     = facturaDetalleObject.factura.cliente
                kardexObject.bodega      = facturaDetalleObject.producto.bodega
                kardexObject.unidades    = 0 - facturaDetalleObject.cantidad
                kardexObject.balance     = facturaDetalleObject.producto.stock_inicial - facturaDetalleObject.cantidad
                kardexObject.precio      = facturaDetalleObject.valor

                kardexObject.save()

                if Inventario.objects.filter(
                    idProducto  = facturaDetalleObject.producto.id,
                    lote        = facturaDetalleObject.lote
                    ).exists():

                    # SE OBTIENE EL PRODUCTO PARA ACTUALIZAR SU CANTIDAD EN EL INVENTARIO
                    producto = Inventario.objects.get(
                            idProducto  = facturaDetalleObject.producto.id,
                            lote        = facturaDetalleObject.lote)


                    

                    # SE ACTUALIZA EL INVENTARIO
                    producto.unidades -=  facturaDetalleObject.cantidad
                    producto.save()

                    # SE ACTUALIZA EL PARAMETRO STOCK EN EL PRODUCTO
                    product.stock_inicial -= facturaDetalleObject.cantidad
                    product.save()

            if newVenta.valorIva > 0:
                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                        impFactura = ImpuestoCxc()
                        impFactura.factura    = newVenta
                        impFactura.impuesto   = imp
                        impFactura.procentaje = imp.porcentaje
                        totalIva = 0
                        totalBase = 0
                        for item in detalleFacturaSave:
                                if item.iva > 0:
                                        totalIva += item.iva * item.cantidad
                                        totalBase += (float(item.valor) -  float(item.descuento)) * item.cantidad
                        impFactura.base       = totalBase
                        impFactura.total      = totalIva    
                        impFactura.save()

            if num.tipoDocumento != numeracion.PROFORMA: 
                newCxc.cxc              = newVenta
                newCxc.factura          = newVenta.numero
                newCxc.formaPago        = newVenta.formaPago
                newCxc.fecha            = newVenta.fecha
                newCxc.fechaVencimiento = newVenta.fechaVencimiento
                newCxc.observacion      = newVenta.observacion
                newCxc.cliente          = newVenta.cliente
                newCxc.base             = newVenta.subtotal
                newCxc.iva              = newVenta.valorIva
                newCxc.valorDescuento   = newVenta.descuento
                newCxc.reteFuente       = newVenta.valorReteFuente
                newCxc.valorTotal       = newVenta.valor

                newCxc.save()

                contabilizarFacturas(newVenta,detalleFacturaSave)

            num.proximaFactura += 1
            num.save()
            return newVenta.numero
    else:
        
        updateCxc   = CxcVentas()
        updateVenta = CxcMovi.objects.get(id = docVenta['id'])
        num = updateVenta.numeracion
        if num.tipoDocumento != numeracion.PROFORMA:
            updateCxc = CxcVentas.objects.get(cxc__id = updateVenta.id)
            if updateCxc.valorAbono > 0:
                raise serializers.ValidationError('La factura tiene un pago, imposible actualizar')

        cliente     = Terceros.objects.get(id   = docVenta['cliente'])
        formaPago   = FormaPago.objects.get(id  = docVenta['formaPago'])


        updateVenta.vendedor       = cliente.vendedor
        updateVenta.formaPago      = formaPago
        updateVenta.cliente        = cliente       
        updateVenta.fecha          = date.today()
        updateVenta.valorDomicilio = docVenta['valorDomicilio']
        updateVenta.valor          = docVenta['valor']
        updateVenta.observacion    = docVenta['observacion']
        updateVenta.valor += updateVenta.valorDomicilio




        

        with transaction.atomic():
            if updateVenta.numeracion.tipoDocumento == numeracion.PROFORMA:
                descripcion = 'Profoma No. '+updateVenta.numero
                tipo        = 'PF'
                kardex =  Kardex.objects.filter(descripcion = descripcion, tipo = tipo)
                kardex.update(tercero = cliente)
                
                updateVenta.save()
            else:
                descripcion = 'Factura No. '+updateVenta.numero
                tipo        = 'FA'
                kardex =  Kardex.objects.filter(descripcion = descripcion, tipo = tipo)
                kardex.update(tercero = cliente)

                detalleVenta = CxcMoviDetalle.objects.filter(factura__id = updateVenta.id)
                
              
                updateCxc.factura          = updateVenta.numero
                updateCxc.formaPago        = updateVenta.formaPago
                updateCxc.fecha            = updateVenta.fecha
                updateCxc.fechaVencimiento = updateVenta.fechaVencimiento
                updateCxc.observacion      = updateVenta.observacion
                updateCxc.cliente          = updateVenta.cliente
                updateCxc.base             = updateVenta.subtotal
                updateCxc.iva              = updateVenta.valorIva
                updateCxc.valorDescuento   = updateVenta.descuento
                updateCxc.reteFuente       = updateVenta.valorReteFuente
                updateCxc.valorTotal       = updateVenta.valor
                
                updateVenta.save()
                updateCxc.save()
                contabilizarFacturas(updateVenta,detalleVenta)
            
            
            return updateVenta.numero
                
       

def DespacharFactura(numero:str):
    cxc =  CxcMovi.objects.get(numero = numero)

    if cxc.despachado: 
        cxc.despachado = False
    else:
        cxc.despachado = True
    cxc.save()

def eliminarProducto(id):
    with transaction.atomic():
        kardexObject         = Kardex()

        cxcDetalle = CxcMoviDetalle.objects.get(id = id)
        cxc = CxcMovi.objects.get(id = cxcDetalle.factura.id)

        if cxc.numeracion.tipoDocumento != numeracion.PROFORMA:
            if cxc.enviadaDian:
                raise serializers.ValidationError('Imposible actualizar, la factura ya fue enviada a la dian')
                

            valor =  CxcVentas.objects.get(cxc__id  = cxc.id).valorAbono
            if valor > 0:
      
                raise serializers.ValidationError('Imposible actualizar, la factura y tiene un pago')


        cantidad  = cxcDetalle.cantidad
        descuento = cxcDetalle.descuento * cantidad
        iva       = cxcDetalle.iva * cantidad
        subtotal  = cxcDetalle.subtotal
        total     = cxcDetalle.total

        if cxc.valorIva > 0:
            cxc.valorIva -= iva
            imp = ImpuestoCxc.objects.filter(factura__id = cxc.id)
            for x in imp:
                x.base -= (subtotal-descuento )
                x.total -= iva
                if x.total <= 0:
                    x.delete()
                else: 
                    x.save()
        if cxc.valorReteFuente > 0:
            rtf = RetencionCxc.objects.filter(factura__id = cxc.id)
            for x in rtf:
                base    = (subtotal-descuento)
                importe = base * x.procentaje / 100
                x.base  -= base
                x.total -= importe
                cxc.valorReteFuente -= importe
                cxc.valor           += importe
                if x.total <= 0:
                    x.delete()
                else:
                    x.save()
        
        cxc.subtotal  -= subtotal 
        cxc.descuento -= descuento
        cxc.valor     -= total
    
        if cxc.numeracion.tipoDocumento == numeracion.PROFORMA:
            kardexObject.descripcion = 'Profoma No. '+cxc.numero
            kardexObject.tipo        = 'PF'
        else:
            kardexObject.descripcion = 'Factura No. '+cxc.numero
            kardexObject.tipo        = 'FA'
        
        
        kardexObject.producto    = cxcDetalle.producto
        kardexObject.tercero     = cxcDetalle.factura.cliente
        kardexObject.bodega      = cxcDetalle.producto.bodega
        kardexObject.unidades    = cxcDetalle.cantidad
        kardexObject.balance     = cxcDetalle.producto.stock_inicial + cxcDetalle.cantidad
        kardexObject.precio      = cxcDetalle.valor

        kardexObject.save()

        if Inventario.objects.filter(
            idProducto  = cxcDetalle.producto.id,
            lote        = cxcDetalle.lote,
            
            ).exists():

            # SE OBTIENE EL PRODUCTO PARA ACTUALIZAR SU CANTIDAD EN EL INVENTARIO
            producto = Inventario.objects.get(
                    idProducto  = cxcDetalle.producto.id,
                    lote        = cxcDetalle.lote)


            

            # SE ACTUALIZA EL INVENTARIO
            producto.unidades +=  cxcDetalle.cantidad
            producto.save()

            # SE ACTUALIZA EL PARAMETRO STOCK EN EL PRODUCTO
            cxcDetalle.producto.stock_inicial += cxcDetalle.cantidad
            cxcDetalle.producto.save()
            cxcDetalle.delete()
            cxc.save()
            if cxc.numeracion.tipoDocumento != numeracion.PROFORMA:
                
                cxcVenta = CxcVentas.objects.get(cxc__id = cxc.id)

                cxcVenta.base             = cxc.subtotal
                cxcVenta.iva              = cxc.valorIva
                cxcVenta.valorDescuento   = cxc.descuento
                cxcVenta.reteFuente       = cxc.valorReteFuente
                cxcVenta.valorTotal       = cxc.valor
                cxcVenta.save()


                detalleFactura = CxcMoviDetalle.objects.filter(factura__id = cxc.id)
                if detalleFactura.count() > 0:
                    contabilizarFacturas(cxc,detalleFactura)
                else:
                    raise serializers.ValidationError('Debe existir almenos un producto en la factura')

            return cxc
        else:
            mensaje_error = f"No se encontró el producto {facturaDetalleObject.producto.codigoDeBarra} con lote {facturaDetalleObject.lote} en el inventario actual"
            raise serializers.ValidationError(mensaje_error)

def eliminarProductoCotizacion(id,retencionCliente):
    
    
    with transaction.atomic():
        

        cotDetalle = NuevaCotizacionDetalle.objects.get(id = id)
        cot = NuevaCotizacion.objects.get(id = cotDetalle.factura.id)
        


        cantidad  = cotDetalle.cantidad
        descuento = cotDetalle.descuento * cantidad
        iva       = cotDetalle.iva * cantidad
        subtotal  = cotDetalle.subtotal
        total     = cotDetalle.total

        if cot.valorIva > 0:
            cot.valorIva -= iva
            
        if cot.valorReteFuente > 0:
            for x in retencionCliente:
                print(x['retencion']['porcentaje'])
                base    = (subtotal-descuento)
                importe = (base * x['retencion']['porcentaje']) / 100
                cot.valorReteFuente -= importe
                cot.valor           += importe
                 
           
        # if cot.valorReteFuente > 0:
        #     for x in retencionCotizacion:
        #         base    = (subtotal-descuento)
        #         importe = base * x['retencion']['porcentaje'] / 100
        #         # x.base  -= base
        #         # x.total -= importe
        #         cot.valorReteFuente -= importe
        #         cot.valor           += importe
                
            
                # print(x['retencion']['porcentaje'],'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                # base    = (subtotal-descuento)
                # importe = base * x.procentaje / 100
                # x.base  -= base
                # x.total -= importe
                # cot.valorReteFuente -= importe
                # cot.valor           += importe
                # if x.total <= 0:
                #     x.delete()
                # else:
                #     x.save()
            
        
        # subtotal = this.subtotalFactura - this.descuentoFactura;
    #   // console.log(subtotal);

    #   for (let x of this.clienteSeleccionado.retencionCliente) {
    #     if (x.fija) {
    #       this.retencionFactura += (subtotal * x.retencion.porcentaje) / 100;
    #     } else {
    #       if (subtotal >= x.retencion.base) {
    #         this.retencionFactura += (subtotal * x.retencion.porcentaje) / 100;
    #       }
    #     }
    #   }

    #   this.totalFactura -= this.retencionFactura;
    # }
            # print('toca modificar valor retefuente')
        
        cot.subtotal  -= subtotal 
        cot.descuento -= descuento
        cot.valor     -= total
        
        cotDetalle.delete()
        cot.save()
            

        return cot
        
        

def agregarProducto(idfactura,detalle):
    with transaction.atomic():
        kardexObject  = Kardex()
        cxc = CxcMovi.objects.get(id = idfactura)

        if cxc.numeracion.tipoDocumento != numeracion.PROFORMA:
            if cxc.enviadaDian:
                raise serializers.ValidationError('Imposible actualizar, la factura ya fue enviada a la dian')


            valor =  CxcVentas.objects.get(cxc__id  = cxc.id).valorAbono
            if valor > 0:

                    
                raise serializers.ValidationError('Imposible actualizar, la factura y tiene un pago')
                 

        item = detalle
        productoParcial      = item['producto']
        facturaDetalleObject = CxcMoviDetalle() 
        kardexObject         = Kardex()
        product              = Productos.objects.get(id = productoParcial['id'])

        ValidarInventario(product,item['lote'],item['cantidad'])
        facturaDetalleObject.factura          = cxc
        facturaDetalleObject.producto         = product
        facturaDetalleObject.cantidad         = item['cantidad']
        facturaDetalleObject.valor            = item['valor']
        facturaDetalleObject.valorCompra      = item['valorCompra']
        facturaDetalleObject.lote             = item['lote']
   
        facturaDetalleObject.vence            = item['vence']

        if item['iva'] == None or item['iva'] == '':
                facturaDetalleObject.iva = 0
        else:
                facturaDetalleObject.iva = item['iva']
        
        if item['descuento'] == None or item['descuento'] == '':
                facturaDetalleObject.descuento = 0
        else:
                facturaDetalleObject.descuento = item['descuento']
        
        facturaDetalleObject.subtotal = item['subtotal']
        facturaDetalleObject.total    = item['total']

        facturaDetalleObject.save()

       
        if cxc.numeracion.tipoDocumento == numeracion.PROFORMA:
            kardexObject.descripcion = 'Profoma No. '+facturaDetalleObject.factura.numero
            kardexObject.tipo        = 'PF'
        else:
            kardexObject.descripcion = 'Factura No. '+facturaDetalleObject.factura.numero
            kardexObject.tipo        = 'FA'
        
        
        kardexObject.producto    = facturaDetalleObject.producto
        kardexObject.tercero     = facturaDetalleObject.factura.cliente
        kardexObject.bodega      = facturaDetalleObject.producto.bodega
        kardexObject.unidades    = 0 - facturaDetalleObject.cantidad
        kardexObject.balance     = facturaDetalleObject.producto.stock_inicial - facturaDetalleObject.cantidad
        kardexObject.precio      = facturaDetalleObject.valor

        kardexObject.save()

        if Inventario.objects.filter(
            idProducto  = facturaDetalleObject.producto.id,
            lote        = facturaDetalleObject.lote
            ).exists():

            # SE OBTIENE EL PRODUCTO PARA ACTUALIZAR SU CANTIDAD EN EL INVENTARIO
            producto = Inventario.objects.get(
                    idProducto  = facturaDetalleObject.producto.id,
                    lote        = facturaDetalleObject.lote)


            

            # SE ACTUALIZA EL INVENTARIO
            producto.unidades -=  facturaDetalleObject.cantidad
            producto.save()

            # SE ACTUALIZA EL PARAMETRO STOCK EN EL PRODUCTO
            product.stock_inicial -= facturaDetalleObject.cantidad
            product.save()

        else:
            mensaje_error = f"No se encontró el producto {facturaDetalleObject.producto.codigoDeBarra} con lote {facturaDetalleObject.lote} en el inventario actual"
            raise serializers.ValidationError(mensaje_error)

        d = facturaDetalleObject
        if d.iva > 0:
            if cxc.valorIva > 0:
                imp = ImpuestoCxc.objects.filter(factura__id = cxc.id)
                for x in imp:
                    x.base += (d.subtotal-d.descuento )
                    x.total += d.iva * d.cantidad
                    x.save()
            else:
                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                    imp = Impuestos.objects.get(nombre = "IVA (19%)")
                    impFactura = ImpuestoCxc()
                    impFactura.factura    = cxc
                    impFactura.impuesto   = imp
                    impFactura.procentaje = imp.porcentaje
                    impFactura.base       = d.subtotal - d.descuento
                    impFactura.total      = d.iva * d.cantidad  
                    impFactura.save()

        cxc.subtotal  += d.subtotal
        cxc.valorIva  += d.iva * d.cantidad
        cxc.descuento += d.descuento * d.cantidad
        cxc.valor     += d.total
    

        if cxc.valorReteFuente > 0:
            rtf = RetencionCxc.objects.filter(factura__id = cxc.id)
            for x in rtf:
                base     = (d.subtotal-d.descuento)
                importe  = base * x.procentaje / 100
                x.base  += base
                x.total += importe
                cxc.valorReteFuente += importe
                cxc.valor           -= importe
                x.save()
        else:
            retencion = RetencionesClientes.objects.filter(tercero__id = cxc.cliente.id)
            for r in retencion:
                reteFac = RetencionCxc()
                if r.fija:
                    reteFac.factura    = cxc
                    reteFac.retencion  = r.retencion
                    reteFac.base       = cxc.subtotal - cxc.descuento
                    reteFac.procentaje = r.retencion.porcentaje
                    reteFac.total      = reteFac.base * reteFac.procentaje / 100
                    # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                    reteFac.save()

                    cxc.valorReteFuente += reteFac.total
                    cxc.valor -= reteFac.total
                else:
                    if r.retencion.base > 0 and (cxc.subtotal - cxc.descuento) >= r.retencion.base:
                        # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                        reteFac.factura    = cxc
                        reteFac.retencion  = r.retencion 
                        reteFac.base       = cxc.subtotal -  cxc.descuento
                        reteFac.procentaje = r.retencion.porcentaje
                        reteFac.total      = reteFac.base * reteFac.procentaje / 100

                        # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                        reteFac.save()
                        cxc.valor -= reteFac.total
                        cxc.valorReteFuente += reteFac.total
        
        cxc.save()
        cxcDetalle = CxcMoviDetalle.objects.filter(factura__id = cxc.id)
        if cxc.numeracion.tipoDocumento != numeracion.PROFORMA:
                
                cxcVenta = CxcVentas.objects.get(cxc__id = cxc.id)

                cxcVenta.base             = cxc.subtotal
                cxcVenta.iva              = cxc.valorIva
                cxcVenta.valorDescuento   = cxc.descuento

                cxcVenta.reteFuente       = cxc.valorReteFuente
                cxcVenta.valorTotal       = cxc.valor
                cxcVenta.save()


                contabilizarFacturas(cxc,cxcDetalle)
                
def agregarProductoCotizacion(idfactura,detalle,retencionCliente):
    
    with transaction.atomic():
        
        cxc = NuevaCotizacion.objects.get(id = idfactura)
        

        item = detalle
        productoParcial      = item['producto']
        facturaDetalleObject = NuevaCotizacionDetalle() 
        product              = Productos.objects.get(id = productoParcial['id'])

        
        facturaDetalleObject.factura          = cxc
        facturaDetalleObject.producto         = product
        facturaDetalleObject.cantidad         = item['cantidad']
        facturaDetalleObject.valor            = item['valor']
        facturaDetalleObject.valorCompra      = item['valorCompra']
        

        if item['iva'] == None or item['iva'] == '':
                facturaDetalleObject.iva = 0
        else:
                facturaDetalleObject.iva = item['iva']
        
        if item['descuento'] == None or item['descuento'] == '':
                facturaDetalleObject.descuento = 0
        else:
                facturaDetalleObject.descuento = item['descuento']
        
        facturaDetalleObject.subtotal = item['subtotal']
        facturaDetalleObject.total    = item['total']

        facturaDetalleObject.save()


        d = facturaDetalleObject
    
        cxc.subtotal  += d.subtotal
        cxc.valorIva  += d.iva * d.cantidad
        cxc.descuento += d.descuento * d.cantidad
        cxc.valor     += d.total
        
        if cxc.valorReteFuente >0:
            for x in retencionCliente:
                base = (d.subtotal-d.descuento)
                importe = base * x['retencion']['porcentaje'] / 100
                cxc.valorReteFuente += importe
                cxc.valor -= importe
        else:
            for r in retencionCliente:
                
                if r['fija']:
        
                    base       = cxc.subtotal - cxc.descuento
                    procentaje = r['retencion']['porcentaje']
                    total      = base * procentaje / 100
                    

                    cxc.valorReteFuente += total
                    cxc.valor -= total
                else:
                    if r['retencion']['base'] > 0 and (cxc.subtotal - cxc.descuento) >= r['retencion']['base']:
                        # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                         
                        base       = cxc.subtotal - cxc.descuento
                        procentaje = r['retencion']['porcentaje']
                        total      = base * procentaje / 100
                    

                        cxc.valorReteFuente += total
                        cxc.valor -= total
            
    

        # if retencionCotizacion:
            
        #     for x in retencionCotizacion:
        #         base     = (d.subtotal-d.descuento)
        #         importe  = base * x['retencion']['porcentaje'] / 100
                
        #         cxc.valorReteFuente += importe
        #         cxc.valor           -= importe   
        # else:
        #     cxc.valorReteFuente += 0
        #     cxc.valor -= 0
                
        
        cxc.save()
    
        
                
def contabilizarFacturas(cxc:CxcMovi,detalleFactura:CxcMoviDetalle):
    empresa = Empresa.objects.get(id = 1)
    conta = obtener_asiento(cxc.numero,'FAC')
    with transaction.atomic():
        if conta:
            EliminarAsiento(cxc.numero,'FAC')
        
        movi = asiento()
        movi.numero        =  cxc.numero
        movi.fecha         =  cxc.fecha
        movi.empresa       =  empresa
        movi.docReferencia = cxc.numero
        movi.tipo          =  'FAC'
        movi.concepto      =  "Venta segun Factura N°: "+ str(cxc.numero)
        movi.usuario       =  cxc.usuario
        movi.totalDebito   = 0
        movi.totalCredito  = 0
        
        listaDetalleAsiento = []

        lineaTercero = asientoDetalle()
        lineaTercero.asiento  = movi
        lineaTercero.tercero  = cxc.cliente
        lineaTercero.cuenta   = cxc.cliente.cuenta_x_cobrar
        lineaTercero.debito   = cxc.valor
        lineaTercero.tipo     = 'FAC'
        listaDetalleAsiento.append(lineaTercero)


    
    
        for rtf in RetencionCxc.objects.filter(factura__id = cxc.id):
                lineasRetencion = asientoDetalle()
                lineasRetencion.asiento  = movi
                lineasRetencion.tercero  = cxc.cliente
                lineasRetencion.cuenta   = rtf.retencion.ventas
                lineasRetencion.tipo     = 'FAC'
                lineasRetencion.debito   = rtf.total
                listaDetalleAsiento.append(lineasRetencion)

        if cxc.descuento > 0:
            if CuentaNecesaria.objects.filter(nombre = "DESCUENTOS VENTAS").exists():   
                    desc = CuentaNecesaria.objects.get(nombre = "DESCUENTOS VENTAS")
                    detalleDescuento = asientoDetalle()
                    detalleDescuento.tipo    = 'FAC'
                    detalleDescuento.asiento = movi
                    detalleDescuento.tercero = cxc.cliente
                    detalleDescuento.cuenta  = desc.cuenta 
                    detalleDescuento.debito = cxc.descuento
                    listaDetalleAsiento.append(detalleDescuento)
        

        if cxc.valorDomicilio > 0:
            if CuentaNecesaria.objects.filter(nombre = "DOMICILIO").exists():   
                    domi = CuentaNecesaria.objects.get(nombre = "DOMICILIO")
                    detalleDomicilio = asientoDetalle()
                    detalleDomicilio.tipo    = 'FAC'
                    detalleDomicilio.asiento = movi
                    detalleDomicilio.tercero = cxc.cliente
                    detalleDomicilio.cuenta  = domi.cuenta 
                    detalleDomicilio.credito = cxc.valorDomicilio
                    listaDetalleAsiento.append(detalleDomicilio)


        for imp in  ImpuestoCxc.objects.filter(factura__id = cxc.id):
            linea = asientoDetalle()
            linea.asiento  = movi
            linea.tercero  = cxc.cliente
            linea.tipo     = 'FAC'
            linea.cuenta   = imp.impuesto.ventas
            linea.credito  = imp.total
            listaDetalleAsiento.append(linea)
        
        tiposDeMercancia = dict()
        for x in detalleFactura:
                if x.producto.tipoProducto.nombre in tiposDeMercancia:
                        nombre = x.producto.tipoProducto.nombre
                        tiposDeMercancia[nombre].valor_ingreso += (x.valorCompra * x.cantidad)
                        tiposDeMercancia[nombre].valor += x.subtotal
                else:
                        nombre = x.producto.tipoProducto.nombre

                        objecto:tiposMercancia = tiposMercancia(
                            x.producto.tipoProducto,
                            x.producto.tipoProducto.c_tipo,
                            x.subtotal,
                            (x.valorCompra * x.cantidad),
                        )

                        tiposDeMercancia[nombre] = objecto
                

         # INGRESO
        for j in tiposDeMercancia:
                linea2 = asientoDetalle()
                linea2.asiento  = movi
                linea2.tercero  = cxc.cliente
                linea2.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_ingreso
                linea2.tipo     = 'FAC'
                linea2.credito  = tiposDeMercancia[j].valor
                listaDetalleAsiento.append(linea2)

        # COSTO
        for j in tiposDeMercancia:
                linea2 = asientoDetalle()
                linea2.asiento  = movi
                linea2.tercero  = cxc.cliente
                linea2.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_costo
                linea2.tipo     = 'FAC'
                linea2.debito   = tiposDeMercancia[j].valor_ingreso
                listaDetalleAsiento.append(linea2)
        
        # INVENTARIO
        for j in tiposDeMercancia:
                linea2 = asientoDetalle()
                linea2.asiento  = movi
                linea2.tercero  = cxc.cliente
                linea2.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipo
                linea2.tipo     = 'FAC'
                linea2.credito  = tiposDeMercancia[j].valor_ingreso
                listaDetalleAsiento.append(linea2)



        
        movi.save()
        for x in listaDetalleAsiento:
            x.save()


import fpdf
from fpdf import FPDF

import math

def calcular_decremento(num_productos):
    max_suma = 20  # Valor máximo de suma
    min_suma = 1   # Valor mínimo de suma

    # Calcula el decremento en función del número de productos
    decremento = (max_suma - min_suma) / (math.log(num_productos + 1) + 1)

    return max_suma - decremento

def crearTicketPDF(cxc:CxcMovi):
    import os

    detalle = CxcMoviDetalle.objects.filter(factura__id = cxc.id)
    cantidad_productos = len(detalle)
    altura_contenido_adicional = 240  # Ajusta el valor según el contenido adicional
    altura_por_producto = 80  # Ajusta el valor según la altura deseada por producto

    suma = calcular_decremento(cantidad_productos)

    for i in range(cantidad_productos):
        altura_por_producto += suma
        
    # Calcula la altura requerida según la cantidad de productos y el contenido adicional
    altura_requerida = altura_contenido_adicional + altura_por_producto

    pdf = FPDF('P', 'mm', [72.1, altura_requerida])
    pdf.set_margins(1, 6, 1)
    pdf.add_page()

    pdf.image('facturas/logoEmpresa.png', 13.55, 2, 45)
    pdf.set_font('Arial', '', 10)  # Cambio de tamaño de fuente
    pdf.set_text_color(0, 0, 0)

    pdf.ln(14)
    pdf.multi_cell(0, 4, str("SUMIPROD DE LA COSTA S.A.S."), 0, 'C', False)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 4, str("NIT: 901648084-9 RÉGIMEN COMÚN"), 0, 'C', False)
    pdf.multi_cell(0, 4, str("TEL: (5) 432 7722 - CEL: 3116974653"), 0, 'C', False)
    pdf.multi_cell(0, 4, str("CALLE 44B N° 21G-11 URB SANTA CRUZ - SANTA MARTA (MAG)"), 0, 'C', False)
    pdf.multi_cell(0, 4, str("E-mail: sumiprodelacosta@gmail.com"), 0, 'C', False)
    pdf.ln(1)
    pdf.cell(0, 5, str("-----------------------------------------------------------------"), 0, 0, 'C')
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(0, 5, str("FACTURA N°: " + cxc.numero), 0, 0, 'L')
    
    pdf.cell(0, 5, str("FECHA: " + datetime.strftime(cxc.fecha, "%d/%m/%Y")), 0, 0, 'R')
    pdf.ln(5)
    pdf.set_font('Arial', '', 8)

    pdf.multi_cell(0, 3, str("Cliente: " + cxc.cliente.nombreComercial), 0, 0, 'L')
    # pdf.ln(1)
    pdf.cell(0, 5, str("Forma de pago: " + cxc.formaPago.nombre), 0, 0, 'L')
    pdf.ln(3.5)
    pdf.cell(0, 5, str("Documento: " + cxc.cliente.documento), 0, 0, 'L')
    pdf.cell(0, 5, str("CEL: " + cxc.cliente.telefonoContacto), 0, 0, 'R')
    pdf.ln(4.5)
    pdf.multi_cell(0, 3, str(cxc.cliente.direccion), 0, 0, 'L')
    
    pdf.set_font('Arial', '', 9)
   
    pdf.cell(0, 5, str("Vendedor: " + cxc.cliente.vendedor.nombre), 0, 0, 'L')
    pdf.ln(2)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, str("-----------------------------------------------------------------"), 0, 0, 'C')
    pdf.set_font('Arial', 'B', 8)
    pdf.ln(3)
    pdf.cell(7, 5, str("IVA"), 0, 0, 'C')
    pdf.cell(30, 5, str("DESCRIPCIÓN"), 0, 0, 'C')
    pdf.cell(15, 5, str("VLR UND."), 0, 0, 'C')
    pdf.cell(21, 5, str("TOTAL"), 0, 0, 'C')
    pdf.ln(2)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, str("-----------------------------------------------------------------"), 0, 0, 'C')
    pdf.set_font('Arial', '', 7)
    pdf.ln(3)
  
    for x in detalle:
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(0, 4, str(x.producto.nombreymarcaunico + ' ' + x.lote), 0, 'L', False)
        pdf.set_font('Arial', 'B', 9)
        if x.iva > 0:
            pdf.cell(7, 4, str("19%"), 0, 0, 'L')
        else:
            pdf.cell(5, 4, str("0%"), 0, 0, 'L')
        pdf.cell(30, 4, str(str(x.cantidad) + "             " + "x"), 0, 0, 'C')
        pdf.cell(15, 4, str("$" + format(x.valor, ',')), 0, 0, 'C')
        pdf.cell(21, 4, str("$" + format(x.total, ',')), 0, 0, 'R')
        pdf.ln(3)
        pdf.set_font('Arial', '', 9)
        pdf.cell(0, 5, str("-----------------------------------------------------------------"), 0, 0, 'C')
        pdf.set_font('Arial', '', 7)
        pdf.ln(3)

    # pdf.set_font('Arial', '', 7)
    # pdf.cell(0, 5, str("TOTAL PRODUCTOS: " + str(len(detalle))), 0, 0, 'L')
    # pdf.ln(3)
    
    pdf.ln(4)
    pdf.set_font('Arial', '', 8)
    pdf.cell(65, 4, str("SUBTOTAL:"), 0, 0, 'C')
    pdf.set_font('Arial', '', 10)

    pdf.cell(0, 4, str("$" + "{:,.2f}".format(float(cxc.subtotal))), 0, 0, 'R')
    pdf.ln(4)
    pdf.set_font('Arial', '', 8)

    pdf.cell(75, 4, str(" IVA:"), 0, 0, 'C')
    pdf.set_font('Arial', '', 10)

    pdf.cell(0, 4, str("$" + "{:,.2f}".format(float(cxc.valorIva))), 0, 0, 'R')
    pdf.set_font('Arial', '', 8)

    pdf.ln(4)
    pdf.cell(62, 4, str("DESCUENTO:"), 0, 0, 'C')
    pdf.set_font('Arial', '', 10)

    pdf.cell(0, 4, str("$" + "{:,.2f}".format(float(cxc.descuento))), 0, 0, 'R')
    pdf.ln(4)
    pdf.set_font('Arial', '', 8)

    pdf.cell(65, 4, str("DOMICILIO:"), 0, 0, 'C')
    pdf.set_font('Arial', '', 10)

    pdf.cell(0, 4, str("$" + "{:,.2f}".format(float(cxc.valorDomicilio))), 0, 0, 'R')
    pdf.ln(4)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(65, 4, str("TOTAL:"), 0, 0, 'C')
    pdf.cell(0, 4, str("$" + "{:,.2f}".format(float(cxc.valor))), 0, 0, 'R')
    pdf.ln(6)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, str("-----------------------------------------------------------------"), 0, 0, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.ln(4)
    pdf.multi_cell(0, 4, str(cxc.observacion), 0, 'L', False)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, str("-----------------------------------------------------------------"), 0, 0, 'C')
    pdf.ln(15)
    pdf.line(3, pdf.get_y(), 78, pdf.get_y())
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(0, 5, str("RECIBÍ CONFORME"), 0, 0, 'C')
    pdf.ln(7)
    pdf.set_font('Arial', '', 8)
    pdf.multi_cell(0, 3, str("RESOLUCION DE FACTURA No. 18764039900052 DEL 21/11/2022 NUMERACION HABILITADA DEL POS PSC 1 HASTA PSC 5000 VIGENCIA DEL 21/11/2022 AL 21/05/2023"), 0, 'L', False)
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 10)
    pdf.multi_cell(0, 5, str("Favor consignar a la cuenta de ahorros"), 0, 0, 'C')
    pdf.cell(0, 4, str("BANCOLOMBIA"), 0, 0, 'C')
    
    pdf.ln(6)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, str("# 781-000027-67"), 0, 0, 'C')
    pdf.ln(9)
    pdf.image('qr_bancolombia.png', 16.05, pdf.get_y(), 40)
    
    pdf.ln(45)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, str("! GRACIAS POR SU COMPRA ¡"), 0, 0, 'C')
    

    return pdf



def enviarFactura(numero:str):

    factura = CxcMovi.objects.get(numero = numero)

    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"
    # url = "https://webservice.facturatech.co/v2/BETA/WSNOMINADEMO.asmx"
       
    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    fe = GenerateRequestFE(factura)

    xml = fe.crear_xml_factura()

    if xml:
        soap = fe.uploadInvoiceFile(xml)   

        try:
            response = requests.post(url, data = soap, headers = options)
            print(response.text)
        except Exception as ex:
            raise serializers.ValidationError(f'ERROR AL ENVIAR LA FACTURA: {factura.numero} ERROR: {ex}')
             
             
        
        
        dictionary = xmltodict.parse(response.text)
        print(dictionary)
        
        principal                 = dictionary['soap:Envelope']
        body                      = principal['soap:Body']
        uploadInvoiceFileResponse = body['uploadInvoiceFileResponse']
        Result                    = uploadInvoiceFileResponse['uploadInvoiceFileResult']
       
        if int(Result['code']) > 400:
            print("Error al emitir fatura")
            
            error = Result['Msgerror']
            raise serializers.ValidationError(f'ERROR AL FIRMAR LA FACTURA: {factura.numero} ERROR: {error}')
        else:
            with transaction.atomic():
                factura.transaccionID = Result['transaccionID']
                factura.statusFac     = verificarStatus(factura)
                factura.cufe          = obtenerCufeFactura(factura)
                factura.qr            = obtenerQRFactura(factura)
                factura.enviadaDian   = True
                factura.save()
                return Result['success']
    else:
        raise serializers.ValidationError(f'NO SE PUDO CREAR  EL XML DE LA FACTURA: {factura.numero} COMUNIQUESE CON EL AREA DE SISTEMAS')



def descargarXMLFE(numero:str):

    factura = CxcMovi.objects.get(numero = numero)

    fe = GenerateRequestFE(factura)

    xml = fe.crear_xml_factura()
    return xml

def descargarXMLNC(numero:str):

    notaCredito = NotaCreditoVentas.objects.get(numero = numero)

    nc = GenerateRequestNC(notaCredito)

    xml = nc.crear_xml_nc()
    return xml



def obtenerCufeFactura(factura:CxcMovi):
    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"
       
    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    fe = GenerateRequestFE(factura)

    soap = fe.downloadCUFEFile()

    response = requests.post(url, data = soap, headers = options)
   
    
    dictionary = xmltodict.parse(response.text)
    
    principal = dictionary['soap:Envelope']
    body = principal['soap:Body']
    downloadCUFEFileResponse  = body['downloadCUFEFileResponse']
    Result = downloadCUFEFileResponse['downloadCUFEFileResult']
  

    if int(Result['code']) > 400:
        print("Error al obtener cufe")
        error = Result['Msgerror']
        raise serializers.ValidationError(f'NO SE PUDO OBTENER EL CUFE DE LA FACTURA: {factura.numero} \n ERROR: {error}')
       
    else:
        return Result['resourceData']
     
         

def obtenerPDFFactura(factura:CxcMovi):
    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"
       
    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    if factura.enviadaDian == False:
        raise serializers.ValidationError(f'LA FACTURA: {factura.numero} \n NO HA SIDO ENVIADA ANTE LA DIAN.')

    fe = GenerateRequestFE(factura)

    soap       = fe.downloadPDFFile()
    response = requests.post(url, data = soap, headers = options)
    
    
    dictionary = xmltodict.parse(response.text)
    
    principal = dictionary['soap:Envelope']
    body = principal['soap:Body']
    downloadPDFFileResponse  = body['downloadPDFFileResponse']
    Result = downloadPDFFileResponse['downloadPDFFileResult']
 

    if int(Result['code']) > 400:
        print("Error al descar pdf de la  fatura")
        error = Result['Msgerror']
        raise serializers.ValidationError(f'NO SE PUDO OBTENER EL PDF DE LA FACTURA: {factura.numero} \n ERROR: {error}')
    else:
        return  base64.b64decode(Result['resourceData'])
        

     
def obtenerQRFactura(factura:CxcMovi):
    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"
       
    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    fe = GenerateRequestFE(factura)

    soap = fe.downloadQRImageFile()

    response = requests.post(url, data = soap, headers = options)
  
    
    dictionary = xmltodict.parse(response.text)
    
    principal = dictionary['soap:Envelope']
    body = principal['soap:Body']
    downloadCUFEFileResponse  = body['downloadQRImageFileResponse']
    Result = downloadCUFEFileResponse['downloadQRImageFileResult']
  

    if int(Result['code']) > 400:
        print("Error al obtener QR")
        error = Result['Msgerror']
        raise serializers.ValidationError(f'NO SE PUDO OBTENER EL QR DE LA FACTURA: {factura.numero} \n ERROR: {error}')
        
    else:
        return Result['resourceData']
         



def verificarStatus(factura:CxcMovi):
    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"
       
    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    fe = GenerateRequestFE(factura)

    soap = fe.documentStatusFile()

    response = requests.post(url, data = soap, headers = options)

    
    dictionary = xmltodict.parse(response.text)
    
    principal = dictionary['soap:Envelope']
    body = principal['soap:Body']
    documentStatusFileResponse   = body['documentStatusFileResponse']
    Result = documentStatusFileResponse ['documentStatusFileResult']
  

    if int(Result['code']) > 400:
        error = Result['Msgerror']
        raise serializers.ValidationError(f'NO SE PUDO OBTENER EL STATUS DE LA FACTURA: {factura.numero} \n ERROR: {error}')
 
    else:
        return Result['status']
 


def enviarNotaCredito(numero):
    nota = NotaCreditoVentas.objects.get(numero = numero)

    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"

    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    nc = GenerateRequestNC(nota)


    xml = nc.crear_xml_nc()
    if xml:
        soap = nc.uploadInvoiceFile(xml)   

        try:
            response = requests.post(url, data = soap, headers = options)
            print(response.text)
        except Exception as ex:
            raise serializers.ValidationError(f'ERROR AL ENVIAR LA FACTURA: {nota.numero} ERROR: {ex}')
             
        dictionary = xmltodict.parse(response.text)
        print(dictionary)
        
        principal                 = dictionary['soap:Envelope']
        body                      = principal['soap:Body']
        uploadInvoiceFileResponse = body['uploadInvoiceFileResponse']
        Result                    = uploadInvoiceFileResponse['uploadInvoiceFileResult']
       
        if int(Result['code']) > 400:
            print("Error al emitir fatura")
            
            error = Result['Msgerror']
            raise serializers.ValidationError(f'ERROR AL FIRMAR LA NOTA: {nota.numero} ERROR: {error}')
        else:
            with transaction.atomic():
                nota.transaccionID = Result['transaccionID']  
                verificarStatusNota(nota)
                nota.enviadaDian   = True
                nota.save()
                return Result['success']
    else:
        raise serializers.ValidationError(f'NO SE PUDO CREAR  EL XML DE LA NOTA: {nota.numero} COMUNIQUESE CON EL AREA DE SISTEMAS')

def verificarStatusNota(nota:NotaCreditoVentas):
    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"
       
    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    nc = GenerateRequestNC(nota)

    soap = nc.documentStatusFile()

    response = requests.post(url, data = soap, headers = options)

    
    dictionary = xmltodict.parse(response.text)
    
    principal = dictionary['soap:Envelope']
    body = principal['soap:Body']
    documentStatusFileResponse   = body['documentStatusFileResponse']
    Result = documentStatusFileResponse ['documentStatusFileResult']
  

    if int(Result['code']) > 400:
        error = Result['Msgerror']
        raise serializers.ValidationError(f'NO SE PUDO OBTENER EL STATUS DE LA NOTA: {nota.numero} \n ERROR: {error}')
 
    else:
        return Result['status']
 
def obtenerPDFFacturaNota(nota:NotaCreditoVentas):
    url = "https://webservice.facturatech.co/v2/BETA/WSV2PRO.asmx"
       
    options = {
        "Content-Type": "text/xml; charset=utf-8"
    }
   
 
    nc = GenerateRequestNC(nota)

    soap       = nc.downloadPDFFile()
    response = requests.post(url, data = soap, headers = options)
    
    
    dictionary = xmltodict.parse(response.text)
    
    principal = dictionary['soap:Envelope']
    body = principal['soap:Body']
    downloadPDFFileResponse  = body['downloadPDFFileResponse']
    Result = downloadPDFFileResponse['downloadPDFFileResult']
 

    if int(Result['code']) > 400:
        print("Error al descar pdf de la  fatura")
        error = Result['Msgerror']
        raise serializers.ValidationError(f'NO SE PUDO OBTENER EL PDF DE LA NOTA: {nota.numero} \n ERROR: {error}')
    else:
        return  base64.b64decode(Result['resourceData'])
        


def obtenerFacturasClientes(IdTercero):
        TerceroVentas = CxcVentas.objects.prefetch_related(
           
                'cliente',
                'formaPago',
     
                ).filter(cliente__id = IdTercero, estado = False).order_by('fechaVencimiento')
        return TerceroVentas



def crearPagosVenta(create, pagoVenta, pagoVentaDetalle):
       NewPago = PagosVentas()
#        ValidarPagoCompras(pagoCompra, pagocompraDetalle)
       if create:
                num      =  numeracion.objects.get(id = pagoVenta['numeracion'])
                usuario  = User.objects.get(id = pagoVenta['usuario'])
                cuenta   = puc.objects.get(id = pagoVenta['formaPago'])
                tercero  = Terceros.objects.get(id = pagoVenta['cliente'])

                NewPago.numeracion      = num
                NewPago.usuario         = usuario
                NewPago.prefijo         = num.prefijo
                NewPago.consecutivo     = num.proximaFactura
                NewPago.numero          = str(num.proximaFactura).rjust(4,'0') +"-"+ num.prefijo
                NewPago.fecha           = pagoVenta['fecha']
                NewPago.cuenta          = cuenta
                NewPago.cliente         = tercero
                NewPago.observacion     = pagoVenta['observacion']
                

                
                detailPaymentInvoice = []
          
             
            
                                                    

                with transaction.atomic():
                        NewPago.save()

                        for item in pagoVentaDetalle:
                            NewDetail = DetailPaymentInvoiceVentas()

                            cxc = CxcMovi.objects.get(numero = item['factura'])
                     

                       
                            
                            NewDetail.cxc   = cxc
                            NewDetail.pago        = NewPago
                            NewDetail.factura     = cxc.numero
                        
                            NewDetail.saldoAFavor = item['saldoFavor']
                            if item['descuento'] is None or item['descuento'] == '':
                                    NewDetail.descuento = 0
                            else:
                                    NewDetail.descuento = item['descuento']
                            NewDetail.totalAbono = item['valorAbono']                                                                                
                            NewDetail.retefuente = item['retefuente']                                                                                
                            NewDetail.reteica    = item['reteica']                                                                                
                            NewDetail.saldo = (cxc.valor - cxc.abono) - (NewDetail.totalAbono + NewDetail.saldoAFavor + NewDetail.descuento + NewDetail.retefuente + NewDetail.reteica )                                                                     
                            
                            detailPaymentInvoice.append(NewDetail)
                            NewDetail.save()


                        for detalle in detailPaymentInvoice:
                                
                                factura = detalle.cxc
                                factura.abono += (detalle.totalAbono + detalle.saldoAFavor + detalle.descuento + detalle.retefuente + detalle.reteica)
                                if factura.valor >= factura.abono:
                                        factura.pagada = True
                                factura.save() 

                                cxcVentas = CxcVentas.objects.get(cxc__id = factura.id)

                                cxcVentas.valorAbono +=  (detalle.totalAbono + detalle.saldoAFavor + detalle.descuento + detalle.retefuente + detalle.reteica) 
                                saldo = cxcVentas.valorTotal  - cxcVentas.valorAbono
                                if saldo <= 0:
                                    cxcVentas.estado = True
                                cxcVentas.save()
                                
                        ContaFacturaPago = Contabilizar_PagoVentas(NewPago, detailPaymentInvoice ,pagoVenta)                                                                                      

                        num.proximaFactura += 1
                        num.save()

                        asiento = ContaFacturaPago['asiento']
                        detalleConta = ContaFacturaPago['detalle']

                        
                        asiento.save()
                        for x in detalleConta:
                                x.save()
                        
                return NewPago                        
       else:
            pass
       
    
def Contabilizar_PagoVentas(pagoVentas:PagosVentas, Detalle, venta):
        empresa = Empresa.objects.get(id = 1)
        tercero = pagoVentas.cliente
        movi = asiento()
        movi.numero  = pagoVentas.numero
        movi.fecha   = pagoVentas.fecha
        movi.tipo   = 'CI'
        movi.empresa = empresa
        facturas = []
        for x in Detalle:
                facturas.append(x.factura)
        movi.concepto     = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
        movi.docReferencia = ', '.join(map(str, facturas))
        movi.usuario      = pagoVentas.usuario
        movi.totalDebito  = 0
        movi.totalCredito = 0

        listaDetalleCompraAsiento = []

        

       

        lineaTercero = asientoDetalle()
        lineaTercero.asiento = movi
        lineaTercero.cuenta  = tercero.cuenta_x_cobrar
        lineaTercero.tercero = tercero
        lineaTercero.tipo     =  'CI'
        lineaTercero.docReferencia = ', '.join(map(str, facturas))
        lineaTercero.concepto= 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
        lineaTercero.credito  = float(venta['totalAbono']) + float(venta['totalDescuento']) + float(venta['totalSaldoAFavor']) + float(venta['totalRetefuente']) + float(venta['totalReteica'])
        listaDetalleCompraAsiento.append(lineaTercero)

        if float(venta['totalSaldoAFavor']) > 0:
                lineaDetalle          = asientoDetalle()
                lineaDetalle.asiento  = movi
                lineaDetalle.cuenta   = tercero.cuenta_saldo_a_cliente
                lineaDetalle.tercero  = tercero
                lineaDetalle.tipo     =  'CI'
                lineaDetalle.docReferencia = ', '.join(map(str, facturas))

                lineaDetalle.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                lineaDetalle.debito  = float(venta['totalSaldoAFavor'])
                listaDetalleCompraAsiento.append(lineaDetalle)


        if float(venta['totalAbono']) > 0:
                lineaDetalle  = asientoDetalle()
                lineaDetalle.asiento  = movi
                lineaDetalle.cuenta   = pagoVentas.cuenta
                lineaDetalle.tercero  = tercero
                lineaDetalle.tipo     =  'CI'
                lineaDetalle.docReferencia = ', '.join(map(str, facturas))
                lineaDetalle.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                lineaDetalle.debito  = float(venta['totalAbono']) + float(venta['diferencia'])
                listaDetalleCompraAsiento.append(lineaDetalle)


    
        if float(venta['totalDescuento']) > 0:
                if CuentaNecesaria.objects.filter(nombre = "DESCUENTOS PRONTO PAGO VENTAS").exists():   
                        desc = CuentaNecesaria.objects.get(nombre = "DESCUENTOS PRONTO PAGO VENTAS")
                        detalleDescuento = asientoDetalle()
        
                        detalleDescuento.asiento = movi
                        detalleDescuento.tercero = tercero
                        detalleDescuento.tipo     =  'CI'
                        detalleDescuento.docReferencia = ', '.join(map(str, facturas))
                        detalleDescuento.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                        detalleDescuento.cuenta  = desc.cuenta 
                        detalleDescuento.debito  = float(venta['totalDescuento'])
                        listaDetalleCompraAsiento.append(detalleDescuento)

        if float(venta['diferencia']) > 0:
                lineaDetalle          = asientoDetalle()
                lineaDetalle.asiento  = movi
                lineaDetalle.cuenta   = tercero.cuenta_saldo_a_cliente
                lineaDetalle.tercero  = tercero
                lineaDetalle.tipo     = 'CI'
                lineaDetalle.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                lineaDetalle.credito  = float(venta['diferencia'])
                listaDetalleCompraAsiento.append(lineaDetalle)
        
        if float(venta['totalRetefuente']) > 0 or float(venta['totalReteica']) > 0:
                retencion = RetencionesClientes.objects.filter(tercero__id = pagoVentas.cliente.id)
                for r in retencion:

                    lineaDetalle          = asientoDetalle()
                    lineaDetalle.asiento  = movi
                    lineaDetalle.cuenta   = r.retencion.ventas
                    lineaDetalle.tercero  = tercero
                    lineaDetalle.docReferencia = ', '.join(map(str, facturas))
                    lineaDetalle.tipo     =  'CI'
                    lineaDetalle.concepto        = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
                    
                    if 'RETEFUENTE' in r.retencion.nombre:
                         
                        lineaDetalle.debito  = float(venta['totalRetefuente'])
                    if 'RETEICA' in r.retencion.nombre:
                        lineaDetalle.debito  = float(venta['totalReteica'])

                    if lineaDetalle.debito != 0 or lineaDetalle.credito != 0:
                        listaDetalleCompraAsiento.append(lineaDetalle)
        
        pagoVentas.concepto = 'PAGO CORRESPONDIENTE A LAS FACTURAS N°: '+', '.join(map(str, facturas))
        pagoVentas.save()
                

                
        
                              
       

        resultado = dict()
        resultado['asiento'] = movi
        resultado['detalle'] = listaDetalleCompraAsiento 


        return resultado


         
def registrarFacturaElectronicaJSON(archivo):
    with transaction.atomic():
        user = User.objects.get(id = 1)
        num  = numeracion.objects.get(id = 2)
        

        

        for x in archivo:
            
            cxc = CxcMovi()
            cxcVentas = CxcVentas()

            print(x['ciente'])
        
            cliente = Terceros.objects.get(nombreComercial = x['ciente'])


            idfactura = x['idfactura'].split("-")
            cxc.numeracion = num
            if len(idfactura) == 1:
                cxc.consecutivo =  int(idfactura[0])
                cxc.numero = x['idfactura']

            else:
                cxc.prefijo = idfactura[0]
                cxc.consecutivo = int(idfactura[1])
                cxc.numero = x['idfactura']
            
            cxc.cliente = cliente
            cxc.fecha = x['fechaVenta']
            cxc.fechaVencimiento = x['vence']
            cxc.observacion = x['observacion']
            cxc.valorLetras = x['valorletras']
            if 'statusFac' in x:
                cxc.statusFac = x['statusFac']
            cxc.vendedor = cliente.vendedor
            cxc.formaPago = FormaPago.objects.get(nombre = x['formaPago'])
            cxc.cufe = x['cufe']
            cxc.xmlEstado = True

            cxc.subtotal = x['subtotal']
            cxc.descuento = x['totalDescuento']
            cxc.valorIva = x['totalIva']
            cxc.valorReteFuente = x['valorRetefuente'] + x['valorReteIca']
            cxc.valor  = cxc.subtotal + cxc.valorIva - cxc.descuento - cxc.valorReteFuente

            if x['abono'] > 0:
                cxc.abono = x['abono'] - x['valorRetefuente'] - x['valorReteIca']
            else:
                cxc.abono = 0
            if (cxc.valor - cxc.abono) <= 0:
                cxc.pagada = True
            cxc.despachado = x['entregado']
            cxc.usuario = user
            cxc.isElectronica = True
            cxc.enviadaDian   = x['enviadaDian']
            if 'correoEnviado' in x:
                cxc.correoEnviado = x['correoEnviado']
            cxc.save()

            detalle = x['Detalle']




            cxcVentas.cxc              = cxc
            cxcVentas.factura          = cxc.numero
            cxcVentas.formaPago        = cxc.formaPago
            cxcVentas.fecha            = cxc.fecha
            cxcVentas.fechaVencimiento = cxc.fechaVencimiento
            cxcVentas.observacion      = cxc.observacion
            cxcVentas.cliente          = cxc.cliente
            cxcVentas.base             = cxc.subtotal
            cxcVentas.iva              = cxc.valorIva
            cxcVentas.reteFuente       = x['valorRetefuente']
            cxcVentas.reteIca          = x['valorReteIca']
            cxcVentas.valorAbono       = cxc.abono 
            cxcVentas.valorTotal       = cxc.valor
            if (cxc.valor - cxc.abono) <= 0:
                cxcVentas.estado      = True    


            cxcVentas.save()



            baseIVa  = 0
            totalIva = 0

            for j in detalle:
                d = CxcMoviDetalle()
                p = Productos.objects.get(codigoDeBarra = j['codigodebarra'].strip())

                d.factura = cxc
                d.producto    = p
                d.cantidad    = j['cantidad']

                if 'Valorcompra' in detalle:
                    d.valorCompra = j['Valorcompra']
                else:
                    d.valorCompra = 0
                d.valor       = j['valproducto']
                d.lote        = j['lote']
                

                if 'vence' in detalle:
                    d.vence       = j['vence']
                else:
                    d.vence       = '2019-01-01'
                

                d.subtotal = d.valor * d.cantidad

                if j['ivaProducto'] > 0:
                    d.iva = d.subtotal * j['ivaProducto'] / 100
                    baseIVa  += d.subtotal
                    totalIva += d.iva


                if j['descuento'] > 0:
                    d.descuento = d.subtotal * j['descuento'] / 100
                
                d.total = d.subtotal  + d.iva - d.descuento

                d.save()
            

            if baseIVa > 0  and totalIva > 0:

                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                        impFactura = ImpuestoCxc()
                        impFactura.factura    = cxc
                        impFactura.impuesto   = imp
                        impFactura.procentaje = imp.porcentaje
                        
                        impFactura.base       = baseIVa
                        impFactura.total      = totalIva    
                        impFactura.save()

                

            if cxc.valorReteFuente > 0:
              

                # RETEFUENTE = '06'
                # ICA = '07
                if x['valorRetefuente'] > 0:
                    r = Retenciones.objects.get(tipoRetencion = '06', porcentaje = 2.5)

                    reteFac = RetencionCxc()
                    reteFac.factura    = cxc
                    reteFac.retencion  = r
                    reteFac.base       = cxc.subtotal - cxc.descuento
                    reteFac.procentaje = r.porcentaje
                    reteFac.total      = reteFac.base * reteFac.procentaje / 100
                    reteFac.save()

                if x['valorReteIca'] > 0:
                    r = Retenciones.objects.get(tipoRetencion = '07')
                    reteFac = RetencionCxc()
                    reteFac.factura    = cxc
                    reteFac.retencion  = r
                    reteFac.base       = cxc.subtotal - cxc.descuento
                    reteFac.procentaje = r.porcentaje
                    reteFac.total      = reteFac.base * reteFac.procentaje / 100
                    reteFac.save()

                    
            print("ok")

          
def registrarFacturaPosJSON(archivo):
    with transaction.atomic():
        user = User.objects.get(id = 1)
        num  = numeracion.objects.get(id = 4)
        

        

        for x in archivo:
            
            cxc = CxcMovi()
            cxcVentas = CxcVentas()

            print(x['ciente'])
        
            cliente = Terceros.objects.get(nombreComercial = x['ciente'])


            idfactura = x['idfactura'].split("-")
            cxc.numeracion = num
            if len(idfactura) == 1:
                cxc.consecutivo =  int(idfactura[0])
                cxc.numero = x['idfactura']

            else:
                cxc.prefijo = idfactura[0]
                cxc.consecutivo = int(idfactura[1])
                cxc.numero = x['idfactura']
            
            cxc.cliente = cliente
            cxc.fecha = x['fechaVenta']
            cxc.fechaVencimiento = x['vence']
            if 'observacion' in x:
                cxc.observacion = x['observacion']
            else:
                cxc.observacion = ''
            cxc.valorLetras = x['valorletras']
           
            cxc.vendedor = cliente.vendedor
            cxc.formaPago = FormaPago.objects.get(nombre = x['formaPago'])
            cxc.cufe = ''
            cxc.xmlEstado = False
            cxc.valorDomicilio = x['domicilio']
            cxc.subtotal = x['subtotal']
            cxc.descuento = x['totalDescuento']
            cxc.valorIva = x['totalIva']
            cxc.valorReteFuente = 0
            cxc.valor  = cxc.subtotal + cxc.valorIva + cxc.valorDomicilio - cxc.descuento - cxc.valorReteFuente
            cxc.abono = x['abono']
            if (cxc.valor - cxc.abono) <= 0:
                cxc.pagada = True
            cxc.despachado = True
            cxc.usuario = user
            cxc.isElectronica = False
            
         
            cxc.save()

            detalle = x['Detalle']




            cxcVentas.cxc              = cxc
            cxcVentas.factura          = cxc.numero
            cxcVentas.formaPago        = cxc.formaPago
            cxcVentas.fecha            = cxc.fecha
            cxcVentas.fechaVencimiento = cxc.fechaVencimiento
            cxcVentas.observacion      = cxc.observacion
            cxcVentas.cliente          = cxc.cliente
            cxcVentas.base             = cxc.subtotal
            cxcVentas.iva              = cxc.valorIva
            cxcVentas.reteFuente       = x['valorRetefuente']
            cxcVentas.reteIca          = x['valorReteIca']
            cxcVentas.valorAbono       = cxc.abono
            cxcVentas.valorTotal       = cxc.valor
            if (cxc.valor - cxc.abono) <= 0:
                cxcVentas.estado      = True    


            cxcVentas.save()



            baseIVa  = 0
            totalIva = 0

            for j in detalle:
                d = CxcMoviDetalle()
                p = Productos.objects.get(codigoDeBarra = j['codigodebarra'].strip())

                d.factura = cxc
                d.producto    = p
                d.cantidad    = j['cantidad']

                if 'Valorcompra' in detalle:
                    d.valorCompra = j['ValorCompra']
                else:
                    d.valorCompra = 0
                d.valor       = j['valproducto']
                d.lote        = j['lote']
                

                if 'vence' in detalle:
                    d.vence       = j['vence']
                else:
                    d.vence       = '2019-01-01'
                

                d.subtotal = d.valor * d.cantidad

                if j['ivaProducto'] > 0:
                    d.iva = d.subtotal * j['ivaProducto'] / 100
                    baseIVa  += d.subtotal
                    totalIva += d.iva


                if j['descuento'] > 0:
                    d.descuento = d.subtotal * j['descuento'] / 100
                
                d.total = d.subtotal  + d.iva - d.descuento

                d.save()
            

            if baseIVa > 0  and totalIva > 0:

                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                        impFactura = ImpuestoCxc()
                        impFactura.factura    = cxc
                        impFactura.impuesto   = imp
                        impFactura.procentaje = imp.porcentaje
                        
                        impFactura.base       = baseIVa
                        impFactura.total      = totalIva    
                        impFactura.save()

                

                    
            print("ok")



def registrarFacturaProformasJSON(archivo):
    with transaction.atomic():
        user = User.objects.get(id = 1)
        num  = numeracion.objects.get(id = 10)
        

        

        for x in archivo:
            
            cxc = CxcMovi()
           
            print(x['ciente'])
        
            cliente = Terceros.objects.get(nombreComercial = x['ciente'])


            
            cxc.numeracion = num
            cxc.prefijo = 'PRO'
            cxc.consecutivo =  x['idfactura']
            cxc.numero = cxc.prefijo +'-'+ str(x['idfactura'])

            
            
            cxc.cliente = cliente
            cxc.fecha = datetime.now()
            cxc.fechaVencimiento = x['fechaVenta']
            if 'observacion' in x:
                cxc.observacion = x['observacion']
            else:
                cxc.observacion = ''
            cxc.valorLetras = ''
           
            cxc.vendedor = cliente.vendedor
            cxc.formaPago = cliente.formaPago
            cxc.cufe = ''
            cxc.subtotal = x['subtotal']
            cxc.descuento = x['totalDescuento']
            cxc.valorIva = x['totalIva']

            if cxc.subtotal > 1130000:
                cxc.valorReteFuente = cxc.subtotal * 2.5 / 100
            cxc.valor  = cxc.subtotal + cxc.valorIva + cxc.valorDomicilio - cxc.descuento - cxc.valorReteFuente
            
            cxc.usuario = cliente.vendedor.usuario
            cxc.isElectronica = False
            
         
            cxc.save()

            detalle = x['Detalle']


            if cxc.valorReteFuente > 0:
                retencion = RetencionesClientes.objects.filter(tercero__id = cliente.id)
                for r in retencion:
                    reteFac = RetencionCxc()
                    if r.fija:
                        reteFac.factura    = cxc
                        reteFac.retencion  = r.retencion
                        reteFac.base       = cxc.subtotal - cxc.descuento
                        reteFac.procentaje = r.retencion.porcentaje
                        reteFac.total      = reteFac.base * reteFac.procentaje / 100
                        # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                        reteFac.save()
                    else:
                        if r.retencion.base > 0 and (cxc.subtotal - cxc.descuento) >= r.retencion.base:
                            # SE ASIGNARAN SUS DATOS CORRESPONDIENTES
                            reteFac.factura    = cxc
                            reteFac.retencion  = r.retencion 
                            reteFac.base       = cxc.subtotal -  cxc.descuento
                            reteFac.procentaje = r.retencion.porcentaje
                            reteFac.total      = reteFac.base * reteFac.procentaje / 100
                            # SE GUARDARÁ LA RETENCIÓN DEL INGRESO
                            reteFac.save()
        



            baseIVa  = 0
            totalIva = 0

            for j in detalle:
                d = CxcMoviDetalle()
                p = Productos.objects.get(codigoDeBarra = j['codigodebarra'].strip())

                d.factura = cxc
                d.producto    = p
                d.cantidad    = j['cantidad']

                if 'Valorcompra' in detalle:
                    d.valorCompra = j['ValorCompra']
                else:
                    d.valorCompra = 0
                d.valor       = j['valproducto']
                d.lote        = j['lote']
                

                if 'vence' in detalle:
                    d.vence       = j['vence']
                else:
                    d.vence       = '2019-01-01'
                

                d.subtotal = d.valor * d.cantidad

                if j['ivaProducto'] > 0:
                    d.iva = d.valor * j['ivaProducto'] / 100
                    baseIVa  += d.subtotal
                    totalIva += d.iva


                if j['descuento'] > 0:
                    d.descuento = d.valor * j['descuento'] / 100
                
                d.total = d.subtotal  + (d.iva * d.cantidad) - (d.descuento * d.cantidad)
                totalIva = totalIva * d.cantidad
                d.save()
            

            if baseIVa > 0  and totalIva > 0:

                if Impuestos.objects.filter(nombre = "IVA (19%)").exists():
                        imp = Impuestos.objects.get(nombre = "IVA (19%)")
                        impFactura = ImpuestoCxc()
                        impFactura.factura    = cxc
                        impFactura.impuesto   = imp
                        impFactura.procentaje = imp.porcentaje
                        
                        impFactura.base       = baseIVa
                        impFactura.total      = totalIva    
                        impFactura.save()

                

                    
            print("ok")


def setPagosDefault(archivo):
        with transaction.atomic():
        # Guardar en el modelo PagosCompras
                usuario    = User.objects.get(id = 1)

                num = numeracion.objects.get(id = 6)

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
                        if len(numero_split) > 1:
                            facturas = data['facturas']
                            facturas = facturas[0]
                            cliente_fac = CxcMovi.objects.get(numero = facturas['factura'])
                            pagos_compras = PagosVentas(
                                    numeracion=num,
                                    numero=data['numero'],


                                    consecutivo=numero_split[0],
                                    prefijo=numero_split[1],
                                    usuario=usuario,
                                    cliente=cliente_fac.cliente,
                                    fecha=data['fecha'],
                                    cuenta = cuenta,
                                    concepto=data['concepto'],
                                    observacion=data['observacion'],
                            )
                            pagos_compras.save()

                            # Guardar en el modelo DetailPaymentInvoice
                            detalles_pago = data['facturas']
                            for detalle in detalles_pago:
                                print(detalle['factura'])
                                cxp = CxcMovi.objects.get(numero = detalle['factura'])

                                detail_payment_invoice = DetailPaymentInvoiceVentas(
                                        
                                        cxc=cxp,
                                        pago=pagos_compras,
                                        factura=cxp.numero,
                                        descuento=detalle['valorDescuentoPP'],
                                        saldoAFavor=0,
                                        saldo=(cxp.valor - cxp.abono),
                                        totalAbono=detalle['valabono'],
                                        )
                                detail_payment_invoice.save()


     


def registrar_nota_credito_default(archivo):
   
    with transaction.atomic():
        num = numeracion.objects.get(id = 9)
        user = User.objects.get(id = 1)
        print('Comenzamos rey')
        for x in archivo:
            print(x['factura'])
            if x['factura'] != 'FS-00370':
                cxc = CxcVentas.objects.get(factura = x['factura'])
                nota = NotaCreditoVentas()


                idfactura = x['idnotacredito'].split("-")
                nota.numeracion = num
                if len(idfactura) == 1:
                    nota.consecutivo =  int(idfactura[0])
                    nota.numero = x['idnotacredito']
                else:
                    nota.prefijo = idfactura[0]
                    nota.consecutivo = int(idfactura[1])
                    nota.numero = x['idnotacredito']
                nota.tipoNota = x['tipoNotacredito']
                nota.cxc = cxc.cxc
                nota.fecha = x['fecha']
                nota.cliente = cxc.cliente
                nota.isElectronica = x['isElectronica']
                nota.enviadaDian = x['enviadaDian']
                nota.observacion = x['observacion']
                nota.subtotal = float(str(x['subtotal']).replace(',', '.'))
                nota.iva = float(str(x['iva']).replace(',', '.'))
                nota.retencion = float(str(x['retefuente']).replace(',', '.'))
                nota.total = float(str(x['total']).replace(',', '.'))
                nota.usuario = user

                nota.save()


                cxc.valorTotal -= nota.total
                # cxc.iva -= nota.iva
                # cxc.reteFuente -= nota.retencion 
                # cxc.valorTotal += nota.retencion 
                cxc.notacredito = True
                cxc.save()

                if 'Detalle' in x:
                    for detalle_data in x['Detalle']:

                        producto = Productos.objects.get(codigoDeBarra =detalle_data['codigodebarra'] )
                        detalle = DetalleNotaCreditoVentas()
                        detalle.nota = nota
                        detalle.producto = producto
                        detalle.lote = detalle_data['lote']
                        detalle.cantidad = detalle_data['cantidad']
                        detalle.iva = float(str(detalle_data['iva']).replace(',', '.'))
                        if 'valorCompra' in detalle_data:
                            detalle.valorCompra = float(str(detalle_data['valorCompra']).replace(',', '.'))
                        else:
                            detalle.valorCompra = 0
                        detalle.valorUnidad = float(str(detalle_data['valorund']).replace(',', '.'))
                        detalle.subtotal = float(str(detalle_data['subtotal']).replace(',', '.'))
                        detalle.save()


def obtener_facturas_x_cliente(idTercero):
    return CxcMovi.objects.filter(cliente__id = idTercero).values('id','numero','valorReteFuente').order_by('-id')


def obtener_productos_x_factura(idfactura):
    result = CxcMoviDetalle.objects.filter(factura__id = idfactura).values(
        'producto',  # Obtén el ID del producto
        'producto__nombreymarcaunico',  # Obtén el campo nombreymarcaunico del producto
        'producto__codigoDeBarra',  # Obtén el campo codigoDeBarra del producto
        'lote', 'valor', 'cantidad', 'descuento', 'iva','valorCompra'
    )
    result = result.annotate(nombreymarcaunico=F('producto__nombreymarcaunico'),codigoDeBarra=F('producto__codigoDeBarra'))
    return result
                


def registrar_notacredito(create, notaC, notaCDetalle,usuario):
        NewnotaC = NotaCreditoVentas()
        ValidarNotaC(notaC)
        if create:
                num       = numeracion.objects.get(id = notaC['numeracion'])
                cxc       = CxcMovi.objects.get(id = notaC['factura'])
                cxcVentas = CxcVentas.objects.get(cxc__id = cxc.id)



                NewnotaC.numeracion      = num
                NewnotaC.prefijo         = num.prefijo
                NewnotaC.consecutivo     = num.proximaFactura
                NewnotaC.numero          = num.prefijo +"-"+ str(num.proximaFactura).zfill(4)
                NewnotaC.cxc             = cxc
                NewnotaC.cliente         = cxc.cliente
                NewnotaC.tipoNota        = NewnotaC.DEVOLUCION
                NewnotaC.factura         = cxc.numero
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

                        if cxc.isElectronica:
                            NewnotaC.isElectronica = True

                        NewnotaC.save()
                        baseIva = 0
                        for item in notaCDetalle:
                                detalleNotaC = DetalleNotaCreditoVentas()

                               

                                producto = Productos.objects.get(id = item['producto'])
                                
                                detalleNotaC.nota        = NewnotaC
                                detalleNotaC.producto    = producto
                                detalleNotaC.cantidad    = item['cantidad']
                                detalleNotaC.lote        = item['lote']
                            
                                detalleNotaC.valorCompra = item['valorCompra']
                                detalleNotaC.valorUnidad = item['valor']
                                if item['iva'] is None or item['iva'] == '':
                                        detalleNotaC.iva = 0
                                else:
                                        detalleNotaC.iva = item['iva']
                               

                                subtotal = (detalleNotaC.valorUnidad * detalleNotaC.cantidad) 

                                if detalleNotaC.iva > 0:
                                        baseIva += subtotal

                                detalleNotaC.subtotal =  subtotal 
                                detalleNotaC.save()
                                

                                producto.stock_inicial += detalleNotaC.cantidad
                                producto.save()

                                if Inventario.objects.filter(
                                        idProducto  = detalleNotaC.producto.id,
                                        lote        = detalleNotaC.lote
                                        ).exists():

                                        inventarioEditar = Inventario.objects.get(idProducto = detalleNotaC.producto.id, lote = detalleNotaC.lote)
                                        inventarioEditar.unidades += detalleNotaC.cantidad
                                        inventarioEditar.save()

                                        kardexInv             = Kardex()
                                        kardexInv.tercero     = NewnotaC.cliente
                                        kardexInv.producto    = detalleNotaC.producto
                                        kardexInv.tipo        = 'NOC'
                                        kardexInv.descripcion = 'Nota Credito No. '+ NewnotaC.numero
                                        kardexInv.bodega      = detalleNotaC.producto.bodega
                                        kardexInv.unidades    = detalleNotaC.cantidad
                                        kardexInv.balance     = producto.stock_inicial
                                        kardexInv.precio      = detalleNotaC.valorUnidad
                                        
                                        kardexInv.save()

                   
                        
                       

                       
                
                        num = NewnotaC.numeracion 
                        num.proximaFactura += 1
                        num.save()
                        cxcVentas.save()
                        Contabilizar_NotaCredito(NewnotaC)

                return NewnotaC                        
        else:
           pass





    
def Contabilizar_NotaCredito(nota:NotaCreditoVentas):
        empresa = Empresa.objects.get(id = 1)

        movi               = asiento()
        movi.numero        = nota.numero
        movi.fecha         = nota.fecha
        movi.empresa       = empresa
        movi.tipo          =  'NOC'
        movi.docReferencia = nota.cxc.numero
        movi.concepto      = 'Nota Credito Correspondiente a la FAC N° '+str(nota.cxc.numero)
        movi.usuario       = nota.usuario
        movi.totalDebito   = 0
        movi.totalCredito  = 0

        listaDetalleCompraAsiento = []
        cxc = CxcVentas.objects.get(cxc__id = nota.cxc.id)

        cxc.base -= nota.subtotal
        saldoFactura = (cxc.valorTotal) - cxc.valorAbono
        nuevoSaldoClienteAfavor = 0
        nuevoSaldoCliente  = 0
        totalCliente = nota.subtotal + nota.iva
        
        if totalCliente > saldoFactura:
                nuevoSaldoClienteAfavor = totalCliente - saldoFactura
                nuevoSaldoCliente =  totalCliente - nuevoSaldoClienteAfavor
        else:
            nuevoSaldoCliente = totalCliente;


        valorABONO = nuevoSaldoCliente;

        ListaDeProductos = DetalleNotaCreditoVentas.objects.filter(nota__id = nota.id) 


        
               

        if nota.retencion > 0:
                r = RetencionesClientes.objects.filter(tercero__id = nota.cliente.id)
                Base  = nota.subtotal
                for x in r:
                        rtf = asientoDetalle()
                        rtf.asiento = movi
                        rtf.cuenta  = x.retencion.ventas
                        rtf.docReferencia = nota.cxc.numero
                        rtf.tercero = nota.cliente
                        rtf.tipo         =  'NOC'
                        rtf.credito  = Base * x.retencion.porcentaje / 100

                        listaDetalleCompraAsiento.append(rtf)

                        #REVISAR PORQUE NO ME ACUERDO COMO FUNCIONA
                        if nuevoSaldoClienteAfavor  > rtf.credito:
                            nuevoSaldoClienteAfavor -= rtf.credito
                        else:
                            nuevoSaldoCliente -= rtf.credito

                        if x.retencion.tipoRetencion == x.retencion.RETEFUENTE:
                            cxc.reteFuente -= rtf.credito
                        else:
                            cxc.reteIca -= rtf.credito




        if nuevoSaldoClienteAfavor > 0:
                saldoAfavor = asientoDetalle()
                saldoAfavor.asiento = movi
                saldoAfavor.cuenta  = nota.cliente.cuenta_saldo_a_cliente
                saldoAfavor.tercero = nota.cliente
                saldoAfavor.tipo    =  'NOC'
                saldoAfavor.credito = nuevoSaldoClienteAfavor
                saldoAfavor.docReferencia = nota.cxc.numero
                listaDetalleCompraAsiento.append(saldoAfavor)

                

             
        if nuevoSaldoCliente > 0:
                proveedor = asientoDetalle()
                proveedor.asiento = movi
                proveedor.cuenta  = nota.cliente.cuenta_x_cobrar
                proveedor.tercero = nota.cliente
                proveedor.credito  = nuevoSaldoCliente
                proveedor.tipo         =  'NOC'
                proveedor.docReferencia = nota.cxc.numero
                listaDetalleCompraAsiento.append(proveedor)
                cxc.valorTotal -= valorABONO

  



        
        if nota.iva > 0:
             
            for imp in  ImpuestoCxc.objects.filter(ingreso__id = nota.ingreso.id):
                    detalle         = asientoDetalle()
                    detalle.asiento = movi
                    detalle.tercero = nota.cliente
                    detalle.cuenta  = imp.impuesto.ventas
                    detalle.debito = nota.iva
                    detalle.tipo         =  'NOC'
                    detalle.docReferencia = nota.cxc.numero
                    listaDetalleCompraAsiento.append(detalle)
            cxc.iva -= nota.iva



        tiposDeMercancia = dict()
        for x in ListaDeProductos:
                if x.producto.tipoProducto.nombre in tiposDeMercancia:
                        nombre = x.producto.tipoProducto.nombre
                        tiposDeMercancia[nombre].valor_ingreso += (x.valorCompra * x.cantidad)
                        tiposDeMercancia[nombre].valor += x.subtotal
                else:
                        nombre = x.producto.tipoProducto.nombre

                        objecto:tiposMercancia = tiposMercancia(
                            x.producto.tipoProducto,
                            x.producto.tipoProducto.c_tipo,
                            x.subtotal,
                            (x.valorCompra * x.cantidad),
                        )

                        tiposDeMercancia[nombre] = objecto
                

         # INGRESO
        for j in tiposDeMercancia:
                linea2 = asientoDetalle()
                linea2.asiento  = movi
                linea2.tercero  = cxc.cliente
                linea2.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_ingreso
                linea2.tipo     = 'NOC'
                linea2.debito   = tiposDeMercancia[j].valor
                listaDetalleCompraAsiento.append(linea2)

        # COSTO
        for j in tiposDeMercancia:
                linea2 = asientoDetalle()
                linea2.asiento  = movi
                linea2.tercero  = cxc.cliente
                linea2.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_costo
                linea2.tipo     = 'NOC'
                linea2.credito  = tiposDeMercancia[j].valor_ingreso
                listaDetalleCompraAsiento.append(linea2)
        
        # INVENTARIO
        for j in tiposDeMercancia:
                linea2 = asientoDetalle()
                linea2.asiento  = movi
                linea2.tercero  = cxc.cliente
                linea2.cuenta   = tiposDeMercancia[j].tipoDeProducto.c_tipo
                linea2.tipo     = 'NOC'
                linea2.debito   = tiposDeMercancia[j].valor_ingreso
                listaDetalleCompraAsiento.append(linea2)



       
        movi.save()
        nota.contabilizado = True
        nota.save()
        cxc.save()
        
        
        for x in listaDetalleCompraAsiento:
                x.save()

