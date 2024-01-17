from rest_framework import serializers
from apps.users.models import User
from apps.configuracion.models import Notificacion 

from apps.configuracion.serializers import EmpresaListSerializer
from rest_framework import serializers
from .models import PermisosUsuario, ContabilidadPermisos, FacturacionPermisos, InventarioPermisos, PagosPermisos, CobrosPermisos, EmpleadosPermisos, SettingsPermisos, InformesPermisos


class LoginTradicionalSerializers(serializers.Serializer):
    correo   = serializers.CharField(required= True)
    password = serializers.CharField(required= True)





class UserListSerializers(serializers.ModelSerializer):
    empresa = EmpresaListSerializer()
    # genero = serializers.CharField( source= 'get_genero_display')
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'avatar_url',
            'nombres',
            'apellidos',
            'genero',
            'empresa',
            'is_vendedor',
            'grupo'
        ]

class UserListSerializers1(serializers.ModelSerializer):
    empresa = EmpresaListSerializer()
    class Meta:
        model = User
        fields = [
            'username',
            'avatar_url',
            'nombres',
            'apellidos',
            'genero',
            'empresa'
        ]

class UserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'avatar_url',
            'nombres',
            'apellidos',
            'genero',
        ]


class NotificacionSerializer(serializers.ModelSerializer):
    
    usuario = UserListSerializers()
    sender_user = UserListSerializers()
    receiver_users = UserListSerializers(many=True)
    vistas = UserListSerializers(many=True)

    class Meta:
        model = Notificacion
        fields = '__all__' 



class SettingsPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsPermisos
        fields = '__all__'

class InformesPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformesPermisos
        fields = '__all__'

class EmpleadosPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpleadosPermisos
        fields = '__all__'

class CobrosPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CobrosPermisos
        fields = '__all__'

class PagosPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagosPermisos
        fields = '__all__'

class InventarioPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioPermisos
        fields = '__all__'

class FacturacionPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturacionPermisos
        fields = '__all__'

class ContabilidadPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContabilidadPermisos
        fields = '__all__'

class PermisosUsuarioSerializer(serializers.ModelSerializer):
    settings_permisos = SettingsPermisosSerializer(many= True)
    informes_permisos = InformesPermisosSerializer(many= True)
    empleados_permisos = EmpleadosPermisosSerializer(many= True)
    cobros_permisos = CobrosPermisosSerializer(many= True)
    pagos_permisos = PagosPermisosSerializer(many= True)
    inventario_permisos = InventarioPermisosSerializer(many= True)
    facturacion_permisos = FacturacionPermisosSerializer(many= True)
    contabilidad_permisos = ContabilidadPermisosSerializer(many= True)

    class Meta:
        model = PermisosUsuario
        fields = '__all__'
