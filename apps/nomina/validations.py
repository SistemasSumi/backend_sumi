from rest_framework import serializers


def validarEmpleado(datos):
    if datos['nombres'] == None or datos['nombres'] == '':
        raise serializers.ValidationError('el nombre no puede quedar nulo o vacio')
    
    if datos['apellidos'] == None or datos['apellidos'] == '':
        raise serializers.ValidationError('el apellido no puede quedar nulo o vacio')