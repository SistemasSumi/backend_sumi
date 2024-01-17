from rest_framework import serializers

def validarCliente(dataTercero):

    if dataTercero['tipoDocumento'] == None or dataTercero['tipoDocumento'] == '':
        raise serializers.ValidationError('El tipo de documento no puede ser nulo o vacio.')
    if dataTercero['documento'] == None or dataTercero['documento'] == '': 
        raise serializers.ValidationError('El documento no puede ser nulo o vacio.')
    if dataTercero['tipoDocumento'] == 'NIT':
        if dataTercero['dv'] == '' or dataTercero['dv'] == None:
            raise serializers.ValidationError('El Dígito de verificación no puede ser nulo, Si el tipo de documento es NIT.')
    if dataTercero['nombreComercial'] == None or dataTercero['nombreComercial'] == '':
        raise serializers.ValidationError('La Razón social o Nombre comercial no puede ser nulo o vacio.')
    if dataTercero['nombreContacto'] == None or dataTercero['nombreContacto'] == '':
        raise serializers.ValidationError('El nombre del contacto no puede ser nulo o vacio.')
    if dataTercero['direccion'] == None or dataTercero['direccion'] == '':
        raise serializers.ValidationError('La dirección no puede ser nula o vacia.')
    if dataTercero['departamento'] == None or dataTercero['departamento'] == '':
        raise serializers.ValidationError('El departamento no puede ser nulo o vacio.')
    if dataTercero['municipio'] == None or dataTercero['municipio'] == '':
        raise serializers.ValidationError('El municipio no puede ser nulo o vacio.')
    if dataTercero['telefonoContacto'] == None or dataTercero['telefonoContacto'] == '':
        raise serializers.ValidationError('El Telefono de contacto no puede ser nulo o vacio.')
    if dataTercero['correoContacto'] == None or dataTercero['correoContacto'] == '':
        raise serializers.ValidationError('El correo de contacto no puede ser nulo o vacio.')
    if dataTercero['correoFacturas'] == None or dataTercero['correoFacturas'] == '':
        raise serializers.ValidationError('El correo de facturas no puede ser nulo o vacio.')
    if dataTercero['vendedor'] == None or dataTercero['vendedor'] == '':
        raise serializers.ValidationError('El vendedor no puede ser nulo o vacio.')
    if dataTercero['formaPago'] == None or dataTercero['formaPago'] == '':
        raise serializers.ValidationError('La forma de Pago no puede ser nula o vacia.')
    if dataTercero['tipoPersona'] == None or dataTercero['tipoPersona'] == '':
        raise serializers.ValidationError('El tipo de persona no puede ser nula o vacia.')
    if dataTercero['regimen'] == None or dataTercero['regimen'] == '':
        raise serializers.ValidationError('El regimen no puede ser nulo o vacio.')
    if dataTercero['matriculaMercantil'] == None or dataTercero['matriculaMercantil'] == '':
        raise serializers.ValidationError('El regimen no puede ser nulo o vacio.')
    if dataTercero['codigoPostal'] == None or dataTercero['codigoPostal'] == '':
        raise serializers.ValidationError('El codigoPostal no puede ser nulo o vacio.')
    if dataTercero['cuenta_x_cobrar'] == None or dataTercero['cuenta_x_cobrar'] == '':
        raise serializers.ValidationError('Si el tercero es cliente la cuenta por cobrar no puede ser nula o vacia.')
    if dataTercero['cuenta_saldo_a_cliente'] == None or dataTercero['cuenta_saldo_a_cliente'] == '':
        raise serializers.ValidationError('Si el tercero es cliente la cuenta saldo a favor no puede ser nula o vacia.')

            






def validarProveedor(dataTercero):
    if dataTercero['tipoDocumento'] == None or dataTercero['tipoDocumento'] == '':
        raise serializers.ValidationError('El tipo de documento no puede ser nulo o vacio.')
    if dataTercero['documento'] == None or dataTercero['documento'] == '': 
        raise serializers.ValidationError('El documento no puede ser nulo o vacio.')
    if dataTercero['tipoDocumento'] == 'NIT':
        if dataTercero['dv'] == '' or dataTercero['dv'] == None:
            raise serializers.ValidationError('El Dígito de verificación no puede ser nulo, Si el tipo de documento es NIT.')
    if dataTercero['nombreComercial'] == None or dataTercero['nombreComercial'] == '':
        raise serializers.ValidationError('La Razón social o Nombre comercial no puede ser nulo o vacio.')
    if dataTercero['nombreContacto'] == None or dataTercero['nombreContacto'] == '':
        raise serializers.ValidationError('El nombre del contacto no puede ser nulo o vacio.')
    if dataTercero['direccion'] == None or dataTercero['direccion'] == '':
        raise serializers.ValidationError('La dirección no puede ser nula o vacia.')
    if dataTercero['departamento'] == None or dataTercero['departamento'] == '':
        raise serializers.ValidationError('El departamento no puede ser nulo o vacio.')
    if dataTercero['municipio'] == None or dataTercero['municipio'] == '':
        raise serializers.ValidationError('El municipio no puede ser nulo o vacio.')
    if dataTercero['telefonoContacto'] == None or dataTercero['telefonoContacto'] == '':
        raise serializers.ValidationError('El Telefono de contacto no puede ser nulo o vacio.')
    if dataTercero['correoContacto'] == None or dataTercero['correoContacto'] == '':
        raise serializers.ValidationError('El correo de contacto no puede ser nulo o vacio.')
    if dataTercero['formaPago'] == None or dataTercero['formaPago'] == '':
        raise serializers.ValidationError('La forma de Pago no puede ser nula o vacia.')
    if dataTercero['tipoPersona'] == None or dataTercero['tipoPersona'] == '':
        raise serializers.ValidationError('El tipo de persona no puede ser nula o vacia.')
    if dataTercero['regimen'] == None or dataTercero['regimen'] == '':
        raise serializers.ValidationError('El regimen no puede ser nulo o vacio.')
    if dataTercero['matriculaMercantil'] == None or dataTercero['matriculaMercantil'] == '':
        raise serializers.ValidationError('El regimen no puede ser nulo o vacio.')
    if dataTercero['codigoPostal'] == None or dataTercero['codigoPostal'] == '':
        raise serializers.ValidationError('El codigoPostal no puede ser nulo o vacio.')
    if dataTercero['cuenta_x_pagar'] == None or dataTercero['cuenta_x_pagar'] == '':
        raise serializers.ValidationError('Si el tercero es proveedor la cuenta por pagar no puede ser nula o vacia.')
    if dataTercero['cuenta_saldo_a_proveedor'] == None or dataTercero['cuenta_saldo_a_proveedor'] == '':
        raise serializers.ValidationError('Si el tercero es proveedor la cuenta saldo a favor no puede ser nula o vacia.')
    
            
