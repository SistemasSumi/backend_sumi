from .models import (
    asiento, 
    asientoDetalle, 
    puc, 
    ComprobantesContable,
    CombrobantesDetalleContable,
    Traslado,
    PagoCajaMenor
)
from django.db import transaction
from apps.configuracion.models import numeracion,Terceros,Empresa
from datetime import date, timedelta,datetime
from django.db.models import Sum,Case, When, Value, ExpressionWrapper,IntegerField,FloatField,F
from django.db.models import Avg, OuterRef, Subquery
from django.db import connection
from django.db.models.functions import Coalesce



from apps.users.models import User

def obtener_asiento(numero,tipo):
    if asiento.objects.filter(numero = numero,tipo = tipo).exists():
        
        asientos = asiento.objects.prefetch_related('asiento_detalle').filter(numero = numero,tipo=tipo)
        return asientos[0]
    else: 
        return None  


def LibroAux(cuenta,inicio,final,tercero):
   


    # c:puc = puc.objects.get(codigo = cuenta)


    print(cuenta)
    print(inicio,final)
    print("tercero", tercero)
    if tercero != '0':
        print("especifico")
        saldoAnterior = asientoDetalle.objects.filter(cuenta__codigo = cuenta,fecha__lt = inicio,tercero__id = tercero).aggregate(
            
            valor = Sum(
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
            
        )

        
        detallle = (asientoDetalle.objects.filter(cuenta__codigo = cuenta,fecha__range=[inicio,final],tercero__id = tercero).order_by('fecha','id'))
        sa = saldoAnterior['valor'] 
        for x in detallle:
            if x.cuenta.naturaleza == 'DEUDORA':
                sa += (x.debito-x.credito)
                x.saldo = sa
            else:
                sa += (x.credito-x.debito)
                x.saldo = sa

        saldoActual = detallle.aggregate(
            
            valor = Sum(
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
        )


    else:

        print("todos")
       
        saldoAnterior = asientoDetalle.objects.filter(cuenta__codigo = cuenta,fecha__lt = inicio).select_related('cuenta','asiento','tercero').order_by('fecha').aggregate(
            
            valor = Sum(
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
        )
        detallle = asientoDetalle.objects.filter(cuenta__codigo =cuenta,fecha__range=[inicio,final]).select_related('cuenta','tercero','asiento').order_by('fecha')
        sa = saldoAnterior['valor'] 
        for x in detallle:
            if x.cuenta.naturaleza == 'DEUDORA':
                sa += (x.debito-x.credito)
                x.saldo = sa
            else:
                sa += (x.credito-x.debito)
                x.saldo = sa

        saldoActual = detallle.aggregate(
            
            valor = Sum(
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
        )

        

    
    data = dict()


    saldoAC = 0
    saldoAN = 0
    if saldoActual['valor']:
        saldoAC = saldoActual['valor']
    if saldoAnterior['valor']:
        saldoAN = saldoAnterior['valor']

    data['saldoActual'] = saldoAN+saldoAC
    data['saldoAnterior'] = saldoAN
    data['detalle'] = detallle
    data['fecha_inicial'] = inicio
    data['fecha_final'] = final
    if  tercero != '0':
        data['tercero'] = detallle[0].tercero.nombreComercial
    else:
        data['tercero'] = 'TODOS LOS TERCEROS'

    data['cuenta'] = str(detallle[0].cuenta.codigo)+' - '+detallle[0].cuenta.nombre

    return data
    

def savePucDefault(archivo):
    listado = []

    for x in archivo:

        p = puc()

        p.codigo       = x["codigo"]
        p.tipoDeCuenta = x["tipo"]
        p.nombre       = x["nombreCuenta"].upper()
        p.naturaleza   = x["naturaleza"]
        if x["padre"] != "":
            p.padre        = int(x["padre"])

        listado.append(p)
    
    puc.objects.bulk_create(listado)


    return archivo


def obtenerCuentasPagos():
    return puc.objects.filter()

def EliminarAsiento(numero,tipo):
    
    resultado = False
    if asiento.objects.filter(numero = numero,tipo=tipo).exists():
        resultado = True
        consultaAsiento = asiento.objects.get(numero = numero, tipo= tipo)
        consultaDetalle = asientoDetalle.objects.filter(asiento = consultaAsiento.id)
        consultaDetalle.delete()
        consultaAsiento.delete()
    else: 
        resultado = False
    return resultado         



def guardarMovimientoContable(create,movi,detalle,usuario):
    
    if create:
        comprobante = ComprobantesContable()


        num       = numeracion.objects.get(id = movi['numeracion'])
        

        comprobante.numeracion = num
        comprobante.consecutivo     = num.proximaFactura
        comprobante.numero          = str(num.proximaFactura).zfill(4)+'-'+num.prefijo
        comprobante.fechaRegistro  = movi['fechaRegistro']
        comprobante.tipo   = movi['tipoMovimiento']
        comprobante.usuario = usuario
        comprobante.total = 0


        listadoDetalle = []
        total = 0
        for x in detalle:

            detalleC    = CombrobantesDetalleContable()

            detalleC.comprobante   = comprobante
            detalleC.fechaMovi     = x['fechaMovimiento']
            detalleC.docReferencia = x['docReferencia']

            cuenta  = x['cuenta']
            tercero = x['tercero']

            detalleC.cuenta        = puc.objects.get(id = cuenta['id']) 
            detalleC.naturaleza    = x['naturaleza']
            detalleC.tercero       = Terceros.objects.get(id = tercero['id'])
            detalleC.concepto      = x['concepto']
            detalleC.debito        = x['debito']
            detalleC.credito       = x['credito']
            total += detalleC.debito
            listadoDetalle.append(detalleC)
        comprobante.total = total
        with transaction.atomic():
            
            comprobante.save()
            comprobante.numeracion.proximaFactura += 1
            comprobante.numeracion.save()

            for x in listadoDetalle:
                
                x.save()

            contabilizarMovimiento(comprobante,listadoDetalle)
        return comprobante
    else:
        comprobante = ComprobantesContable.objects.get(id = movi['id'])


        print(movi)
        print("**************************")
        print(detalle)
        

       
        comprobante.fechaRegistro  = movi['fechaRegistro']
        comprobante.tipo   = movi['tipoMovimiento']
        comprobante.usuario = usuario
        comprobante.total = 0


        listadoDetalle = []
        total = 0
        for x in detalle:

            detalleC    = CombrobantesDetalleContable()

            detalleC.comprobante   = comprobante
            detalleC.fechaMovi     = x['fechaMovimiento']
            detalleC.docReferencia = x['docReferencia']

            cuenta  = x['cuenta']
            tercero = x['tercero']

            detalleC.cuenta        = puc.objects.get(id = cuenta['id']) 
            detalleC.naturaleza    = x['naturaleza']
            detalleC.tercero       = Terceros.objects.get(id = tercero['id'])
            detalleC.concepto      = x['concepto']
            detalleC.debito        = x['debito']
            detalleC.credito       = x['credito']
            total += detalleC.debito
            listadoDetalle.append(detalleC)
        comprobante.total = total
        with transaction.atomic():
            
            CombrobantesDetalleContable.objects.filter(comprobante__id = comprobante.id).delete()


            comprobante.save()
            

            for x in listadoDetalle:
                
                x.save()

            contabilizarMovimiento(comprobante,listadoDetalle)
        return comprobante





def contabilizar_traslado(traslado:Traslado):
    empresa = Empresa.objects.get(id = 1)
    conta   = obtener_asiento(traslado.numero,'TRA')
    

    if conta:
        EliminarAsiento(traslado.numero,'TRA')
    movi = asiento()

    movi.numero        =  traslado.numero
    movi.fecha         =  traslado.fecha
    movi.empresa       =  empresa
    movi.docReferencia =  traslado.numero
    movi.tipo          =  'TRA'
    movi.concepto      =  "Traslado de fondo N°: "+ traslado.numero
    movi.usuario       =  traslado.usuario
    movi.totalDebito   = 0
    movi.totalCredito  = 0

    movi.save()

    tercero = Terceros.objects.get(nombreComercial = 'N/A')


    print(type(traslado.monto))

    linea_detalle_credito = asientoDetalle()
    linea_detalle_credito.asiento    = movi
    linea_detalle_credito.tercero    = tercero
    linea_detalle_credito.cuenta     = traslado.cuenta_origen
    linea_detalle_credito.credito    = traslado.monto
    linea_detalle_credito.tipo       = movi.tipo
    linea_detalle_credito.fecha      = traslado.fecha
    
    linea_detalle_credito.save()


    linea_detalle_debito = asientoDetalle()
    linea_detalle_debito.asiento    = movi
    linea_detalle_debito.tercero    = tercero
    linea_detalle_debito.cuenta     = traslado.cuenta_destino
    linea_detalle_debito.debito     = traslado.monto
    linea_detalle_debito.tipo       = movi.tipo
    linea_detalle_debito.fecha      = traslado.fecha
    linea_detalle_debito.save()


def contabilizar_PagoCajaMenor(pago:PagoCajaMenor):
    empresa = Empresa.objects.get(id = 1)
    conta   = obtener_asiento(pago.numero_str,'CM')
    user = User.objects.get(pk = 1)
    

    if conta:
        EliminarAsiento(pago.numero_str,'CM')
    movi = asiento()

    movi.numero        =  pago.numero_str
    movi.fecha         =  pago.fecha
    movi.empresa       =  empresa
    movi.docReferencia =  pago.numero_str
    movi.tipo          =  'CM'
    movi.concepto      =  "Recibo de caja menor N°: "+ pago.numero_str
    movi.usuario       =  user
    movi.totalDebito   = 0
    movi.totalCredito  = 0

    movi.save()

    tercero = Terceros.objects.get(id = pago.tercero.id)

    cajaMenor = puc.objects.get(codigo = 110510)

    tipoPago = puc.objects.get(codigo = pago.tipo_gasto)

    linea_detalle_credito = asientoDetalle()
    linea_detalle_credito.asiento    = movi
    linea_detalle_credito.tercero    = tercero
    linea_detalle_credito.cuenta     = cajaMenor
    linea_detalle_credito.credito    = pago.valor
    linea_detalle_credito.tipo       = movi.tipo
    linea_detalle_credito.fecha      = pago.fecha
    
    linea_detalle_credito.save()


    linea_detalle_debito = asientoDetalle()
    linea_detalle_debito.asiento    = movi
    linea_detalle_debito.tercero    = tercero
    linea_detalle_debito.cuenta     = tipoPago
    linea_detalle_debito.debito     = pago.valor
    linea_detalle_debito.tipo       = movi.tipo
    linea_detalle_debito.fecha      = pago.fecha
    linea_detalle_debito.save()

        
  


def contabilizarMovimiento(comprobante:ComprobantesContable,listado):
    empresa = Empresa.objects.get(id = 1)
    conta   = obtener_asiento(comprobante.numero,comprobante.tipo)
    with transaction.atomic():
        if conta:
            EliminarAsiento(comprobante.numero,comprobante.tipo)
    
        movi = asiento()
        movi.numero        =  comprobante.numero
        movi.fecha         =  comprobante.fechaRegistro
        movi.empresa       =  empresa
        movi.docReferencia =  comprobante.numero
        movi.tipo          =  comprobante.tipo
        movi.concepto      =  "Movimiento N°: "+ str(comprobante.numero)
        movi.usuario       =  comprobante.usuario
        movi.totalDebito   = 0
        movi.totalCredito  = 0

        movi.save()
        listaDetalleAsiento = []

        for x in listado:
            lineaDetalle = asientoDetalle()
            lineaDetalle.asiento    = movi
            lineaDetalle.tercero    = x.tercero
            lineaDetalle.cuenta     = x.cuenta
            lineaDetalle.debito     = x.debito
            lineaDetalle.concepto   = x.concepto
            lineaDetalle.credito    = x.credito
            lineaDetalle.tipo       = movi.tipo
            lineaDetalle.fecha      = x.fechaMovi
            lineaDetalle.save()





def setContabilidadDefault(archivo):
    empresa = Empresa.objects.get(id = 1)
    index = 1
    with transaction.atomic():
        listadoAsientos = []
        listadoDetalle = []
        for x in archivo:
            t = ''
            if 'tercero' in x:
                t = x['tercero']

            r = ''
            if 'docReferencia' in x:
                r = x['docReferencia']
            
            
            # fecha_cadena = x['fecha']
            # fecha_datetime = datetime.strptime(fecha_cadena, '%Y-%m-%dT%H:%M:%S')
            # fecha_formateada = fecha_datetime.strftime('%Y-%m-%d')

            asi = asiento()
            usuario = User.objects.get(id = 1)
            try:
                asi = asiento.objects.get(numero = x['numero'], tipo = x['tipo'])
            except:
                asi.numero       =  x['numero']
                asi.fecha        =  x['fecha']
                asi.empresa      =  empresa
                if 'docReferencia' in x:
                    asi.docReferencia         =  x['docReferencia']
                asi.tipo         =  x['tipo']
                asi.concepto     =  "CONTABILIDAD FARMAC"
                asi.usuario      =  usuario
                asi.totalDebito  = 0
                asi.totalCredito = 0

                asi.save()
            

            try:

                # documento =  x['tercero'].split("-")
                # d=documento[0]

                tercero = Terceros.objects.get(nombreComercial = x['tercero'] )
            except:
                print('tercero', 'no valido', x['tercero'])
                tercero = Terceros.objects.get(nombreComercial = 'N/A')

            if  x['noCuenta'] != 0:
                cuenta = puc.objects.get(codigo = x['noCuenta'])

                lineaDetalle = asientoDetalle()
                lineaDetalle.asiento    = asi
                lineaDetalle.tercero    = tercero
                lineaDetalle.cuenta     = cuenta
                lineaDetalle.concepto    = x['concepto']
                if 'docReferencia' in x:
                        lineaDetalle.docReferencia  =  x['docReferencia']
                lineaDetalle.debito     = x['debito']
                lineaDetalle.credito    = x['credito']
                lineaDetalle.tipo       = x['tipo']
                lineaDetalle.fecha      = x['fecha']
                
                try:
                    lineaDetalle.save()
                except Exception as e:
                    print(e,index,r,x['fecha'],x['noCuenta'],t)
                index+=1
            
        print("Proceso completado. Todos los datos han sido guardados.")        
 

def reporteCierreContable(mes,year):
    from apps.stock.models import CxPCompras
    from apps.docVentas.models import CxcVentas
    from apps.stock.models import Inventario
    from django.db import models
    from django.db.models import F, Sum, ExpressionWrapper, FloatField, Case, When

    import calendar


    year = int(year)
    mes = int(mes)


    print(mes)
    ultimo_dia = calendar.monthrange(year, mes)[1]


    fecha = f"{year}-{mes:02d}-{ultimo_dia:02d}"
    print(fecha)

    deuda = CxPCompras.objects.filter(estado=False,fecha__lte=fecha).values('formaPago__nombre').annotate(
        total_deuda=Coalesce(Sum(F('valorTotal') - F('valorAbono'), output_field=models.CharField()), Value('0'))
    ).filter(total_deuda__gt=Value('0'))

    # Mapea los resultados en el formato deseado
    cxp = [
        {
            'name': item['formaPago__nombre'],
            'value': float(item['total_deuda']),
        }
        for item in deuda
    ]

    deuda_ventas = CxcVentas.objects.filter(
        estado=False,fecha__lte=fecha  # Ventas pendientes de pago
    ).values(
        'formaPago__nombre'  # Agrupar por nombre de forma de pago
    ).annotate(
        deuda=ExpressionWrapper(
            Coalesce(Sum(F('valorTotal') - F('valorAbono'), output_field=FloatField()), 0),
            output_field=FloatField()
        )
    ).filter(
        deuda__gt=0  # Solo las formas de pago con deuda mayor a 0
    )

    # Mapea los resultados en el formato deseado
    cxc = [
        {
            'name': item['formaPago__nombre'],
            'value': float(item['deuda']),
        }
        for item in deuda_ventas
    ]

    saldo_por_cuenta = asientoDetalle.objects.filter(cuenta__formaPago = True, fecha__lte=fecha).values('cuenta__nombre').annotate(
            saldo=Sum('debito') - Sum('credito')
    )

  
    
    

    result = dict()
    result['cxp'] = cxp
    result['cxc'] = cxc

    result['saldos'] = saldo_por_cuenta


    return result