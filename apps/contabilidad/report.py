from .models import *
from datetime import date, datetime, time
from django.db import transaction
from django.db.models import Sum,Case, When, Value, IntegerField,FloatField
from .serializers import BalanceSerializer,EstadoFinancieroSerializer


class BalanceDePrueba():

    cuenta       : puc
    saldoAnterior: float = 0
    saldoActual  : float = 0
    debito       : float = 0
    credito      : float = 0
    padre        : int
    naturaleza   : str
    # movimientos  : list[asientoDetalle]

    def __init__(self,cuenta,padre):

        self.cuenta      = cuenta
        self.padre       = padre
        # self.movimientos = movimientos

        

    

def GenerarBalance(inicio,fin):
    
    inicio = datetime.strptime(inicio+'T00:00:00', '%Y-%m-%dT%H:%M:%S')
    fin    = datetime.strptime(fin+'T23:59:59', '%Y-%m-%dT%H:%M:%S')
    

    detalle = (asientoDetalle.objects.filter(fecha__gte=inicio,fecha__lte=fin)
            .values('cuenta__codigo')
            .annotate(
                totalCredito = Sum('credito'),
                totalDebito  = Sum('debito'),
                saldoActual = Sum(
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
            .order_by('cuenta')
            
        )
    
    saldo_anterior = (asientoDetalle.objects.filter(fecha__lt=inicio)
            .values('cuenta__codigo',)
            .annotate(
                saldoAnterior = Sum(
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
            .order_by('cuenta')
            
        )


    with transaction.atomic():
        listadoB = []

        BalancePrueba.objects.all().delete()

        for x in puc.objects.all():
            b = BalancePrueba()

            b.cuenta = x
            b.padre = x.padre
            listadoB.append(b)
        BalancePrueba.objects.bulk_create(listadoB)
        
        listadoNuevo =  BalancePrueba.objects.all()

        for x in saldo_anterior:
            c = listadoNuevo.get(cuenta__codigo = x['cuenta__codigo'])
            if c.padre:
                print("c",c.padre,c.cuenta.codigo)
                p = listadoNuevo.get(cuenta__codigo = c.padre)
                p.saldoAnterior += x['saldoAnterior']
                p.save()
                if p.padre:
                    # print("p",p.padre)
                    p1 = listadoNuevo.get(cuenta__codigo = p.padre)
                    p1.saldoAnterior += x['saldoAnterior']
                    p1.save()

                    if p1.padre:
                        # print("p1",p1.padre)
                        p2 = listadoNuevo.get(cuenta__codigo = p1.padre)
                        p2.saldoAnterior += x['saldoAnterior']
                        p2.save()

                        if p2.padre:
                            # print("p2",p2.padre)
                            p3 = listadoNuevo.get(cuenta__codigo = p2.padre)
                            p3.saldoAnterior += x['saldoAnterior']
                            p3.save()

            c.saldoAnterior = x['saldoAnterior']
            c.save()
        
        for x in detalle:
            print("************detalle *******************")
            c = listadoNuevo.get(cuenta__codigo = x['cuenta__codigo'])
            if c.padre:
                print("c",c.padre,c.cuenta.codigo)
                p = listadoNuevo.get(cuenta__codigo = c.padre)
                p.totalDebito  += x['totalDebito']
                p.totalCredito += x['totalCredito']
                p.saldoActual  += x['saldoActual']
                p.save()
                if p.padre:
                    # print("p",p.padre)
                    p1 = listadoNuevo.get(cuenta__codigo = p.padre)
                    p1.totalDebito  += x['totalDebito']
                    p1.totalCredito += x['totalCredito']
                    p1.saldoActual  += x['saldoActual']
                    p1.save()

                    if p1.padre:
                        # print("p1",p1.padre)
                        p2 = listadoNuevo.get(cuenta__codigo = p1.padre)
                        p2.totalDebito  += x['totalDebito']
                        p2.totalCredito += x['totalCredito']
                        p2.saldoActual  += x['saldoActual']
                        print("detalle:p2",p2.cuenta.codigo,p2.cuenta.nombre,p2.saldoAnterior,x['saldoActual'])
                        
                        p2.save()

                        if p2.padre:
                            # print("p2",p2.padre)
                            p3 = listadoNuevo.get(cuenta__codigo = p2.padre)
                            p3.totalDebito  += x['totalDebito']
                            p3.totalCredito += x['totalCredito']
                            p3.saldoActual  += x['saldoActual']
                            print("p3",p3.cuenta.codigo,p3.cuenta.nombre,p3.saldoAnterior,x['saldoActual'])
                            p3.save()
            
            c.totalDebito  = x['totalDebito']
            c.totalCredito = x['totalCredito']
            c.saldoActual  =  x['saldoActual']
            print("c:Detalle",c.cuenta.codigo,c.cuenta.nombre,c.saldoAnterior,x['saldoActual'])
            c.save()
        
        balance = listadoNuevo
        reporte = []
        clases  = balance.filter(cuenta__tipoDeCuenta='CLASES').order_by('cuenta__codigo')
        for x in clases:
            reporte.append(x)
            for v in balance.filter(cuenta__padre=x.cuenta.codigo).order_by('cuenta__codigo'):
                reporte.append(v)
                for y in balance.filter(cuenta__padre=v.cuenta.codigo).order_by('cuenta__codigo'):
                    reporte.append(y)
                    for z in balance.filter(cuenta__padre=y.cuenta.codigo).order_by('cuenta__codigo'):
                        reporte.append(z)
                        for a in balance.filter(cuenta__padre=z.cuenta.codigo).order_by('cuenta__codigo'):
                            reporte.append(a)
                            for b in balance.filter(cuenta__padre=a.cuenta.codigo).order_by('cuenta__codigo'):
                                reporte.append(b)



        data = dict()                  
        data['fechaInicial'] = inicio
        data['fechaFinal']   = fin
        data['reporte']      = BalanceSerializer(reporte,many = True).data
        return data
    


        

def EstadoFinancieroReporte(inicio,fin):
    GenerarBalance(inicio,fin)

    balance = BalancePrueba.objects.filter(cuenta__estadoFinanciero = True)

    EstadoFinanciero.objects.all().delete()


    listaDeCuentas = []
    for x in balance.filter(cuenta__tipoDeCuenta = puc.SUBCLASE).order_by('cuenta__codigo'):
        estado = EstadoFinanciero()
        estado.cuenta = x.cuenta
        estado.padre  = x.cuenta.padre
        estado.saldo  = x.saldoAnterior + x.saldoActual
        estado.grupo  = x.cuenta.grupoReporte
        listaDeCuentas.append(estado)
        for y in balance.filter(cuenta__tipoDeCuenta = puc.GRUPO,padre = x.cuenta.codigo).order_by('cuenta__codigo'):
            estado = EstadoFinanciero()
            estado.cuenta = y.cuenta
            estado.padre  = y.cuenta.padre
            estado.saldo  = y.saldoAnterior + y.saldoActual
            estado.grupo  = y.cuenta.grupoReporte
            listaDeCuentas.append(estado)

    EstadoFinanciero.objects.bulk_create(listaDeCuentas)

    data = dict()


    activosCorrientes   = EstadoFinancieroSerializer(
                            EstadoFinanciero.objects.filter(
                                grupo = EstadoFinanciero.ACTIVOSCORRIENTES
                            ),many = True).data
    activosNoCorrientes = EstadoFinancieroSerializer(
                            EstadoFinanciero.objects.filter(
                                grupo = EstadoFinanciero.ACTIVOSNOCORRIENTES
                            ),many = True).data
    pasivosCorrientes = EstadoFinancieroSerializer(
                            EstadoFinanciero.objects.filter(
                                grupo = EstadoFinanciero.PASIVOSCORRIENTES
                            ),many = True).data
    
    pasivosNoCorrientes = EstadoFinancieroSerializer(
                            EstadoFinanciero.objects.filter(
                                grupo = EstadoFinanciero.PASIVOSNOCORRIENTES
                            ),many = True).data
    
    patrimonio = EstadoFinancieroSerializer(
                        EstadoFinanciero.objects.filter(
                            grupo = EstadoFinanciero.PATRIMONIO
                        ),many = True).data
   
    data['ActivosCorrientes']     = activosCorrientes
    data['ActivosNoCorrientes']   = activosNoCorrientes
    data['PasivosCorrientes']     = pasivosCorrientes
    data['PasivosNoCorrientes']   = pasivosNoCorrientes
    data['Patrimonio']            = patrimonio
    data['fechaInicial']          = inicio
    data['fechaFinal']            = fin

    return data




 

