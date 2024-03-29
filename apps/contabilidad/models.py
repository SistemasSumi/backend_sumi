from django.db import models, transaction
from django.db.models.signals import post_save,post_delete
from django.core.exceptions import ValidationError
from .signal import *
from .manager import *

from apps.users.models import User
from django.db.models import F, Sum, Case, When, FloatField
from datetime import datetime,date

import locale
# Setea la variable LC_ALL al conjunto de código UTF-8 con descripción español España
#locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')



from apps.configuracion.models import *

class puc(models.Model):
    """Model definition for puc."""
    CLASE        = 'CLASES'
    SUBCLASE     = 'SUBCLASE'
    GRUPO        = 'GRUPO'
    CUENTA       = 'CUENTA'
    SUBCUENTA    = 'SUBCUENTA'
    AUXILIAR     = 'AUXILIAR'


    DEUDORA      = 'DEUDORA'
    ACREEDORA    = 'ACREEDORA'

    NATURALEZA_CHOICES = (
        (DEUDORA, 'Deudora'),
        (ACREEDORA, 'Acreedora'),
    )

    TIPOSCUENTAS_CHOICES = (
        (CLASE, 'CLASE'),
        (SUBCLASE, 'SUBCLASE'),
        (GRUPO, 'GRUPO'),
        (CUENTA, 'CUENTAS'),
        (SUBCUENTA, 'SUBCUENTA'),
        (AUXILIAR, 'AUXILIAR'),
    )



    ACTIVOSCORRIENTES   = 'EF1'
    ACTIVOSNOCORRIENTES = 'EF2'
    PASIVOSCORRIENTES   = 'EF3'
    PASIVOSNOCORRIENTES = 'EF4'
    PATRIMONIO          = 'EF5'

    INGRESOSDEACTIVIDADESCONTINUADAS = 'RI1'
    COSTOSDEACTIVIDADESCONTINUADAS   = 'RI2'
    GASTOSDEADMINISTRACION           = 'RI3'
    GASTOSFINANCIEROS                = 'RI4'
    INGRESOSFINANCIEROS              = 'RI5'
    IMPUESTOALARENTAYCOMPLEMENTARIOS = 'RI6'

    GRUPOREPORTES_CHOICES = (
        (ACTIVOSCORRIENTES, 'ACTIVOS CORRIENTES'),
        (ACTIVOSNOCORRIENTES, 'ACTIVOS NO CORRIENTES'),
        (PASIVOSCORRIENTES, 'PASIVOS CORRIENTES'),
        (PASIVOSNOCORRIENTES, 'PASIVOS NO CORRIENTES'),
        (PATRIMONIO, 'PATRIMONIO'),
        (INGRESOSDEACTIVIDADESCONTINUADAS, 'INGRESOS DE ACTIVIDADES CONTINUADAS'),
        (COSTOSDEACTIVIDADESCONTINUADAS, 'COSTOS DE ACTIVIDADES CONTINUADAS'),
        (GASTOSDEADMINISTRACION, 'GASTOS DE ADMINISTRACIÓN'),
        (GASTOSFINANCIEROS, 'GASTOS FINANCIEROS'),
        (INGRESOSFINANCIEROS, 'INGRESOS FINANCIEROS'),
        (IMPUESTOALARENTAYCOMPLEMENTARIOS, 'IMPUESTO A LA RENTA Y COMPLEMENTARIOS'),
    )



    id               = models.AutoField(primary_key=True)
    tipoDeCuenta     = models.CharField('Tipo de Cuenta:', max_length=15,blank=False, null=False,choices=TIPOSCUENTAS_CHOICES)
    naturaleza       = models.CharField('Naturaleza de la Cuenta:', max_length=20,blank=False, null=False,choices=NATURALEZA_CHOICES)
    nombre           = models.CharField('Nombre de la cuenta:', max_length=100,blank=False, null=False)
    codigo           = models.IntegerField('Codigo de la cuenta:', unique = True,blank=True, null=True)
    estadoFinanciero = models.BooleanField(blank=True, null=True,default=False)
    estadoResultado  = models.BooleanField(blank=True, null=True,default=False)
    grupoReporte     = models.CharField('Grupo Reporte:', max_length=5,blank=True, null=True, choices=GRUPOREPORTES_CHOICES)
    formaPago        = models.BooleanField(blank=True, null=True, default= False)
    rete_compras     = models.BooleanField(blank=True, null=True, default= False)
    rete_ventas      = models.BooleanField(blank=True, null=True, default= False)
    padre            = models.IntegerField(blank=True, null=True)
    
    

    objects = pucManager()

    # TODO: Define fields here

    class Meta:
        """Meta definition for puc."""

        verbose_name = 'puc'
        verbose_name_plural = 'puc'
        db_table = 'puc'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class asiento(models.Model):
    """Model definition for asiento."""
    id             = models.AutoField(primary_key=True)
    tipo           = models.CharField('tipo', max_length=50,default='')
    numero         = models.CharField('Asiento contable:', max_length=50,blank=False, null=False)
    fecha          = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    mes            = models.CharField('Mes:', max_length=50,blank=True, null=True)
    docReferencia  = models.CharField('docRefencia:', max_length=500,blank=True, null=True)
    anio           = models.CharField('Año:', max_length=50,blank=True, null=True)
    concepto       = models.CharField('Concepto:', max_length=500,blank=True, null=True)
    empresa        = models.ForeignKey(to='configuracion.Empresa', related_name='asiento_empresa', on_delete=models.PROTECT)
    usuario        = models.ForeignKey(User, related_name='asiento_usuario', on_delete=models.PROTECT)
    totalDebito    = models.FloatField('Total crédito:')
    totalCredito   = models.FloatField('Total débito:')



    # TODO: Define fields here

    objects = asientoManager()

    class Meta:
        """Meta definition for asiento."""

        verbose_name = 'asiento'
        verbose_name_plural = 'asientos'
        db_table = 'asiento'

    def save(self, *args, **kwargs):
        # self.fecha = datetime.strptime(str(self.fecha),"%Y-%m-%d").date()
        
        super(asiento, self).save(*args, **kwargs)


    def __str__(self):
        return self.numero


class asientoDetalle(models.Model):
    id      = models.AutoField(primary_key = True)
    asiento = models.ForeignKey(asiento, related_name='asiento_detalle', on_delete=models.PROTECT)
    tercero = models.ForeignKey(to='configuracion.Terceros', related_name='asiento_tercero', on_delete=models.PROTECT)
    cuenta  = models.ForeignKey(puc, related_name='asiento_cuenta', on_delete=models.PROTECT)
    docReferencia    = models.CharField('docRefencia:', max_length=500,blank=True, null=True)
    concepto= models.CharField('Concepto:', max_length=500,blank=True, null=True)
    tipo    = models.CharField('tipo:', max_length=50)
    debito  = models.FloatField('Débito', default   = 0)                  
    credito = models.FloatField('credito', default  = 0)           
    saldo   = models.FloatField('credito', default  = 0)   
    conciliado = models.BooleanField(default = False)        
    fecha   = models.DateField('Fecha', auto_now=False, auto_now_add=False,blank=True, null=True)
    mes     = models.CharField('Mes:', max_length=50,blank=True, null=True)
    anio    = models.CharField('Año:', max_length=50,blank=True, null=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for asientoDetalle."""

        verbose_name = 'asientoDetalle'
        verbose_name_plural = 'asientoDetalles'
        db_table = 'asientoDetalle'


    def save(self, *args, **kwargs):
        # Asignar valores a los atributos del asientoDetalle
        if self.fecha is None:
            self.fecha = self.asiento.fecha
        if self.docReferencia is None:
            self.docReferencia = self.asiento.docReferencia
        if self.tipo is None:
            self.tipo = self.asiento.tipo

        # Guardar el asientoDetalle
        super(asientoDetalle, self).save(*args, **kwargs)

    @classmethod
    def calcular_saldo_diferencia_movimientos(cls, mes, year, saldo_banco, cuenta_id):
        # Calcular el saldo anterior
        saldo_anterior = cls.objects.filter(
            cuenta_id=cuenta_id,
            fecha__lt=f"{year}-{mes}-01"
        ).aggregate(
            saldo_anterior=Sum('debito') - Sum('credito')
        )['saldo_anterior'] or 0

        # Obtener todos los movimientos para el mes y cuenta específicos
        movimientos = cls.objects.filter(
            cuenta_id=cuenta_id,
            fecha__year=year,
            fecha__month=mes
        ).values('id','conciliado','tipo','asiento__numero','tercero__nombreComercial','docReferencia','debito','fecha','credito','concepto').order_by('id','fecha')

        # Calcular el saldo actual
        saldo_actual =   saldo_anterior + sum(
            movimiento['debito'] - movimiento['credito']
            for movimiento in movimientos if movimiento['conciliado']
        )

        # Calcular la diferencia
        diferencia = saldo_banco - saldo_actual

        return {
            'saldo_anterior': saldo_anterior,
            'saldo_actual'  : saldo_actual,
            'diferencia'    : diferencia,
            'movimientos'   : movimientos
        } 

    def __str__(self):
       return self.asiento.numero


class ComprobantesContable(models.Model):
    """Model definition for ComprobantesContable."""

    MC  = 'MC'
    NTC = 'NTC'

    TIPOS_CHOICES = (
        (MC, 'Movimiento contable'),
        (NTC, 'Nota contable'),
    )


    id             = models.AutoField(primary_key=True)
    numeracion     = models.ForeignKey(to='configuracion.numeracion', related_name='numeracion_comprobante', on_delete=models.PROTECT)
    numero         = models.CharField('Numero:', max_length=50, unique = True,blank=True, null=True)
    consecutivo    = models.IntegerField('Consecutivo:',blank=True, null=True)
    tipo           = models.CharField('Tipo movimiento:', max_length=50,blank=True, null=True, choices=TIPOS_CHOICES)
    usuario        = models.ForeignKey(User, related_name='comprobante_usuario', on_delete=models.PROTECT)
    total          = models.FloatField('Total Comprobante:', default = 0)
    fechaRegistro  = models.DateField('Fecha', auto_now=False, auto_now_add=False,blank=True, null=True)
    mes            = models.CharField('Mes:', max_length=50,blank=True, null=True)
    anio           = models.CharField('Año:', max_length=50,blank=True, null=True)

    # TODO: Define fields here


    objects = comprobantesManager()

    class Meta:
        """Meta definition for ComprobantesContable."""

        verbose_name        = 'ComprobantesContable'
        verbose_name_plural = 'ComprobantesContables'
        db_table            = 'comprobantesContables'

    def save(self, *args, **kwargs):
        self.fechaRegistro = datetime.strptime(str(self.fechaRegistro),"%Y-%m-%d")
        self.mes         = self.fechaRegistro.strftime('%B')
        self.anio        = self.fechaRegistro.year
        super(ComprobantesContable, self).save(*args, **kwargs)


    @classmethod
    def filter_comprobantes(cls, obj):
        
        queryset = cls.objects.select_related('numeracion','usuario').all()
        inicial = True
        
        

        if 'numero' in obj and obj['numero'] is not None:
            queryset = queryset.filter(numero=obj['numero'])
            inicial = False

        if 'consecutivo' in obj and obj['consecutivo'] is not None:
            queryset = queryset.filter(consecutivo=obj['consecutivo'])
            inicial = False

        if 'year' in obj and obj['year'] is not None:
            queryset = queryset.filter(fechaRegistro__year=obj['year'])
            inicial = False
        # if 'year' in obj and obj['year'] is not None:
        #     queryset = queryset.filter(fechaRegistro__year=obj['year'])
        #     inicial = False
        # else:
        # # Establecer un valor predeterminado (por ejemplo, el año actual)
        #     current_year = datetime.now().year
        #     queryset = queryset.filter(fechaRegistro__year__lte=current_year)
        #     inicial = False
        

        if 'mes' in obj and obj['mes'] is not None:
            queryset = queryset.filter(fechaRegistro__month=obj['mes'])
            inicial = False

        if 'fechaInicial' in obj and 'fechaFinal' in obj and obj['fechaInicial'] is not None and obj['fechaFinal'] is not None:
                fecha_inicial = obj['fechaInicial']
                fecha_final = obj['fechaFinal']

                fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%dT%H:%M:%S.%fZ")
                fecha_final = datetime.strptime(fecha_final, "%Y-%m-%dT%H:%M:%S.%fZ")

                fecha_inicial = fecha_inicial.strftime("%Y-%m-%d") 
                fecha_final   = fecha_final.strftime("%Y-%m-%d")
                
               


                if fecha_inicial and fecha_final:
                    queryset = queryset.filter(fechaRegistro__gte=fecha_inicial, fechaRegistro__lte=fecha_final)
                    inicial = False

        if 'tipoMovimiento' in obj and obj['tipoMovimiento'] is not None:
            queryset = queryset.filter(tipo=obj['tipoMovimiento'])
            inicial = False

        if 'total' in obj and obj['total'] is not None:
            queryset = queryset.filter(total=obj['total'])
            inicial = False

        if 'cuenta' in obj and obj['cuenta'] is not None:
            queryset = queryset.filter(comprobante_detalle__cuenta__id=obj['cuenta']).distinct()
            inicial = False

        if 'docReferencia' in obj and obj['docReferencia'] is not None:
            queryset = queryset.filter(comprobante_detalle__docReferencia__icontains=obj['docReferencia']).distinct()
            inicial = False


        if 'tercero' in obj and obj['tercero'] is not None:
            queryset = queryset.filter(comprobante_detalle__tercero__id=obj['tercero']).distinct()
            inicial = False


        if 'concepto' in obj and obj['concepto'] is not None:
            queryset = queryset.filter(comprobante_detalle__concepto__icontains=obj['concepto']).distinct()
            inicial = False
            
        # print("Fechas de registro despues de aplicar los filtros:")
        # for comprobante in queryset:
        #     print(f"Comprobante {comprobante.id}: {comprobante.fechaRegistro}")
        for comprobante in queryset:
            print(f"Comprobante {comprobante.id}: Consecutivo - {comprobante.consecutivo}, Fecha - {comprobante.fechaRegistro}")
            

        if inicial:
            return queryset.order_by('-id', '-fechaRegistro')[:20]

        return queryset.order_by('-id', '-fechaRegistro')


    def __str__(self):
        return self.numero


class CombrobantesDetalleContable(models.Model):
    """Model definition for CombrobantesDetalleContable."""

    debito  = 'D'
    credito = 'C'

    
    NATURALEZA_CHOICES = (
        (debito, 'DÉBITO'),
        (credito, 'CRÉDITO'),
    )


    id           = models.AutoField(primary_key=True)
    comprobante  = models.ForeignKey(ComprobantesContable, related_name='comprobante_detalle', on_delete=models.PROTECT)  
    tercero      = models.ForeignKey(to='configuracion.Terceros', related_name='cd_tercero', on_delete=models.PROTECT)
    naturaleza   = models.CharField('Naturaleza:', max_length=50, choices=NATURALEZA_CHOICES)
    docReferencia= models.CharField('Doc ref:', max_length=50)
    cuenta       = models.ForeignKey(puc, related_name='cd_cuenta', on_delete=models.PROTECT)
    concepto     = models.CharField('Descripción', max_length=500,blank=True, null=True)
    debito       = models.FloatField('Débito', default   = 0)                  
    credito      = models.FloatField('credito', default  = 0)                  
    fechaMovi    = models.DateField('Fecha', auto_now=False, auto_now_add=False,blank=True, null=True)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for CombrobantesDetalleContable."""

        verbose_name        = 'CombrobantesDetalleContable'
        verbose_name_plural = 'CombrobantesDetalleContables'
        db_table            = 'CombrobantesDetalleContables'

    def __str__(self):
        return self.comprobante.numero



class CuentaNecesaria(models.Model):
    """Model definition for CuentaNecesaria."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key     = True)
    cuenta   = models.ForeignKey(puc, on_delete = models.PROTECT)
    nombre   = models.CharField("Nombre         : ", max_length = 50, unique = True)
    isCompra = models.BooleanField(default      = False)
    isVenta  = models.BooleanField(default      = False)
    class Meta:
        """Meta definition for CuentaNecesaria."""

        verbose_name = 'CuentaNecesaria'
        verbose_name_plural = 'CuentaNecesarias'
        db_table = 'cuentanecesaria'

    def __str__(self):
        """Unicode representation of CuentaNecesaria."""
        return self.nombre



class Traslado(models.Model):
    """Model definition for Traslado."""

    # TODO: Define fields here
    id             = models.AutoField(primary_key= True)
    numeracion     = models.ForeignKey(to='configuracion.numeracion', related_name='numeracion_traslado', on_delete=models.PROTECT)
    numero         = models.CharField('Numero:', max_length=50, unique = True,blank=True, null=True)
    consecutivo    = models.IntegerField('Consecutivo:',blank=True, null=True)
    fecha          = models.DateField('Fecha:', auto_now=False, auto_now_add=False)
    cuenta_origen  = models.ForeignKey(puc, related_name='traslado_cuenta_origen', on_delete=models.PROTECT)
    cuenta_destino = models.ForeignKey(puc, related_name='traslado_cuenta_destino', on_delete=models.PROTECT)
    monto          = models.FloatField()
    concepto       = models.TextField()
    usuario        = models.ForeignKey(User, related_name='traslado_usuario', on_delete=models.PROTECT)


    def reservar_objeto(self):
        if not self.id:
            # Si el objeto no ha sido guardado (es decir, es un objeto nuevo),
            # configuramos los campos 'numero' y 'consecutivo' basados en 'numeracion'
            if self.numeracion:
                proxima_factura = self.numeracion.proximaFactura
                prefijo = self.numeracion.prefijo
                formato_numero = f'{proxima_factura:04d}'
                self.numero = f'{formato_numero}-{prefijo}'
                self.consecutivo = proxima_factura
                # Incrementar el valor de 'proximaFactura' en el objeto 'numeracion'
                self.numeracion.proximaFactura += 1
                self.numeracion.save()


    def clean(self):
        # Llamar al método clean() de la superclase para realizar las validaciones básicas
        super().clean()

        # Validar el campo 'monto' para asegurarnos de que sea un número
        if not str(self.monto).isnumeric():
            raise ValidationError({'monto': 'El campo "monto" debe ser un número válido.'})

    @classmethod
    def guardar_traslado(cls, data, user, traslado_id=None):

        import json
        from apps.configuracion.models import numeracion
        from datetime import datetime
        from .functions import contabilizar_traslado

        # Convierte el JSON a un diccionario (si no está en formato de diccionario)
        if isinstance(data, str):
            data = json.loads(data)

        # Obtener el ID de 'numeracion' del diccionario JSON
        numeracion_id = data['numeracion']

        # Convertir la cadena en un objeto datetime
        fecha_registro =  datetime.strptime(data['fecha'], "%Y-%m-%dT%H:%M:%S.%fZ")

        # Formatear el objeto datetime como una cadena "YYYY-MM-DD"
        fecha_registro = fecha_registro.strftime("%Y-%m-%d")

        # Obtener la instancia de 'numeracion' a partir del ID proporcionado
        num = numeracion.objects.get(id=numeracion_id)

        # Obtener las instancias de 'cuenta_origen' y 'cuenta_destino' a partir de los IDs proporcionados en el diccionario JSON
        cuenta_origen = puc.objects.get(id=data['cuenta_origen'])
        cuenta_destino = puc.objects.get(id=data['cuenta_destino'])

        # Si traslado_id no es None, es una actualización, de lo contrario es una creación
        with transaction.atomic():
            if traslado_id is not None:
                # Obtener la instancia del traslado existente a partir del ID proporcionado
                traslado = cls.objects.get(pk=traslado_id)

                # Actualizar los campos del traslado con los valores proporcionados
                
                traslado.fecha = fecha_registro
                traslado.cuenta_origen = cuenta_origen
                traslado.cuenta_destino = cuenta_destino
                traslado.monto = float(data['monto'])
                traslado.concepto = data['concepto']
                traslado.usuario = user
            else:
                # Crea una instancia del modelo Traslado con los valores proporcionados
                traslado = cls(
                    numeracion=num,
                    fecha=fecha_registro,
                    cuenta_origen=cuenta_origen,
                    cuenta_destino=cuenta_destino,
                    monto=float(data['monto']),
                    concepto=data['concepto'],
                    usuario = user
                )

            # Reservar el número antes de guardar el objeto
            traslado.reservar_objeto()

            # Guarda el objeto Traslado en la base de datos
            traslado.save()

            # Realiza la contabilización del traslado
            contabilizar_traslado(traslado)

        return traslado

    

    class Meta:
        """Meta definition for Traslado."""

        verbose_name = 'Traslado'
        verbose_name_plural = 'Traslados'

    def __str__(self):
        # Implementar el método __str__ para representar el objeto Traslado en una cadena
        return f'ID: {self.id}, Numero: {self.numero}'



class CajaMenor(models.Model):
    """Model definition for CajaMenor."""
    id             = models.AutoField(primary_key=True)
    numero         = models.IntegerField()
    numero_str     = models.CharField(max_length=50)
    fecha_apertura = models.DateField('fecha apertura:', auto_now=False, auto_now_add=False)
    fecha_cierre   = models.DateField('fecha apertura:', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado         = models.BooleanField(default=False)
    saldo_inicial  = models.FloatField()
    saldo_cierre   = models.FloatField(default = 0)

    

    # TODO: Define fields here
    @classmethod
    def obtener_caja(cls):
        caja = cls.objects.filter(estado = False)
        if caja:
            return caja[0]
        else:
            return None

    @classmethod
    def abrir_caja(cls):
        # Obtener el número más alto entre las cajas existentes
        max_numero = cls.objects.aggregate(models.Max('numero'))['numero__max']

        # Incrementar el número en 1 para la nueva caja
        nuevo_numero = max_numero + 1 if max_numero is not None else 1

        saldo_apertura = asientoDetalle.objects.filter(cuenta__codigo=110510).aggregate(
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
        if saldo_apertura is None:
            saldo_apertura = 0

        # Crear un nuevo registro de caja menor con el número actualizado y la fecha de apertura actual
        caja = cls.objects.create(
            numero=nuevo_numero, 
            numero_str=f'{nuevo_numero:04d}', 
            fecha_apertura=date.today(),
            saldo_inicial = saldo_apertura
        )
        return caja

    @classmethod
    def cerrar_caja(cls, caja_id):
        # Obtener el registro de la caja a cerrar
        try:
            caja = cls.objects.get(id=caja_id)
        except cls.DoesNotExist:
            return None
        
        saldo_cierre = asientoDetalle.objects.filter(cuenta__codigo=110510).aggregate(
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
        if saldo_cierre is None:
            saldo_cierre = 0

        # Actualizar la fecha de cierre y el estado de la caja
        caja.fecha_cierre = date.today()
        caja.estado = True
        caja.saldo_cierre = saldo_cierre;
        caja.save()
        return caja
    class Meta:
        """Meta definition for CajaMenor."""

        verbose_name = 'Caja Menor'
        verbose_name_plural = 'Cajas Menores'

    def __str__(self):
        """Unicode representation of CajaMenor."""
        return f'ID: {self.id}, Numero: {self.numero}'

class PagoCajaMenor(models.Model):
    """Model definition for PagoCajaMenor."""
    # Variables para las opciones del campo 'tipo_gasto'
    ARRIENDOS_CONSTRUCCIONES = '512010'
    ARRIENDOS_FLOTA = '513040'
    ARRIENDOS_OTROS = '513095'
    GASTO_PERSONAL_COMISIONES = '510518'
    GASTO_PERSONAL_BONIFICACIONES = '510548'
    GASTO_PERSONAL_DOTACION = '510551'
    GASTOS_REPARACION_ASEO_CAFETERIA = '519525'
    GASTOS_REPARACION_UTILES_PAPELERIA = '519530'
    GASTOS_REPARACION_COMBUSTIBLES_LUBRICANTES = '519535'
    GASTOS_REPARACION_TAXIS_BUSES = '519545'
    GASTOS_REPARACION_AGASAJOS_EVENTOS = '519565'
    GASTOS_REPARACION_OTROS = '519595'
    GASTOS_VIAJES_ALOJAMIENTO_MANUTENCION = '515505'
    GASTOS_VIAJES_PASAJES_AEREOS = '515515'
    GASTOS_VIAJES_PASAJES_TERRESTRES = '515520'
    GASTOS_VIAJES_OTROS = '515595'
    HONORARIOS_ASESORIA_JURIDICA = '511025'
    HONORARIOS_ASESORIA_FINANCIERA = '511030'
    HONORARIOS_ASESORIA_TECNICA = '511035'
    HONORARIOS_ASESORIA_LABORAL = '511055'
    HONORARIOS_OTROS = '511095'
    MANTENIMIENTO_REPARACION_EQUIPOS_OFICINA = '514520'
    MANTENIMIENTO_REPARACION_EQUIPOS_COMPUTACION_COMUNICACION = '514525'
    PAGO_PROVEEDORES_PROVEEDORES = '220501'
    SERVICIOS_ASISTENCIA_TECNICA = '513515'
    SERVICIOS_ACUEDUCTO_ALCANTARILLADO = '513525'
    SERVICIOS_ENERGIA_ELECTRICA = '513530'
    SERVICIOS_TELEFONOS = '513535'
    SERVICIOS_TRANSPORTE_FLETES_ACARREOS = '513550'
    SERVICIOS_OTROS = '513595'

    TIPOS_GASTOS = (
        (ARRIENDOS_CONSTRUCCIONES, '(ARRIENDOS) CONSTRUCCIONES Y EDIFICACIONES'),
        (ARRIENDOS_FLOTA, '(ARRIENDOS) FLOTA Y EQUIPO DE TRANSPORTE'),
        (ARRIENDOS_OTROS, '(ARRIENDOS) OTROS'),
        (GASTO_PERSONAL_COMISIONES, '(GASTO DEL PERSONAL) COMISIONES'),
        (GASTO_PERSONAL_BONIFICACIONES, '(GASTO DEL PERSONAL) BONIFICACIONES'),
        (GASTO_PERSONAL_DOTACION, '(GASTO DEL PERSONAL) DOTACION Y SUMINISTRO A TRABAJADORES'),
        (GASTOS_REPARACION_ASEO_CAFETERIA, '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) ELEMENTOS DE ASEO Y CAFETERIA'),
        (GASTOS_REPARACION_UTILES_PAPELERIA, '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) UTILES DE PAPELERIA Y FOTOCOPIA'),
        (GASTOS_REPARACION_COMBUSTIBLES_LUBRICANTES, '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) COMBUSTIBLES Y LUBRICANTES'),
        (GASTOS_REPARACION_TAXIS_BUSES, '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) TAXIS Y BUSES'),
        (GASTOS_REPARACION_AGASAJOS_EVENTOS, '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) AGAZAJOS Y EVENTOS'),
        (GASTOS_REPARACION_OTROS, '(GASTOS DE REPARACION Y RELACIONES PUBLICAS) OTROS'),
        (GASTOS_VIAJES_ALOJAMIENTO_MANUTENCION, '(GASTOS DE VIAJES) ALOJAMIENTO Y MANUTENCION'),
        (GASTOS_VIAJES_PASAJES_AEREOS, '(GASTOS DE VIAJES) PASAJES AEREOS'),
        (GASTOS_VIAJES_PASAJES_TERRESTRES, '(GASTOS DE VIAJES) PASAJES TERRESTRES'),
        (GASTOS_VIAJES_OTROS, '(GASTOS DE VIAJES) OTROS'),
        (HONORARIOS_ASESORIA_JURIDICA, '(HONORARIOS) ASESORIA JURIDICA'),
        (HONORARIOS_ASESORIA_FINANCIERA, '(HONORARIOS) ASESORIA FINANCIERA'),
        (HONORARIOS_ASESORIA_TECNICA, '(HONORARIOS) ASESORIA TECNICA'),
        (HONORARIOS_ASESORIA_LABORAL, '(HONORARIOS) ASESORIA LABORAL'),
        (HONORARIOS_OTROS, '(HONORARIOS) OTROS'),
        (MANTENIMIENTO_REPARACION_EQUIPOS_OFICINA, '(MANTENIMIENTO Y REPARACION) EQUIPOS DE OFICINA'),
        (MANTENIMIENTO_REPARACION_EQUIPOS_COMPUTACION_COMUNICACION, '(MANTENIMIENTO Y REPARACION) EQUIPOS DE COMPUTACION Y COMUNICACION'),
        (PAGO_PROVEEDORES_PROVEEDORES, '(PAGO A PROVEEDORES) PROVEEDORES'),
        (SERVICIOS_ASISTENCIA_TECNICA, '(SERVICIOS) ASISTENCIA TECNICA'),
        (SERVICIOS_ACUEDUCTO_ALCANTARILLADO, '(SERVICIOS) ACUEDUCTO Y ALCANTARILLADO'),
        (SERVICIOS_ENERGIA_ELECTRICA, '(SERVICIOS) ENERGIA ELECTRICA'),
        (SERVICIOS_TELEFONOS, '(SERVICIOS) TELEFONOS'),
        (SERVICIOS_TRANSPORTE_FLETES_ACARREOS, '(SERVICIOS) TRASPORTE, FLETES Y ACARREOS'),
        (SERVICIOS_OTROS, '(SERVICIOS) OTROS'),
        # Agrega aquí el resto de las opciones
    )



    # TODO: Define fields here
    id            = models.AutoField(primary_key=True)
    caja          = models.ForeignKey(CajaMenor, on_delete=models.PROTECT , related_name="caja_menor_pago")
    tipo_gasto    = models.CharField('TIPOS DE GASTOS:',choices=TIPOS_GASTOS, max_length=50)
    numero        = models.IntegerField()
    numero_str    = models.CharField(max_length=50)
    tercero       = models.ForeignKey(to='configuracion.Terceros', related_name='pago_caja_tercero', on_delete=models.PROTECT)
    fecha         = models.DateField('fecha:', auto_now=False, auto_now_add=False)
    docReferencia = models.CharField('Doc referencia:', max_length=80)
    concepto      = models.TextField()
    valor         = models.FloatField()



    class Meta:
        """Meta definition for PagoCajaMenor."""

        verbose_name = 'Pago Caja Menor'
        verbose_name_plural = 'Pagos Cajas Menores'

    def __str__(self):
        """Unicode representation of PagoCajaMenor."""
        return f'consecutivo: {self.id}, Caja: {self.caja.numero}'


    @classmethod
    def guardar_o_actualizar_pago(cls, data, user, pago_id=None):
        import json
        from apps.configuracion.models import numeracion,Terceros
        from datetime import datetime
        from .functions import contabilizar_PagoCajaMenor
        # Convierte el JSON a un diccionario (si no está en formato de diccionario)
        if isinstance(data, str):
            data = json.loads(data)


        

        # Obtener el número más alto entre las cajas existentes
        max_numero = cls.objects.aggregate(models.Max('numero'))['numero__max']

        # Incrementar el número en 1 para la nueva caja
        nuevo_numero = max_numero + 1 if max_numero is not None else 1


        # Obtener los datos del objeto JSON
        caja_id        = data.get('caja')
        tipo_gasto     = data.get('tipo_gasto')
        numero         = nuevo_numero
        tercero_id     = data.get('tercero')
        fecha_str      = data.get('fecha')
        doc_referencia = data.get('docReferencia')
        concepto       = data.get('concepto')
        valor          = data.get('valor')

        # Verificar que se proporcionen todos los campos requeridos
        if None in [caja_id, tipo_gasto, numero, tercero_id, fecha_str, doc_referencia, concepto, valor]:
            raise ValueError("Todos los campos son requeridos.")

        
        # Convertir la cadena en un objeto datetime
        fecha =  datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Formatear el objeto datetime como una cadena "YYYY-MM-DD"
        fecha = fecha.strftime("%Y-%m-%d")

        # Obtener las instancias de 'CajaMenor' y 'Terceros' a partir de los IDs proporcionados
        caja_obj = CajaMenor.objects.get(numero=caja_id)
        tercero_obj = Terceros.objects.get(id=tercero_id)

        with transaction.atomic():
            if pago_id is not None:
                # Es una actualización, obtener el pago existente a partir del ID proporcionado
                pago = cls.objects.select_for_update().get(pk=pago_id)
                pago.tipo_gasto = tipo_gasto
                pago.tercero = tercero_obj
                pago.fecha = fecha
                pago.docReferencia = doc_referencia
                pago.concepto = concepto
                pago.valor = float(valor)
            else:
                # Es un nuevo registro, crea una instancia del modelo PagoCajaMenor
                pago = cls(
                    caja=caja_obj,
                    tipo_gasto=tipo_gasto,
                    numero=numero,
                    numero_str=f'{nuevo_numero:04d}', 
                    tercero=tercero_obj,
                    fecha=fecha,
                    docReferencia=doc_referencia,
                    concepto=concepto,
                    valor=float(valor)
                )

            # Guardar el objeto PagoCajaMenor en la base de datos
            pago.save()

            contabilizar_PagoCajaMenor(pago)

        return pago    









class BalancePrueba(models.Model):
    """Model definition for BalancePrueba."""
    cuenta   = models.ForeignKey(puc, on_delete = models.PROTECT)
    padre    = models.IntegerField(blank=True, null=True)
    saldoAnterior = models.FloatField(default = 0)
    saldoActual = models.FloatField(default = 0)
    totalCredito = models.FloatField(default = 0)
    totalDebito = models.FloatField(default = 0)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BalancePrueba."""

        verbose_name = 'BalancePrueba'
        verbose_name_plural = 'BalancePruebas'
        db_table = 'balancePrueba'
    def __str__(self):
        """Unicode representation of BalancePrueba."""
        return f'{self.cuenta.codigo}'


class EstadoFinanciero(models.Model):

    ACTIVOSCORRIENTES   = 'EF1'
    ACTIVOSNOCORRIENTES = 'EF2'
    PASIVOSCORRIENTES   = 'EF3'
    PASIVOSNOCORRIENTES = 'EF4'
    PATRIMONIO          = 'EF5'

    GRUPOREPORTES_CHOICES = (
        (ACTIVOSCORRIENTES, 'ACTIVOS CORRIENTES'),
        (ACTIVOSNOCORRIENTES, 'ACTIVOS NO CORRIENTES'),
        (PASIVOSCORRIENTES, 'PASIVOS CORRIENTES'),
        (PASIVOSNOCORRIENTES, 'PASIVOS NO CORRIENTES'),
        (PATRIMONIO, 'PATRIMONIO'),
       
    )



    cuenta  = models.ForeignKey(puc, on_delete = models.PROTECT)
    padre   = models.IntegerField(blank=True, null=True)
    saldo   = models.FloatField(default = 0)
    grupo   = models.CharField('Grupo Reporte:', max_length=5,blank=True, null=True, choices=GRUPOREPORTES_CHOICES)


    class Meta:
        """Meta definition for estadoFinanciero."""

        verbose_name = 'Estado financiero'
        verbose_name_plural = 'Estados Financieros'
        db_table = 'estadoFinanciero'
    def __str__(self):
        """Unicode representation of estadoFinanciero."""
        return f'{self.cuenta.codigo}'



class Conciliacion(models.Model):
    """Model definition for Conciliacion."""
    id             = models.AutoField(primary_key=True)
    num            = models.ForeignKey("configuracion.numeracion", on_delete=models.CASCADE)
    consecutivo    = models.IntegerField()
    prefijo        = models.CharField('prefijo', max_length=50)
    numero         = models.CharField('numero', max_length=50)
    cuenta        = models.ForeignKey(puc, on_delete = models.PROTECT)
    saldoAnterior = models.FloatField(default= 0)
    saldoFinal    = models.FloatField(default= 0)
    mes       = models.CharField('mes', max_length=50)
    year        = models.CharField('year', max_length=50)
   
    fechaCierre   = models.DateField('fecha cierre', auto_now=True, auto_now_add=False)
    

    # TODO: Define fields here

    class Meta:
        """Meta definition for Conciliacion."""

        verbose_name = 'Conciliacion'
        verbose_name_plural = 'Conciliaciones'
        db_table = 'conciliaciones'


    def __str__(self):
        """Unicode representation of Conciliacion."""
        return f'{self.cuenta.codigo}'

    @classmethod
    def registrar_conciliacion(cls, mes, year, cuenta, saldoAnterior, saldoFinal):
     
        with transaction.atomic():
            try:
                from apps.configuracion.models import numeracion
                num = numeracion.objects.get(tipoDocumento = numeracion.CONCILIACION)
                
                cuenta = puc.objects.get(id=cuenta)


                conciliacion = cls(
                    num = num,
                    prefijo = num.prefijo,
                    consecutivo = num.proximaFactura,
                    numero = str(num.proximaFactura).rjust(4,'0') +"-"+  num.prefijo, 
                    mes=mes,
                    year=year,
                    cuenta=cuenta,
                    saldoAnterior=saldoAnterior,
                    saldoFinal=saldoFinal
                )
                conciliacion.save()
                num.proximaFactura += 1
                num.save()
                return conciliacion
            except Exception as e:
                print(f"Error al registrar la conciliación: {str(e)}")
                raise ValueError(f"Error al registrar la conciliación: {str(e)}")


# signals para el modelo Asiento detalle & Asiento
post_save.connect(update_credito_debito_asiento,sender=asientoDetalle)
post_delete.connect(delete_credito_debito_asiento,sender=asientoDetalle)







