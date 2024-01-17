from django.db import models
from .models import *







class pucManager(models.Manager):

    def listar_puc(self):
        return self.all().order_by('codigo')          

    def save_or_update(self,id,accion,tipoDeCuenta,naturaleza,nombre,codigo,padre):
        if accion:
            cuenta = puc.objects.get(id=id)
            cuenta.save(nombre = nombre, codigo = codigo)
            return cuenta
        else:
            cuenta = self.create(tipoDeCuenta = tipoDeCuenta,naturaleza = naturaleza, nombre = nombre,codigo = codigo, padre = padre)
            return cuenta



class asientoManager(models.Manager):


    def save_or_update(self,numeroAsiento,fecha,usuario,empresa,detalleAsiento):
    
        try:
            # capturo el asiento
            asiento = self.get(numero = numeroAsiento)
            
            #capturo el detalle del asiento
            dt = asientoDetalle.objects.filter(asiento = asiento)


            #ELIMINO EL DETALLE 
            for d in dt:
            # por cada registro eliminado se dispara el signal para disminuir el credito - debito
                d.delete()

            # actualizo el asiento
            asiento.save(numero = numeroAsiento, fecha = fecha, usuario = usuario, empresa = empresa)

            # registro de nuevo el detalle del asiento, automaticamente
            # se dispara el signal que actualiza el debito y el credito
            asientoDetalle.objects.bulk_create(detalleAsiento)
            return asiento
            

        except self.DoesNotExist:
            asiento = self.objects.create(numero=numeroAsiento,fecha = fecha,usuario = usuario, empresa = empresa)
            asiento.save()

            dt = []
            for d in detalleAsiento:
                d.asiento = asiento
                dt.append(d)
            asientoDetalle.objects.bulk_create(dt)
            return asiento



class comprobantesManager(models.Manager):
    # metodo para guardar un comprobante
    def save_or_update(self,numeracion,numero,referencia,empresa,usuario,total,observaciones,fecha,detalleComprobante):
        try:
            # capturo el comprobante
            comprobante = self.get(numero = numero)
            
            #capturo el detalle del asiento
            dt = CombrobantesDetalleContable.objects.filter(numero = numero)


            #ELIMINO EL DETALLE 
            for d in dt:
                d.delete()

            # actualizo el comprobante
            comprobante.save(fecha = fecha, refrencia = referencia,total = total, observaciones = observaciones, usuario = usuario, empresa = empresa)

            # registro de nuevo el detalle del comprobante
            CombrobantesDetalleContable.objects.bulk_create(detalleComprobante)
            return comprobante
            

        except self.DoesNotExist:
            comprobante = self.objects.create(numeracion = numeracion,numero=numero,refrencia = referencia,total = total, observaciones = observaciones,fecha = fecha,usuario = usuario, empresa = empresa)
            comprobante.save()

            dt = []
            for d in detalleComprobante:
                d.comprobante = comprobante
                dt.append(d)
            CombrobantesDetalleContable.objects.bulk_create(dt)
            return comprobante

