from django.db import models

from django.db import transaction

# Create your models here.

class tiposDeConcepto(models.Model):
    """Model definition for tiposDeConcepto."""

    # TODO: Define fields here
    id     = models.AutoField(primary_key=True)
    nombre = models.CharField('Tipo de concepto:', max_length=150)



    class Meta:
        """Meta definition for tiposDeConcepto."""

        verbose_name = 'tiposDeConcepto'
        verbose_name_plural = 'tiposDeConceptos'

    def __str__(self):
        """Unicode representation of tiposDeConcepto."""
        return self.nombre

class Concepto(models.Model):
    """Model definition for Concepto."""

    # TODO: Define fields here
    nombre           = models.CharField('Concepto:', max_length=150)
    cuenta           = models.ForeignKey(to="contabilidad.puc",related_name="concepto_cuentas" , on_delete=models.PROTECT,blank=True, null=True)
    contrapartida    = models.ForeignKey(to="contabilidad.puc",related_name="concepto_cuentas_contra" , on_delete=models.PROTECT,blank=True, null=True)
    tipo             = models.ForeignKey(tiposDeConcepto, related_name="tipos_concepto" ,on_delete=models.PROTECT)
    valor            = models.FloatField(default = 0)
    empleado         = models.FloatField(default = 0)
    empleador        = models.FloatField(default = 0)


    class Meta:
        """Meta definition for Concepto."""

        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'

    def __str__(self):
        """Unicode representation of Concepto."""
        return self.nombre


class Eps(models.Model):
    """Model definition for EmpresaPrestadoraDeServicios."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)


    class Meta:
        """Meta definition for EmpresaPrestadoraDeServicios."""

        verbose_name = 'Empresa Prestadora De Servicio'
        verbose_name_plural = 'Empresa Prestadora De Servicios'

    def __str__(self):
        """Unicode representation of EmpresaPrestadoraDeServicios."""
        return self.tercero.nombreComercial


class FondoPension(models.Model):
    """Model definition for FondoPension."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)



    class Meta:
        """Meta definition for FondoPension."""

        verbose_name = 'FondoPension'
        verbose_name_plural = 'FondoPensiones'

    def __str__(self):
        """Unicode representation of FondoPension."""
        return self.tercero.nombreComercial


class Arl(models.Model):
    """Model definition for Arl."""


    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)
    
     
    # riesgo   = models.FloatField('Riesgo:',choices=RIESGOS_CHOICES,blank=True, null=True)
    


    class Meta:
        """Meta definition for Arl."""

        verbose_name = 'Arl'
        verbose_name_plural = 'Arls'

    def __str__(self):
        """Unicode representation of Arl."""
        return self.tercero.nombreComercial




class FondoCesantias(models.Model):
    """Model definition for FondoCesantias."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)
    

    class Meta:
        """Meta definition for FondoCesantias."""

        verbose_name = 'FondoCesantias'
        verbose_name_plural = 'FondoCesantias'

    def __str__(self):
        """Unicode representation of FondoCesantias."""
        return self.tercero.nombreComercial


class Sena(models.Model):
    """Model definition for Sena."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)



    class Meta:
        """Meta definition for Sena."""

        verbose_name = 'Sena'
        verbose_name_plural = 'Sena'

    def __str__(self):
        """Unicode representation of Sena."""
        return self.tercero.nombreComercial


class CajaCompensacion(models.Model):
    """Model definition for CajaCompensacion."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)



    class Meta:
        """Meta definition for Sena."""

        verbose_name = 'Caja de compensación'
        verbose_name_plural = 'Caja de compensaciones'

    def __str__(self):
        """Unicode representation of CajaCompensacion."""
        return self.tercero.nombreComercial






class ICBF(models.Model):
    """Model definition for ICBF."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)



    class Meta:
        """Meta definition for ICBF."""

        verbose_name = 'ICBF'
        verbose_name_plural = 'ICBF'

    def __str__(self):
        """Unicode representation of ICBF."""
        return self.tercero.nombreComercial
    
class IngresoRecurrente(models.Model):
    """Model definition for IngresoRecurrente."""


    salarial   = 1
    noSalarial = 2

    TIPO_CHOICES = (
        (salarial, 'Salarial'),
        (noSalarial, 'No Salarial'),
       
    )

    tipo           = models.IntegerField('tipo: ',choices = TIPO_CHOICES, default = salarial)
    concepto       = models.ForeignKey(Concepto,related_name = "ingresoRecurrente_conceptos" ,on_delete = models.PROTECT)
    valorMensual   = models.FloatField('Valor Mensual:')
    valorQuincenal = models.FloatField('Valor Quincena:')


    # TODO: Define fields here



    class Meta:
        """Meta definition for IngresoRecurrente."""

        verbose_name = 'IngresoRecurrente'
        verbose_name_plural = 'IngresoRecurrentes'

    def __str__(self):
        """Unicode representation of IngresoRecurrente."""
        return f'Tipo:{self.tipo} Monto:{self.valorMensual}'
    

class DeduccionRecurrente(models.Model):
    """Model definition for DeduccionRecurrente."""


    salarial   = 1
    noSalarial = 2

    TIPO_CHOICES = (
        (salarial, 'Salarial'),
        (noSalarial, 'No Salarial'),
       
    )

    tipo           = models.IntegerField('tipo: ',choices = TIPO_CHOICES, default = salarial)
    concepto       = models.ForeignKey(Concepto,related_name = "deduccionRecurrente_conceptos" ,on_delete = models.PROTECT)
    valorMensual   = models.FloatField('Valor Mensual:')
    valorQuincenal = models.FloatField('Valor Quincena:')


    # TODO: Define fields here



    class Meta:
        """Meta definition for DeduccionRecurrente."""

        verbose_name = 'DeduccionRecurrente'
        verbose_name_plural = 'DeduccionRecurrentes'

    def __str__(self):
        """Unicode representation of DeduccionRecurrente."""
        return f'Tipo:{self.tipo} Monto:{self.valorMensual}'






class Contrato(models.Model):
    """Model definition for Contrato."""
    # tipos de contrato
    Termino_Fijo       = '1'
    Termino_Indefinido = '2'
    Obra_o_Labor       = '3'
    Aprendizaje        = '4'
    Practicas          = '5'


    minimo = 0.522
    bajo   = 1.044
    medio  = 2.436
    alto   = 4.350
    maximo = 6.960

    RIESGOS_CHOICES = (
        (minimo, 'Minimo - Riesgo 1'),
        (bajo, 'Bajo - Riesgo 2'),
        (medio, 'Medio - Riesgo 3'),
        (alto, 'Alto - Riesgo 4'),
        (maximo, 'Máximo - Riesgo 5'),
    )


    TIPOCONTRATO_CHOICES = (
        (Termino_Fijo, 'Termino Fijo'),
        (Termino_Indefinido, 'Término Indefinido'),
        (Obra_o_Labor, 'Obra o Labor'),
        (Aprendizaje, 'Aprendizaje'),
        (Practicas, 'Prácticas'),
    )

    # tipo de trabajador

    DEPENDIENTE = '1'
    SERVICIO_DOMESTICO = '2'
    INDEPENDIENTE = '3'
    MADRE_COMUNITARIA = '4'
    SENA_LECTIVA = '12'
    INDEPENDIENTE_AGREMIADO = '16'
    SENA_PRODUCTIVA = '19'
    ESTUDIANTES_LEY_789_2002 = '20'
    ESTUDIANTES_POSTGRADO_SALUD = '21'
    ESTUDIANTES_RIESGOS_LABORALES = '23'
    INDEPENDIENTE_CONTRATO_SERVICIOS = '59'

    TIPO_TRABAJADOR_CHOICES = (
        (DEPENDIENTE, 'Dependiente'),
        (SERVICIO_DOMESTICO, 'Servicio domestico'),
        (INDEPENDIENTE, 'Independiente'),
        (MADRE_COMUNITARIA, 'Madre comunitaria'),
        (SENA_LECTIVA, 'Aprendices del Sena en etapa lectiva'),
        (INDEPENDIENTE_AGREMIADO, 'Independiente agremiado o asociado'),
        (SENA_PRODUCTIVA, 'Aprendices del SENA en etapa productiva'),
        (ESTUDIANTES_LEY_789_2002, 'Estudiantes (régimen especial ley 789 de 2002)'),
        (ESTUDIANTES_POSTGRADO_SALUD, 'Estudiantes de postgrado en salud'),
        (ESTUDIANTES_RIESGOS_LABORALES, 'Estudiantes aportes solo riesgos laborales'),
        (INDEPENDIENTE_CONTRATO_SERVICIOS, 'Independiente con contrato de prestación de servicios superior a 1 mes'),
    )

    id               = models.AutoField(primary_key = True)
    salarioBase      = models.FloatField(default=0)
    valorDia         = models.FloatField(default=0)
    noContrato       = models.CharField('N° Contrato', max_length=50)
    tipoContrato      = models.CharField('tipo Contrato', max_length=80, choices=TIPOCONTRATO_CHOICES)
    tipoTrabajador    = models.CharField('tipo Trabajador', max_length=80, choices=TIPO_TRABAJADOR_CHOICES)
    fechaInicioContrato = models.DateField('Fecha inicio contrato:', auto_now=False, auto_now_add=False)
    fechaFinalContrato = models.DateField('Fecha final contrato:', auto_now=False, auto_now_add=False)
    eps              = models.ForeignKey(Eps, on_delete=models.PROTECT, related_name="eps_empleado", blank=True, null=True)
    arl              = models.ForeignKey(Arl, on_delete=models.PROTECT, related_name="arl_empleado", blank=True, null=True)
    fondoPension     = models.ForeignKey(FondoPension, on_delete=models.PROTECT, related_name="fondoPension_empleado", blank=True, null=True)
    fondoCesantias   = models.ForeignKey(FondoCesantias, on_delete=models.PROTECT, related_name="fondoPension_empleado", blank=True, null=True)
    cajaCompensacion = models.ForeignKey(CajaCompensacion, on_delete=models.PROTECT,related_name="caja_empleado", blank=True, null=True)
    icbf             = models.ForeignKey(ICBF, on_delete=models.PROTECT,related_name="icbf_empleado", blank=True, null=True)
    sena             = models.ForeignKey(Sena, on_delete=models.PROTECT,related_name="sena_empleado", blank=True, null=True)
    riesgo           = models.FloatField('Riegos:', choices=RIESGOS_CHOICES)
    usuario          = models.ForeignKey(to="users.User", on_delete=models.PROTECT, related_name="usuario_contrato_creacion")
    deduccionesRecurrentes = models.ManyToManyField(DeduccionRecurrente,  related_name="deduccionRecurrente_empleado", blank=True, null=True)
    ingresosRecurrentes = models.ManyToManyField(IngresoRecurrente,  related_name="ingresoRecurrente_empleado", blank=True, null=True)


    @classmethod
    def actualizar_contrato(cls, contrato_id, formulario, user):
        from datetime import datetime
        from apps.configuracion.models import Terceros
        
        actContrato = cls.objects.get(id=contrato_id)
        
        salario_data = formulario.get('salarioBase')  
        if salario_data is not None:    
            actContrato.salarioBase = formulario.get('salarioBase',actContrato.salarioBase)
        
        riesgo_data=formulario.get('riesgo')
        if riesgo_data is not None:
            actContrato.riesgo = float(riesgo_data['valor'])
            
        tipoContrato_data=formulario.get('tipoContrato')
        if tipoContrato_data is not None:
            actContrato.tipoContrato=(tipoContrato_data['valor'])
            
        ingreso_recurrente_data = formulario.get('ingresosRecurrentes')
        if ingreso_recurrente_data is not None:
        # Obtén o crea la instancia de IngresoRecurrente
            instancia = IngresoRecurrente.objects.create(**ingreso_recurrente_data)
        # Agrega la instancia a la relación many-to-many sin eliminar las existentes
            actContrato.ingresosRecurrentes.add(instancia)
            
        
        
        arl_data = formulario.get('arl')
        if arl_data is not None:
            arl_instancia = Arl.objects.get(id=arl_data['id'])
            actContrato.arl = arl_instancia
         
            
        eps_data = formulario.get('eps')
        if eps_data is not None:
            eps_instancia = Eps.objects.get(id=eps_data['id'])
            actContrato.eps = eps_instancia
        
            
        pension_data = formulario.get('fondoPension')
        if pension_data is not None:
            pension_instancia = FondoPension.objects.get(id=pension_data['id'])
            actContrato.fondoPension = pension_instancia
        
            
        cesantias_data = formulario.get('fondoCesantias')
        if cesantias_data is not None:
            cesantias_instancia = FondoCesantias.objects.get(id=cesantias_data['id'])
            actContrato.fondoCesantias = cesantias_instancia
            
        caja_data = formulario.get('cajaCompensacion')
        if caja_data is not None:
            caja_instancia = CajaCompensacion.objects.get(id=caja_data['id'])
            actContrato.cajaCompensacion = caja_instancia
            
        fechaInicial_data = datetime.strptime(formulario['fechaInicioContrato'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if fechaInicial_data is not None:      
            actContrato.fechaInicioContrato = fechaInicial_data.strftime("%Y-%m-%d")
        
        fechaFinal_data = datetime.strptime(formulario['fechaFinalContrato'], "%Y-%m-%dT%H:%M:%S.%fZ").date()      
        if fechaFinal_data is not None:
            actContrato.fechaFinalContrato = fechaFinal_data.strftime("%Y-%m-%d")
            
        actContrato.save()

        return actContrato
    
    # TODO: Define fields here
    class Meta:
        """Meta definition for Contrato."""

        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
    
    


    def __str__(self):
        """Unicode representation of Contrato."""
        return self.noContrato




class Empleado(models.Model):
    """Model definition for Empleado."""

    # forma De Pago
    noDefinido      = '1'
    efectivo        = '10'
    transferencia   = '42'


    FORMADEAPGO_CHOICES = (
        (noDefinido, 'Instrumento no definido'),
        (efectivo, 'Efectivo'),
        (transferencia, 'Consignación bancaria'),
      
    )

    # TIPOS DE DOCUMENTOS
    CC = '1'
    CE = '2'
    TI = '3'
    PA = '4'

    TIPOSDOCUMENTOS_CHOICES = (
        (CC, 'Cédula de ciudadanía'),
        (CE, 'Cédula de extranjería'),
        (TI, 'Tarjeta de identidad'),
        (PA, 'Pasaporte'),
    )
    

    # TODO: Define fields here

    id               = models.AutoField(primary_key = True)
    foto             = models.TextField(blank=True, null=True)
    primerNombre     = models.CharField('Primer nombre:', max_length=150)
    segundoNombre    = models.CharField('Segundo nombre:', max_length=150)
    primerApellido   = models.CharField('Primer apellido:', max_length=150)
    segundoApellido  = models.CharField('Segundo apellido:', max_length=150)
    tipoDocumento    = models.CharField('Tipo de documento:', choices=TIPOSDOCUMENTOS_CHOICES,default=CC, max_length=5)
    documento        = models.CharField('Documento:', max_length=60 , unique = True)
    fechaNacimiento  = models.DateField('nacimiento:', auto_now=False, auto_now_add=False)
    correo           = models.EmailField('correo:', max_length=254, blank=True, null=True)
    telefono         = models.CharField( 'Telefono',max_length=150,blank=True, null=True)
    direccion        = models.CharField('Dirección:', max_length=150, blank=True, null=True)
    Cargo            = models.CharField('Cargo', max_length=150, blank=True, null=True)
    tercero          = models.ForeignKey(to="configuracion.Terceros", related_name="empleado_Tercero", on_delete=models.PROTECT)
    banco            = models.CharField('Banco:', max_length=150, blank=True, null=True)
    formaDepago      = models.CharField('Forma de pago:', max_length=50, choices=FORMADEAPGO_CHOICES, default=transferencia, blank=True, null=True)
    noCuenta         = models.CharField('N° de cuenta:', max_length=150, blank=True, null=True)
    contrato         = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='contrato_empleado')
    activo           = models.BooleanField(default=True)
    usuario          = models.ForeignKey(to="users.User", on_delete=models.PROTECT, related_name="usuario_empleado_creacion")
    
    @classmethod
    def crear_empleado_con_contrato(cls, formulario, user):
        from datetime import datetime
        from apps.configuracion.models import Terceros
       
      
        fecha_nacimiento =  datetime.strptime(formulario['fechaNacimiento'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Formatear el objeto datetime como una cadena "YYYY-MM-DD"
        fecha_nacimiento = fecha_nacimiento.strftime("%Y-%m-%d")

        tercero = Terceros.objects.get(id = formulario['tercero'] )

        with transaction.atomic():
            nombres   = formulario['nombres'].split(" ")
            apellidos = formulario['apellidos'].split(" ")
            empleado = Empleado(
                foto = formulario['foto'],
                primerNombre=nombres[0],
                segundoNombre=nombres[1],
                primerApellido=apellidos[0],
                segundoApellido=apellidos[1],
                tipoDocumento=formulario['tipoDocumento'],
                documento=formulario['documento'],
                fechaNacimiento=fecha_nacimiento,
                correo=formulario['correo'],
                telefono=formulario['telefono'],
                direccion=formulario['direccion'],
                Cargo=formulario['cargo'],
                tercero=tercero,
                banco=formulario['banco'],
                formaDepago=formulario['formaDePago'],
                noCuenta=formulario['noCuenta'],
                usuario = user
                # Resto de los campos...
            )

            fecha_inicio_contrato =  datetime.strptime(formulario['fechaInicioContrato'], "%Y-%m-%dT%H:%M:%S.%fZ")
            # Formatear el objeto datetime como una cadena "YYYY-MM-DD"
            fecha_inicio_contrato = fecha_inicio_contrato.strftime("%Y-%m-%d")

            fecha_final_contrato =  datetime.strptime(formulario['fechaFinalContrato'], "%Y-%m-%dT%H:%M:%S.%fZ")
            # Formatear el objeto datetime como una cadena "YYYY-MM-DD"
            fecha_final_contrato = fecha_final_contrato.strftime("%Y-%m-%d")


            eps_id              = Eps.objects.get(id            = formulario['eps'] )
            arl_id              = Arl.objects.get(id            = formulario['arl'] )
            fondoPension_id     = FondoPension.objects.get(id   = formulario['fondoPension'] )
            fondoCesantias_id   = FondoCesantias.objects.get(id = formulario['fondoCesantias'] )
            cajaCompensacion_id = CajaCompensacion.objects.get(id = formulario['cajaCompensacion'] )
            # ingresosRecurrentes_id = IngresoRecurrente.objects.get('ingresosRecurrentes',ingresosRecurrentes_id )
            # deduccionesRecurrentes_id = DeduccionRecurrente.objects.get('deduccionesRecurrentes',deduccionesRecurrentes_id )
            
            deduccionesRecurrentes = formulario.get('deduccionesRecurrentes', [])  # Obtén la lista de identificadores

            deduccionesRecurrentes_id = []  # Inicializa una lista para almacenar los objetos DeduccionRecurrente

            for deduccion_id in deduccionesRecurrentes:
                try:
                    deduccion_instancia = DeduccionRecurrente.objects.get(id=deduccion_id)
                    deduccionesRecurrentes_id.append(deduccion_instancia)
                except DeduccionRecurrente.DoesNotExist:
                    # Manejo de excepción si no se encuentra el objeto con el ID dado
                    pass
                
            ingresosRecurrentes = formulario.get('ingresosRecurrentes', [])  # Obtén la lista de identificadores

            ingresosRecurrentes_id = []  # Inic
                
            for ingreso_id in ingresosRecurrentes:
                try:
                    ingreso_instancia = IngresoRecurrente.objects.get(id=ingreso_id)
                    ingresosRecurrentes_id.append(ingreso_instancia)
                except IngresoRecurrente.DoesNotExist:
                    # Manejo de excepción si no se encuentra el objeto con el ID dado
                    pass


            contrato = Contrato.objects.create(
                salarioBase=float(formulario['salarioBase']),
                valorDia=float(formulario['salarioBase'])/30,
                eps=eps_id,
                arl=arl_id,
                fondoPension=fondoPension_id,
                fondoCesantias=fondoCesantias_id,
                cajaCompensacion=cajaCompensacion_id,
                riesgo=formulario['riesgo'],
                fechaInicioContrato=fecha_inicio_contrato,
                fechaFinalContrato=fecha_final_contrato,
                noContrato=formulario['noContrato'],
                tipoContrato=formulario['tipoContrato'],
                tipoTrabajador=formulario['tipoTrabajador'],
                usuario = user,
                # Resto de los campos...
            )
            contrato.ingresosRecurrentes.set([ingreso.id for ingreso in ingresosRecurrentes_id])

            contrato.deduccionesRecurrentes.set([deduccion.id for deduccion in deduccionesRecurrentes_id])

            empleado.contrato = contrato
            empleado.save()
            return empleado
        
    @classmethod
    def actualizar_empleado_con_contrato_datos_personales(cls, empleado_id, formulario, user):
        from datetime import datetime
        from apps.configuracion.models import Terceros
        
        
        actEmpleado = cls.objects.get(id=empleado_id)
        actEmpleado.primerNombre = formulario.get('primerNombre', actEmpleado.primerNombre)
        actEmpleado.segundoNombre = formulario.get('segundoNombre', actEmpleado.segundoNombre)
        actEmpleado.segundoNombre = formulario.get('segundoNombre', actEmpleado.segundoNombre)
        
        actEmpleado.primerApellido = formulario.get('primerApellido', actEmpleado.primerApellido)
        actEmpleado.segundoApellido = formulario.get('segundoApellido', actEmpleado.segundoApellido)
        
        actEmpleado.documento = formulario.get('documento', actEmpleado.documento)
        
        fecha_nacimiento = datetime.strptime(formulario['fechaNacimiento'], "%Y-%m-%dT%H:%M:%S.%fZ").date()      
        actEmpleado.fechaNacimiento = fecha_nacimiento.strftime("%Y-%m-%d")
        
        actEmpleado.correo = formulario.get('correo', actEmpleado.correo)
        
        actEmpleado.telefono = formulario.get('telefono', actEmpleado.telefono)
        
        actEmpleado.direccion = formulario.get('direccion', actEmpleado.direccion)
        
        actEmpleado.Cargo = formulario.get('Cargo', actEmpleado.Cargo)
        
        actEmpleado.banco = formulario.get('banco', actEmpleado.banco)
        
        actEmpleado.noCuenta = formulario.get('noCuenta', actEmpleado.noCuenta)
        
        formaDePago_data=formulario.get('formaDepago')
        if formaDePago_data is not None:
            actEmpleado.formaDepago=(formaDePago_data['valor'])

        actEmpleado.save()

        return actEmpleado

    

    class Meta:
        """Meta definition for Empleado."""

        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        """Unicode representation of Empleado."""
        return f'Primer Nombre:{self.primerNombre} Primer Apellido:{self.primerApellido}'
    
    
class Nomina(models.Model):
    id = models.AutoField(primary_key=True)
    numeracion = models.CharField('Numeración:', max_length=255)
    prefijo = models.CharField('Prefijo:', max_length=255)
    consecutivo = models.IntegerField('Consecutivo:')
    numero = models.IntegerField('Número:')
    fecha_inicio_pago = models.FloatField('Fecha de inicio de pago:')
    fecha_fin_pago = models.FloatField('Fecha de fin de pago:')
    total_pago = models.FloatField('Total de pago:')
    total_vacaciones = models.FloatField('Total de vacaciones:')
    total_primas = models.FloatField('Total de primas:' )
    total_cesantias = models.FloatField('Total de cesantías:' )
    total_c_intereses = models.FloatField('Total de intereses sobre cesantías:' )
    numero_trabajadores = models.IntegerField('Número de trabajadores:')
    total_salud = models.FloatField('Total de aportes a salud:' )
    total_pension = models.FloatField('Total de aportes a pensión:')
    total_arl = models.FloatField('Total de aportes a ARL:' )
    total_caja = models.FloatField('Total de aportes a caja de compensación:')

    def __str__(self):
        return f'Nomina {self.id} - {self.fecha_inicio_pago} a {self.fecha_fin_pago}'
    
class NominaDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    fk_nomina = models.ForeignKey(Nomina, on_delete=models.PROTECT, verbose_name='Nómina relacionada',related_name='detalles_nomina')
    fk_numeracion = models.ForeignKey(to='configuracion.numeracion',on_delete=models.PROTECT, max_length=255, related_name='numeracion_nomina_detalle')
    numero = models.IntegerField('Número:')
    consecutivo = models.IntegerField('Consecutivo:')
    prefijo = models.CharField('Prefijo:', max_length=255)
    fk_contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, verbose_name='Contrato relacionado')
    fk_descuentos = models.ForeignKey(DeduccionRecurrente, on_delete=models.PROTECT, verbose_name='Descuentos relacionados')
    fk_ingresos = models.ForeignKey(IngresoRecurrente, on_delete=models.PROTECT, verbose_name='Ingresos relacionados')
    salario_base = models.FloatField('Salario base:')
    auxilio = models.FloatField('Auxilio:')
    dias_trabajados = models.IntegerField('Días trabajados:')
    pago_base = models.FloatField('Pago base:')
    total_tra_salud = models.FloatField('Total trabajador aportes salud:')
    total_tra_pension = models.FloatField('Total trabajador aportes pensión:')
    total_emp_arl = models.FloatField('Total empleador aportes ARL:')
    total_emp_eps = models.FloatField('Total empleador aportes EPS:')
    total_emp_pension = models.FloatField('Total empleador aportes pensión:')
    total_emp_cesantias = models.FloatField('Total empleador aportes cesantías:')
    total_emp_intereses = models.FloatField('Total empleador intereses sobre cesantías:')
    total_primas = models.FloatField('Total primas:')
    total_vacaciones = models.FloatField('Total vacaciones:')

    def __str__(self):
        return f'Detalle de Nómina {self.id} - Nómina: {self.fk_nomina} - Contrato: {self.fk_contrato}'




