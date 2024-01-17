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
    concepto = models.ForeignKey(to="nomina.Concepto", on_delete=models.PROTECT)
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
    concepto = models.ForeignKey(to="nomina.Concepto", on_delete=models.PROTECT)
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
    concepto = models.ForeignKey(to="nomina.Concepto", on_delete=models.PROTECT)
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
    concepto = models.ForeignKey(to="nomina.Concepto", on_delete=models.PROTECT)
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
    concepto = models.ForeignKey(to="nomina.Concepto", on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)



    class Meta:
        """Meta definition for Sena."""

        verbose_name = 'Sena'
        verbose_name_plural = 'Sena'

    def __str__(self):
        """Unicode representation of Sena."""
        self.tercero.nombreComercial


class CajaCompensacion(models.Model):
    """Model definition for CajaCompensacion."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(to="nomina.Concepto", on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)



    class Meta:
        """Meta definition for Sena."""

        verbose_name = 'Caja de compensación'
        verbose_name_plural = 'Caja de compensaciones'

    def __str__(self):
        """Unicode representation of CajaCompensacion."""
        self.tercero.nombreComercial






class ICBF(models.Model):
    """Model definition for ICBF."""

    # TODO: Define fields here
    id       = models.AutoField(primary_key= True)
    concepto = models.ForeignKey(to="nomina.Concepto", on_delete=models.PROTECT)
    tercero  = models.ForeignKey(to="configuracion.Terceros", on_delete=models.PROTECT)



    class Meta:
        """Meta definition for ICBF."""

        verbose_name = 'ICBF'
        verbose_name_plural = 'ICBF'

    def __str__(self):
        """Unicode representation of ICBF."""
        self.tercero.nombreComercial
    





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
        print(formulario)
      
        fecha_nacimiento =  datetime.strptime(formulario['fechaNacimiento'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Formatear el objeto datetime como una cadena "YYYY-MM-DD"
        fecha_nacimiento = fecha_nacimiento.strftime("%Y-%m-%d")

        tercero = Terceros.objects.get(id = formulario['tercero'] )

        with transaction.atomic():
            nombres   = formulario['nombres'].split("-")
            apellidos = formulario['apellidos'].split("-")
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
                usuario = user
                # Resto de los campos...
            )
            empleado.contrato = contrato
            empleado.save()
            return empleado

    

    class Meta:
        """Meta definition for Empleado."""

        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        """Unicode representation of Empleado."""
        return f'Primer Nombre:{self.primerNombre} Primer Apellido:{self.primerApellido}'




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
