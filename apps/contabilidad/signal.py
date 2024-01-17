


def update_credito_debito_asiento(sender,instance,**kwargs):
    from apps.configuracion.models import RetencionesEnGeneral,Retenciones,Impuestos,ImpuestosEnGeneral
    if instance.credito > 0:
        instance.asiento.totalCredito = instance.asiento.totalCredito + instance.credito 
        instance.asiento.save()
      
    
    if instance.debito > 0:
        instance.asiento.totalDebito = instance.asiento.totalDebito + instance.debito 
        instance.asiento.save()
   


    # TODO  GUARDADO DE RETENCION & DEVOLUCIÓN COMPRAS
    if  Retenciones.objects.filter(compras__id = instance.cuenta.id).exists():

        r = Retenciones.objects.get(compras__codigo = instance.cuenta.codigo)
        if instance.credito > 0:

            if instance.cuenta.naturaleza == 'ACREEDORA':

                RetencionesEnGeneral.objects.create_retencion(
                        tipo=RetencionesEnGeneral.COMPRAS, 
                        doc_referencia=instance.asiento.docReferencia, 
                        retencion= r, 
                        tercero = instance.tercero,                           
                        base= instance.credito / (r.porcentaje / 100), 
                        porcentaje=r.porcentaje, 
                        total=instance.credito, 
                        fecha=instance.fecha,
                        ventas=False,
                        compras=True
                )
        else:
            if instance.tipo == 'NOCD':
                RetencionesEnGeneral.objects.create_retencion(
                        tipo=RetencionesEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        retencion= r, 
                        tercero = instance.tercero,                           
                        base= instance.debito / (r.porcentaje / 100), 
                        porcentaje=r.porcentaje, 
                        total=instance.debito, 
                        fecha=instance.fecha,
                        ventas=False,
                        compras=True
                )

            
            
    # TODO DEVOLUCIÓN DE RETENCIONES & DEVOLUCIÓN  VENTAS
    if  Retenciones.objects.filter(ventas__id = instance.cuenta.id).exists():
        r = Retenciones.objects.get(ventas__codigo = instance.cuenta.codigo)
        if instance.credito > 0:

            if instance.cuenta.naturaleza == 'DEUDORA' and instance.tipo == 'NOC':

                RetencionesEnGeneral.objects.create_retencion(
                        tipo=RetencionesEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        retencion= r, 
                        tercero = instance.tercero,                           
                        base= instance.credito / (r.porcentaje / 100), 
                        porcentaje=r.porcentaje, 
                        total=instance.credito, 
                        fecha=instance.fecha,
                        ventas=True,
                        compras=False
                )
        else:
            
            RetencionesEnGeneral.objects.create_retencion(
                    tipo=RetencionesEnGeneral.VENTAS, 
                    doc_referencia=instance.asiento.docReferencia, 
                    retencion= r, 
                    tercero = instance.tercero,                           
                    base= instance.debito / (r.porcentaje / 100), 
                    porcentaje=r.porcentaje, 
                    total=instance.debito, 
                    fecha=instance.fecha,
                    ventas=True,
                    compras=False
                    )



    # TODO REGISTRO DE IMPUESTOS  VENTAS
    if Impuestos.objects.filter(ventas__codigo = instance.cuenta.codigo).exists():
        if instance.cuenta.naturaleza == 'ACREEDORA':
            imp = Impuestos.objects.get(ventas__codigo = instance.cuenta.codigo)
            if instance.credito > 0:
                ImpuestosEnGeneral.objects.create_impuesto(
                    tipo=ImpuestosEnGeneral.VENTAS, 
                    doc_referencia=instance.asiento.docReferencia, 
                    impuesto= imp, 
                    tercero = instance.tercero,                           
                    base= instance.credito / (imp.porcentaje / 100), 
                    porcentaje=imp.porcentaje, 
                    total=instance.credito, 
                    fecha=instance.fecha,
                    ventas=True,
                    compras=False  
                        
    )

    # TODO DEVOLUCIÓN DE IMPUESTOS VENTAS - cambiar cuenta  compras despues del deploy importante
    if Impuestos.objects.filter(compras__codigo = instance.cuenta.codigo).exists():
        if  instance.tipo == 'NOC':
            imp = Impuestos.objects.get(compras__codigo = instance.cuenta.codigo)

            if instance.debito > 0:
                ImpuestosEnGeneral.objects.create_impuesto(
                    tipo=ImpuestosEnGeneral.DEVOLUCION, 
                    doc_referencia=instance.asiaento.docReferencia, 
                    impuesto= imp, 
                    tercero = instance.tercero,                           
                    base= instance.debito / (imp.porcentaje / 100), 
                    porcentaje=imp.porcentaje, 
                    total=instance.debito, 
                    fecha=instance.fecha,
                    ventas=False,
                    compras=True  
                )
            else:
                ImpuestosEnGeneral.objects.create_impuesto(
                    tipo=ImpuestosEnGeneral.DEVOLUCION, 
                    doc_referencia=instance.asiento.docReferencia, 
                    impuesto= imp, 
                    tercero = instance.tercero,                           
                    base= instance.credito / (imp.porcentaje / 100), 
                    porcentaje=imp.porcentaje, 
                    total=instance.credito, 
                    fecha=instance.fecha,
                    ventas=False,
                    compras=True  
                )

    # TODO REGISTRO DE IMPUESTOS COMPRAS
    if Impuestos.objects.filter(compras__codigo = instance.cuenta.codigo).exists():
        if instance.cuenta.naturaleza == 'DEUDORA':
            imp = Impuestos.objects.get(compras__codigo = instance.cuenta.codigo)

            if instance.debito > 0:
                ImpuestosEnGeneral.objects.create_impuesto(
                    tipo=RetencionesEnGeneral.COMPRAS, 
                    doc_referencia=instance.asiento.docReferencia, 
                    impuesto= imp, 
                    tercero = instance.tercero,                           
                    base= instance.debito / (imp.porcentaje / 100), 
                    porcentaje=imp.porcentaje, 
                    total=instance.debito, 
                    fecha=instance.fecha,
                    ventas=False,
                    compras=True  
                        
                )
    
   # TODO DEVOLUCIÓN DE IMPUESTOS COMPRAS - cambiar cuenta  ventas despues del deploy importante
    if Impuestos.objects.filter(ventas__codigo = instance.cuenta.codigo).exists():
        if  instance.tipo == 'NOCD':
            imp = Impuestos.objects.get(ventas__codigo = instance.cuenta.codigo)

            if instance.debito > 0:
                ImpuestosEnGeneral.objects.create_impuesto(
                    tipo=ImpuestosEnGeneral.DEVOLUCION, 
                    doc_referencia=instance.asiento.docReferencia, 
                    impuesto= imp, 
                    tercero = instance.tercero,                           
                    base= instance.debito / (imp.porcentaje / 100), 
                    porcentaje=imp.porcentaje, 
                    total=instance.debito, 
                    fecha=instance.fecha,
                    ventas=True,
                    compras=False  
                )
            else:
                ImpuestosEnGeneral.objects.create_impuesto(
                    tipo=ImpuestosEnGeneral.DEVOLUCION, 
                    doc_referencia=instance.asiento.docReferencia, 
                    impuesto= imp, 
                    tercero = instance.tercero,                           
                    base= instance.credito / (imp.porcentaje / 100), 
                    porcentaje=imp.porcentaje, 
                    total=instance.credito, 
                    fecha=instance.fecha,
                    ventas=True,
                    compras=False  
                )
    
    


def delete_credito_debito_asiento(sender,instance,**kwargs):
    from apps.configuracion.models import RetencionesEnGeneral,Retenciones,Impuestos,ImpuestosEnGeneral
    if instance.credito > 0:
        instance.asiento.totalCredito = instance.asiento.totalCredito - instance.credito 
        instance.asiento.save()
    
    if instance.debito > 0:
        instance.asiento.totalDebito = instance.asiento.totalDebito - instance.debito 
        instance.asiento.save()



    # TODO ELIMINACIÓN DE RETENCIÓNES COMPRAS
    if  Retenciones.objects.filter(compras__id = instance.cuenta.id).exists():
        if instance.cuenta.naturaleza == 'ACREEDORA':
            r = Retenciones.objects.get(compras__codigo = instance.cuenta.codigo)

            if instance.credito > 0:
                RetencionesEnGeneral.objects.delete_retencion(
                        tipo=RetencionesEnGeneral.COMPRAS, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base= instance.credito / (r.porcentaje / 100), 
                        fecha=instance.fecha,
                        retencion= r, 
                        tercero = instance.tercero,                           
                        
                )
            else:
                if instance.tipo == 'NOCD':
                    RetencionesEnGeneral.objects.delete_retencion(
                            tipo=RetencionesEnGeneral.DEVOLUCION, 
                            doc_referencia=instance.asiento.docReferencia, 
                            base= instance.debito / (r.porcentaje / 100), 
                            fecha=instance.fecha,
                            retencion= r, 
                            tercero = instance.tercero,                                 
                    )

    
    # TODO ELIMINACIÓN DE RETENCIONES & DEVOLUCIÓN  VENTAS
    if  Retenciones.objects.filter(ventas__id = instance.cuenta.id).exists():
        r = Retenciones.objects.get(ventas__codigo = instance.cuenta.codigo)
        if instance.credito > 0:

            if instance.cuenta.naturaleza == 'DEUDORA' and instance.tipo == 'NOC':

                RetencionesEnGeneral.objects.delete_retencion(
                        tipo=RetencionesEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base= instance.credito / (r.porcentaje / 100), 
                        fecha=instance.fecha,
                        retencion= r, 
                        tercero = instance.tercero,                           
                )
        else:
            
            RetencionesEnGeneral.objects.delete_retencion(
                        tipo=RetencionesEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base= instance.debito / (r.porcentaje / 100), 
                        fecha=instance.fecha,
                        retencion= r, 
                        tercero = instance.tercero,                           
                )



    # TODO DEVOLUCIÓN DE IMPUESTOS VENTAS - cambiar cuenta  compras despues del deploy importante
    if Impuestos.objects.filter(ventas__codigo = instance.cuenta.codigo).exists():
        if  instance.tipo == 'NOC':
            imp = Impuestos.objects.get(ventas__codigo = instance.cuenta.codigo)

            if instance.debito > 0:

                
                ImpuestosEnGeneral.objects.delete_impuesto(
                        tipo=ImpuestosEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base= instance.debito / (imp.porcentaje / 100), 
                        fecha=instance.fecha,
                        impuesto= imp, 
                        tercero = instance.tercero,     
                        
                )   
    
            else:
                ImpuestosEnGeneral.objects.delete_impuesto(
                        tipo=ImpuestosEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base= instance.credito / (imp.porcentaje / 100), 
                        fecha=instance.fecha,
                        impuesto= imp, 
                        tercero = instance.tercero,     
                        
                )   
    

    # TODO DEVOLUCIÓN DE IMPUESTOS COMPRAS - cambiar cuenta  ventas despues del deploy importante
    if Impuestos.objects.filter(compras__codigo = instance.cuenta.codigo).exists():
        if  instance.tipo == 'NOCD':
            imp = Impuestos.objects.get(compras__codigo = instance.cuenta.codigo)

            if instance.debito > 0:
                ImpuestosEnGeneral.objects.delete_impuesto(
                        tipo=ImpuestosEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base  = instance.debito / (imp.porcentaje / 100), 
                        fecha = instance.fecha,
                        impuesto = imp, 
                        tercero  = instance.tercero,     
                )
            else:
                ImpuestosEnGeneral.objects.delete_impuesto(
                        tipo=ImpuestosEnGeneral.DEVOLUCION, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base  = instance.credito / (imp.porcentaje / 100), 
                        fecha = instance.fecha,
                        impuesto = imp, 
                        tercero  = instance.tercero,     
                )
    
    


    if Impuestos.objects.filter(ventas__codigo = instance.cuenta.codigo).exists():
        if instance.cuenta.naturaleza == 'ACREEDORA':
            imp = Impuestos.objects.get(ventas__codigo = instance.cuenta.codigo)

            if instance.credito > 0:
                ImpuestosEnGeneral.objects.delete_impuesto(
                        tipo=ImpuestosEnGeneral.VENTAS, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base= instance.credito / (imp.porcentaje / 100), 
                        fecha=instance.fecha,
                        impuesto= imp, 
                        tercero = instance.tercero,     
                        
                )   
    
            
    if Impuestos.objects.filter(compras__codigo = instance.cuenta.codigo).exists():
        if instance.cuenta.naturaleza == 'ACREEDORA':
            imp = Impuestos.objects.get(compras__codigo = instance.cuenta.codigo)
            if instance.debito > 0:
                ImpuestosEnGeneral.objects.delete_impuesto(
                        tipo=ImpuestosEnGeneral.COMPRAS, 
                        doc_referencia=instance.asiento.docReferencia, 
                        base= instance.debito / (imp.porcentaje / 100), 
                        fecha=instance.fecha,
                        impuesto= imp, 
                        tercero = instance.tercero,     
                )
                    
    

