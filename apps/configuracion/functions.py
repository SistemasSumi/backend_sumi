from rest_framework import serializers
from django.db import transaction
from .validations import validarCliente,validarProveedor
from .models import *
from apps.configuracion.models import puc
from django.db.models import Q
from django.utils import timezone
from .serializers import TercerosCreateSerializer

def saveTercero(create,tercero):
    if create:
        if Terceros.objects.filter(documento=tercero['documento']).exists():
            raise serializers.ValidationError('Ya existe un tercero con este documento.')
    if tercero['isCliente']:
        validarCliente(tercero)
    if tercero['isProveedor']:
        validarProveedor(tercero)

    t = None
    # descuentoC   = None  
    # descuentoP   = None
    # retencionesC = None
    # retencionesP = None
    id = 0
    if tercero['id']:
        id = tercero['id']
    if Terceros.objects.filter(id=id).exists():
        t            = Terceros.objects.get(id=tercero['id'])
        # if descuentoCliente:
        #     descuentoC   = PlazosDecuentosClientes.objects.get(id=descuentoCliente['id']).delete()
        # if descuentoProveedor:
        #     descuentoP   = PlazosDecuentosProveedores.objects.get(id=descuentoProveedor['id']).delete()
        # if retencionesClientes:
        #     retencionesC = RetencionesClientes.objects.filter(tercero=t.id).delete()
        # if retencionesProveedor:
        #     retencionesP = RetencionesProveedor.objects.filter(tercero=t.id).delete()
    else:
        t            = Terceros()
        # descuentoC   = PlazosDecuentosClientes()  
        # descuentoP   = PlazosDecuentosProveedores()
        # retencionesC = RetencionesClientes()
        # retencionesP = RetencionesProveedor()
    

    departamento     = Departamentos.objects.get(id = tercero['departamento'])
    municipio        = Municipios.objects.get(id = tercero['municipio'])
    formaDePago      = FormaPago.objects.get(id = tercero['formaPago'])

    
    t.tipoDocumento            = tercero['tipoDocumento']
    t.documento                = tercero['documento']
    t.dv                       = tercero['dv']
    t.nombreComercial          = tercero['nombreComercial']
    t.nombreContacto           = tercero['nombreContacto']
    t.direccion                = tercero['direccion']
    t.departamento             = departamento
    t.municipio                = municipio
    t.telefonoContacto         = tercero['telefonoContacto']
    t.correoContacto           = tercero['correoContacto']
    t.correoFacturas           = tercero['correoFacturas']

    if tercero['isCliente']:
        vendedor = VendedoresClientes.objects.get(id = tercero['vendedor'])
        c_cobrar = puc.objects.get(id = tercero['cuenta_x_cobrar'])
        c_saldo  = puc.objects.get(id = tercero['cuenta_saldo_a_cliente'])

        t.vendedor  = vendedor
        t.cuenta_x_cobrar        = c_cobrar
        t.cuenta_saldo_a_cliente = c_saldo 
    
    t.formaPago                = formaDePago
    t.tipoPersona              = tercero['tipoPersona']
    t.regimen                  = tercero['regimen']
    t.matriculaMercantil       = tercero['matriculaMercantil']
    t.codigoPostal             = tercero['codigoPostal']
    t.isCliente                = tercero['isCliente']
    t.isProveedor              = tercero['isProveedor']
    t.isCompras                = tercero['isCompras']
    t.isContabilidad           = tercero['isContabilidad']
    t.isElectronico            = tercero['isElectronico']
    t.isPos                    = tercero['isPos']

    if tercero['isProveedor']:
        p_pagar  = puc.objects.get(id = tercero['cuenta_x_pagar'])
        p_saldo  = puc.objects.get(id = tercero['cuenta_saldo_a_proveedor'])

        t.cuenta_x_pagar           = p_pagar  
        t.cuenta_saldo_a_proveedor = p_saldo  
        
    with transaction.atomic():
        t.save()
        # if descuentoCliente:
        #     descuentoC.tercero        = t
        #     descuentoC.quince         = descuentoCliente['quince']
        #     descuentoC.treinta        = descuentoCliente['treinta']
        #     descuentoC.cuarentaYcinco = descuentoCliente['cuarentaycinco']
        #     descuentoC.sesenta        = descuentoCliente['sesenta']
        #     descuentoC.noventa        = descuentoCliente['noventa']
        #     descuentoC.save()
        
        # if descuentoProveedor: 
        #     descuentoP.tercero        = t
        #     descuentoP.quince         = descuentoProveedor['quince']
        #     descuentoP.treinta        = descuentoProveedor['treinta']
        #     descuentoP.cuarentaYcinco = descuentoProveedor['cuarentaycinco']
        #     descuentoP.sesenta        = descuentoProveedor['sesenta']
        #     descuentoP.noventa        = descuentoProveedor['noventa']
        #     descuentoP.save()
        
        # if retencionesClientes:

        #     lista = []
        #     for x in retencionesClientes:
        #         j = x['retencion']
        #         r = Retenciones.objects.get(id = j['id']) 
        #         RTF = RetencionesClientes(
        #             tercero   = t,
        #             retencion = r,
        #             fija      = x['fija']
        #         )
        #         RTF.save()
        # if retencionesProveedor:
        #     lista = []
        #     for x in retencionesProveedor:
        #         j = x['retencion']
        #         print(j)
        #         r = Retenciones.objects.get(id = j['id']) 
        #         RTF = RetencionesProveedor(
        #             tercero   = t,
        #             retencion = r,
        #             fija      = x['fija']
        #         )
        #         RTF.save()
        return t



def getTerceros(tipo):
    if tipo == 'TODOS':
        return Terceros.objects.all().select_related('listaPrecios','vendedor','cuenta_x_cobrar','cuenta_x_pagar','cuenta_saldo_a_cliente','cuenta_saldo_a_proveedor','formaPago','departamento','municipio').prefetch_related('retencion_cliente','retencion_proveedor','plazos_clientes','plazos_proveedores','datos_bancarios').order_by('nombreComercial') 
    if tipo == 'CLIENTE':
        return Terceros.objects.filter(isCliente = True).select_related('vendedor','cuenta_x_cobrar','cuenta_x_pagar','cuenta_saldo_a_cliente','cuenta_saldo_a_proveedor','formaPago','departamento','municipio').prefetch_related('retencion_cliente','retencion_proveedor','plazos_clientes','plazos_proveedores','datos_bancarios').order_by('nombreComercial')
    if tipo == 'PROVEEDOR':
        return Terceros.objects.filter(isProveedor = True).select_related('vendedor','cuenta_x_cobrar','cuenta_x_pagar','cuenta_saldo_a_cliente','cuenta_saldo_a_proveedor','formaPago','departamento','municipio').prefetch_related('retencion_cliente','retencion_proveedor','plazos_clientes','plazos_proveedores','datos_bancarios').order_by('nombreComercial')
    


def saveDescuentoProveedor(descuentoProveedor):
    tercero = Terceros.objects.get(id = descuentoProveedor['tercero'])
    descuentoP   = PlazosDecuentosProveedores()

    with transaction.atomic():
        descuentoP.tercero        = tercero
        descuentoP.quince         = descuentoProveedor['quince']
        descuentoP.treinta        = descuentoProveedor['treinta']
        descuentoP.cuarenta       = descuentoProveedor['cuarenta']
        descuentoP.cuarentaYcinco = descuentoProveedor['cuarentaycinco']
        descuentoP.sesenta        = descuentoProveedor['sesenta']
        descuentoP.noventa        = descuentoProveedor['noventa']
        descuentoP.save()
    

def saveRetencionCliente(retencionesCliente):
    tercero = Terceros.objects.get(id = retencionesCliente['tercero'])  
    with transaction.atomic():
        j = retencionesCliente['retencion']
        print(j)
        r = Retenciones.objects.get(id = j['id']) 
        RTF = RetencionesClientes(
            tercero   = tercero,
            retencion = r,
            fija      = retencionesCliente['fija']
        )
        RTF.save()
    
def saveRetencionProveedor(retencionesProveedor):
    tercero = Terceros.objects.get(id = retencionesProveedor['tercero'])  
    with transaction.atomic():
        j = retencionesProveedor['retencion']
        print(j)
        r = Retenciones.objects.get(id = j['id']) 
        RTF = RetencionesProveedor(
            tercero   = tercero,
            retencion = r,
            fija      = retencionesProveedor['fija']
        )
        RTF.save()
    



def saveContacto(contacto):
    tercero = Terceros.objects.get(id = contacto['tercero'])  

    conta = DatosContacto()
    with transaction.atomic():
        conta.tipo    = contacto['tipo']
        conta.nombre  = contacto['nombre']
        conta.correo  = contacto['correo']
        conta.telefono  = contacto['telefono']
        conta.tercero = tercero
        conta.save()


def saveBanco(banco):
    tercero = Terceros.objects.get(id = banco['tercero'])  

    b = DatosBancarios()
    with transaction.atomic():
        b.tipo    = banco['tipo']
        b.banco   = banco['banco']
        b.cuenta  = banco['cuenta']
        b.tercero = tercero
        b.save()

def setDeaultTercerosProvedores(archivo):
    listado = []
    for x in archivo:
        tercero = Terceros()

        f = FormaPago.objects.get(nombre = x['formaPago'])
        tercero.formaPago = f

        documento                =  x['documento'].split('-')
        if Terceros.objects.filter(documento = documento[0]).exists():
            print(documento[0])
            tercero = Terceros.objects.get(documento = documento[0])
        tercero.tipoDocumento    =  x['tipoDocumento']
        tercero.documento        =  documento[0]
        if tercero.tipoDocumento == "NIT": 
            if len(documento) > 1:
                tercero.dv           =  documento[1]
        tercero.nombreComercial  =  x['nombre']
        tercero.direccion        = x['direccion']


        if x["departamento"] != "":
            depa = Departamentos.objects.get(departamento = x["departamento"])
        else:
            depa = Departamentos.objects.get(departamento = "Magdalena")
        
        tercero.departamento = depa


        if x["municipio"] != "":
       
            muni = Municipios.objects.get(municipio = x["municipio"], departamento__id = depa.id)
        else:
         

            muni = Municipios.objects.get(municipio = "Santa Marta",departamento__id = depa.id)
        
        tercero.municipio        = muni
        tercero.telefonoContacto = x['telefonoContacto']
        tercero.correoContacto   = x['emailContacto']
        tercero.tipoPersona      = x['tipoPersona']
        tercero.isProveedor      = x['isProveedor']
        tercero.isCompras        = x['isCompras']

        tercero.formaPago = FormaPago.objects.get(id = 1)



        cuenta_P = puc.objects.get(codigo = x['cuenta_x_pagar'])
        cuenta_s = puc.objects.get(codigo = x['cuenta_saldo_a_favor'])


        tercero.cuenta_x_pagar            = cuenta_P
        tercero.cuenta_saldo_a_proveedor  = cuenta_s

        tercero.save()
    return archivo


def setDeaultTercerosClientes(archivo):
    listado = []
    for x in archivo:
        tercero = Terceros()
        documento                =  x['documento'].split('-')

        lista = ListaDePrecios.objects.get(id = x['lista'])

        usuario = User.objects.get(id = 1)

        vendedor = VendedoresClientes.objects.get_or_create(nombre = x['vendedor'],usuario = usuario)[0]

        if Terceros.objects.filter(documento = documento[0]).exists():
            print(documento[0])
            tercero = Terceros.objects.get(documento = documento[0])
            tercero.isCliente = True
            if x['isPos'] == 1:
                tercero.isPos = True
            else:
                tercero.isElectronico = True
            tercero.listaPrecios = lista
            tercero.tipoPersona = x['tipoPersona']
            tercero.codigoPostal       = x['codigoPostal']
            if 'matriculaMercantil' in x:
                tercero.matriculaMercantil = x['matriculaMercantil']
            tercero.codigoPostal       = x['codigoPostal']
            if 'correoFacturas' in x:
                tercero.correoFacturas = x['correoFacturas']
            tercero.vendedor = vendedor
            tercero.telefonoContacto = x['telefonoContacto']
            cuenta_P = puc.objects.get(codigo = x['cuenta_x_cobrar'])
            cuenta_s = puc.objects.get(codigo = x['cuenta_saldo_a_favor'])


            tercero.cuenta_x_cobrar           = cuenta_P
            tercero.cuenta_saldo_a_cliente   = cuenta_s

            
        
            
        else:
            tercero.tipoDocumento    =  x['tipoDocumento']
            tercero.documento        =  documento[0]
            tercero.tipoPersona = x['tipoPersona']
            if tercero.tipoDocumento == "NIT": 
                if len(documento) > 1:
                    tercero.dv           =  documento[1]
            tercero.nombreComercial  =  x['nombre']
            tercero.direccion        = x['direccion']
            tercero.isCliente = True
            if x['isPos'] == 1:
                tercero.isPos = True
            else:
                tercero.isElectronico = True
            tercero.listaPrecios = lista
            if 'matriculaMercantil' in x:
                tercero.matriculaMercantil = x['matriculaMercantil']
            tercero.codigoPostal       = x['codigoPostal']
            if 'correoFacturas' in x:
                tercero.correoFacturas = x['correoFacturas']
            
            tercero.vendedor = vendedor
            tercero.telefonoContacto = x['telefonoContacto']
            cuenta_P = puc.objects.get(codigo = x['cuenta_x_cobrar'])
            cuenta_s = puc.objects.get(codigo = x['cuenta_saldo_a_favor'])


            tercero.cuenta_x_cobrar           = cuenta_P
            tercero.cuenta_saldo_a_cliente    = cuenta_s
        
            f = FormaPago.objects.get(nombre = x['formaPago'])
            tercero.formaPago = f


            if 'departamento' in x:
                if x["departamento"] != "":
                    try:
                        depa = Departamentos.objects.filter(departamento__iexact = x["departamento"])[0]
                    except:
                        depa = Departamentos.objects.filter(departamento__iexact = x["departamento"])[0]

                else:
                    depa = Departamentos.objects.get(departamento = "Magdalena")
            else:
                depa = Departamentos.objects.get(departamento = "Magdalena")
                


            tercero.departamento = depa

            if 'municipio' in x:
                if x["municipio"] != "":
                    
                    try:
                        muni = Municipios.objects.get(municipio__iexact = x["municipio"])
                    except:
                        muni = Municipios.objects.get(municipio = "Santa Marta")

                else:
            
                    muni = Municipios.objects.get(municipio = "Santa Marta")
            else:
                muni = Municipios.objects.get(municipio = "Santa Marta")
            tercero.municipio = muni

        tercero.save()
    return archivo



def setDeaultTercerosProveedoresFormaPago(archivo):
    listado = []
    for x in archivo:
        tercero = Terceros()

        
        documento                =  x['documento'].split('-')
        if Terceros.objects.filter(documento = documento[0]).exists():
            print(documento[0])
            tercero = Terceros.objects.get(documento = documento[0])
      
            f = FormaPago.objects.get(nombre = x['formaPago'])
            tercero.formaPago = f
            tercero.save()
    return archivo





def getProveedoresCompras():
    return Terceros.objects.filter(isProveedor = True, isCompras = True).select_related('vendedor','cuenta_x_cobrar','cuenta_x_pagar','cuenta_saldo_a_cliente','cuenta_saldo_a_proveedor','formaPago','departamento','municipio').prefetch_related('retencion_cliente','retencion_proveedor','plazos_clientes','plazos_proveedores').order_by('nombreComercial')



def getClientesElectronicos():
    return Terceros.objects.filter(isCliente = True, isElectronico = True).select_related('listaPrecios','vendedor','cuenta_x_cobrar','cuenta_x_pagar','cuenta_saldo_a_cliente','cuenta_saldo_a_proveedor','formaPago','departamento','municipio').prefetch_related('retencion_cliente','retencion_proveedor','plazos_clientes','plazos_proveedores').order_by('nombreComercial')


def getClientesPos():
    return Terceros.objects.filter(isCliente = True, isPos = True).select_related('listaPrecios','vendedor','cuenta_x_cobrar','cuenta_x_pagar','cuenta_saldo_a_cliente','cuenta_saldo_a_proveedor','formaPago','departamento','municipio').prefetch_related('retencion_cliente','retencion_proveedor','plazos_clientes','plazos_proveedores').order_by('nombreComercial')

def getTercero(id):
    print(id)
    return Terceros.objects.select_related('listaPrecios','vendedor','cuenta_x_cobrar','cuenta_x_pagar','cuenta_saldo_a_cliente','cuenta_saldo_a_proveedor','formaPago','departamento','municipio').prefetch_related('retencion_cliente','retencion_proveedor','plazos_clientes','plazos_proveedores').get(id=id)



def obtenerNumeracion(tipo):
       
    num = numeracion()
    if tipo == 'orden':
        num = numeracion.objects.filter(tipoDocumento = num.ORDEN_COMPRA, estado = True)
        return num
    elif tipo == 'ingreso':
        num = numeracion.objects.filter(tipoDocumento = num.INGRESO_ALMACEN, estado = True)
        return num
    elif tipo == 'notaCreditoCompras':
        num = numeracion.objects.filter(tipoDocumento = num.NOTA_CREDITO_COMPRAS, estado = True)
        return num
    elif tipo == 'ce':
        num = numeracion.objects.filter(tipoDocumento = num.COMPROBANTE_EGRESO, estado = True)
        return num
    elif tipo == 'ci':
        num = numeracion.objects.filter(tipoDocumento = num.COMPROBANTE_INGRESO, estado = True)
        return num
    elif tipo == 'tra':
        num = numeracion.objects.filter(tipoDocumento = num.TRASLADO_FONDOS, estado = True)
        return num
    elif tipo == 'mc':
        num = numeracion.objects.filter(tipoDocumento = num.COMPROBANTE_CONTABLE, estado = True)
        return num
    elif tipo == 'ajustes-inventario':
        num = numeracion.objects.filter(tipoDocumento = num.AJUSTE_INVENTARIO, estado = True)
        return num
    elif tipo == 'ventas':
        num = numeracion.objects.filter(
            Q(tipoDocumento = num.FACTURA_ELECTRONICA) | 
            Q(tipoDocumento = num.FACTURA_POS)|
            Q(tipoDocumento = num.PROFORMA)
        )
        num.filter(estado = True)
        return num
    elif tipo == 'notacredito':
        num = numeracion.objects.filter(
            Q(tipoDocumento = num.NOTA_CREDITO) | 
            Q(tipoDocumento = num.NOTA_CREDITO_POS)
        )
        num.filter(estado = True)
        return num


def actualizarRetencion(archivo):
    for x in archivo:
        print(x['tercero'])
        tercero = Terceros.objects.get(nombreComercial = x['tercero'])
        tercero.isRetencion = True
        tercero.save()



def crear_notificacion(usuario, mensaje, grupo, data, sender_user, receiver_users, tipo, vistas):
    # Crear un usuario emisor (si aún no existe)

    # Crear la notificación
    notificacion = Notificacion(
        id='notificacion_id',  # Sustituye 'notificacion_id' por el ID deseado
        usuario=usuario,
        mensaje=mensaje,
        grupo=grupo,
        data=data,
        sender_user=usuario,
        fecha=timezone.now(),
        tipo=tipo
    )

    # Guardar la notificación
    notificacion.save()

    # Agregar usuarios receptores a la notificación
    notificacion.receiver_users.set(receiver_users)

    # Agregar usuarios que han visto la notificación
    notificacion.vistas.set(vistas)

    from apps.users.serializers import NotificacionSerializer

    return NotificacionSerializer(notificacion).data  # Devuelve la notificación creada
