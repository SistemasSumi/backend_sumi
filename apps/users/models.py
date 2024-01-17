from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    GRUPO_CHOICES = (
        ('CONTABILIDAD', 'CONTABILIDAD'),
        ('FACTURACION', 'FACTURACIÓN'),
        ('LOGISTICA', 'LOGÍSTICA'),
        ('GENERAL', 'GENERAL'),
    )

    username    = models.CharField(max_length=20, unique=True)
    email       = models.EmailField(unique = True)
    nombres     = models.CharField(max_length=30, blank=True)
    apellidos   = models.CharField(max_length=30, blank=True)
    genero      = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    grupo       = models.CharField(max_length=50, choices=GRUPO_CHOICES, blank=True)
    avatar_url  = models.TextField(blank=True)
    empresa     = models.ForeignKey("configuracion.Empresa", on_delete=models.PROTECT, related_name="empresa_usuario", null=True, blank=True)
    #
    is_vendedor = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)

    USERNAME_FIELD  = 'username'

    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos






class PermisosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="permisos_usuario")
    superusuario = models.BooleanField(default=False)
    wtablas = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Usuario"
        verbose_name_plural = "Permisos de Usuarios"

class ContabilidadPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="contabilidad_permisos")
    puc = models.BooleanField(default=False)
    comprobantes_contables = models.BooleanField(default=False)
    informes = models.BooleanField(default=False)
    libro_auxiliar = models.BooleanField(default=False)
    conciliacion = models.BooleanField(default=False)
    traslados = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Contabilidad"
        verbose_name_plural = "Permisos de Contabilidad"

class FacturacionPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="facturacion_permisos")
    crear = models.BooleanField(default=False)
    proforma = models.BooleanField(default=False)
    cotizacion = models.BooleanField(default=False)
    listado = models.BooleanField(default=False)
    despachos = models.BooleanField(default=False)
    nota_credito = models.BooleanField(default=False)
    nota_debito = models.BooleanField(default=False)
    firmar_factura = models.BooleanField(default=False)
    dar_alta_factura = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Facturación"
        verbose_name_plural = "Permisos de Facturación"

class InventarioPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="inventario_permisos")
    bodegas = models.BooleanField(default=False)
    orden = models.BooleanField(default=False)
    crear_orden = models.BooleanField(default=False)
    ingresar_orden = models.BooleanField(default=False)
    productos = models.BooleanField(default=False)
    listado_productos = models.BooleanField(default=False)
    nota_credito = models.BooleanField(default=False)
    crear_nota_credito = models.BooleanField(default=False)
    ajuste = models.BooleanField(default=False)
    consumo = models.BooleanField(default=False)
    kardex = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Inventario"
        verbose_name_plural = "Permisos de Inventario"

class PagosPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="pagos_permisos")
    cxp = models.BooleanField(default=False)
    egresos = models.BooleanField(default=False)
    crear = models.BooleanField(default=False)
    pagos = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Pagos"
        verbose_name_plural = "Permisos de Pagos"

class CobrosPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="cobros_permisos")
    cxc = models.BooleanField(default=False)
    ingreso = models.BooleanField(default=False)
    crear = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Cobros"
        verbose_name_plural = "Permisos de Cobros"

class EmpleadosPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="empleados_permisos")
    crear = models.BooleanField(default=False)
    listado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Empleados"
        verbose_name_plural = "Permisos de Empleados"

class SettingsPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="settings_permisos")
    crear_user = models.BooleanField(default=False)
    ver_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Configuración"
        verbose_name_plural = "Permisos de Configuración"

class InformesPermisos(models.Model):
    permisos_usuario = models.ForeignKey(PermisosUsuario, on_delete=models.PROTECT, related_name="informes_permisos")
    inv_inventario = models.BooleanField(default=False)
    inv_inventario_vencido = models.BooleanField(default=False)
    oc_compras_detalladas = models.BooleanField(default=False)
    oc_rotacion_productos = models.BooleanField(default=False)
    oc_retenciones = models.BooleanField(default=False)
    fac_rotacion_productos = models.BooleanField(default=False)
    fac_ventas_detalladas = models.BooleanField(default=False)
    fac_ventas_x_vendedor = models.BooleanField(default=False)
    fac_retenciones = models.BooleanField(default=False)
    conta_balance_prueba = models.BooleanField(default=False)
    conta_estado_financiero = models.BooleanField(default=False)
    conta_estado_resultado = models.BooleanField(default=False)
    conta_libro_aux = models.BooleanField(default=False)
    conta_cxc = models.BooleanField(default=False)
    conta_cxp = models.BooleanField(default=False)
    conta_abonos_recibidos = models.BooleanField(default=False)
    cliente_estado_cartera = models.BooleanField(default=False)
    cliente_cartera_vencida = models.BooleanField(default=False)
    cliente_listado = models.BooleanField(default=False)
    proveedor_estado_cartera = models.BooleanField(default=False)
    proveedor_listado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Permisos de Informes"
        verbose_name_plural = "Permisos de Informes"
