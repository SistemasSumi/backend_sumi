from django.shortcuts import render
# Create your views here.

from django.views.generic import (
    CreateView
)
from django.shortcuts import get_object_or_404
from apps.configuracion.models import VendedoresClientes

from django.contrib.auth import authenticate,login,logout
from apps.users.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser,ParseError
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.generics import (CreateAPIView, ListAPIView,)
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from .models import *

from .serializers import (LoginTradicionalSerializers,UserListSerializers,PermisosUsuarioSerializer)

# from apps.acceso.serializers import (permisosSerializer)

# from apps.acceso.models import (permisos_model)

class tradicionalLoginView(APIView):
    parser_classes   = (JSONParser,)
    serializer_class = LoginTradicionalSerializers
    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username   = serializer.data.get('correo')
        password = serializer.data.get('password')

        print(username+' '+password)
        user = authenticate(
            username  = username,
            password = password
        )
        print(user)
        if not user:
            raise PermissionDenied('Por favor introduzca el email y la clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.')
        login(self.request, user)
        token = ""
        try:
            token = Token.objects.get(user = user)
        except Token.DoesNotExist:
            token = Token.objects.create(user = user)


        permisos = None

        try:
            permisos_usuario = PermisosUsuario.objects.prefetch_related(
                'settings_permisos',
                'informes_permisos',
                'empleados_permisos',
                'cobros_permisos',
                'pagos_permisos',
                'inventario_permisos',
                'facturacion_permisos',
                'contabilidad_permisos',
            ).get(user__id=user.id)
            serializer = PermisosUsuarioSerializer(permisos_usuario)
            permisos = serializer.data
        except PermisosUsuario.DoesNotExist:
            permisos = None
        
        print(permisos)

        
        user = UserListSerializers(user)
    

        
        # permisos = permisos_model.objects.get(usuario = self.request.user.id)

        return Response(
            {
                'token': token.key,
                'user': user.data,
                'permisos': permisos
                # 'permisos': permisosSerializer(permisos).data,
            }
        )

class UserAPIListView(ListAPIView):
	# authentication_classes = [TokenAuthentication]
	# permission_classes     = [IsAuthenticated]
	serializer_class       = UserListSerializers

	def get_queryset(self):
		return User.objects.all()



@csrf_exempt
@api_view(('GET','POST'))
def CrearUsuario(request):
    if request.method == "POST":
        data = request.data

        user = User.objects.create_user(data['username'],data['email'],data['password'])

       
        return Response({'user':user.username})
@csrf_exempt
@api_view(('GET','POST'))
def ActualizarPefil(request):
    if request.method == "POST":
        data = request.data

        user = User.objects.actualizar_datos(
            data['idUser'],
            data['nombres'],
            data['apellidos'],data['email'],
            data['genero'],
            data['avatar']
        )

       
        return Response(UserListSerializers(user).data)

@csrf_exempt
@api_view(('GET','POST'))
def PermisosPorDefecto(request):
    if request.method == 'GET':
        users_without_permisos = User.objects.filter(permisos_usuario__isnull=True)

        # Itera sobre los usuarios y crea registros por defecto en Contabilidad
        for user in users_without_permisos:
            # Crea un nuevo registro de Contabilidad
            permisos = PermisosUsuario.objects.create(user=user)
            ContabilidadPermisos.objects.create(permisos_usuario = permisos)
            FacturacionPermisos.objects.create(permisos_usuario = permisos)
            InformesPermisos.objects.create(permisos_usuario = permisos)
            SettingsPermisos.objects.create(permisos_usuario = permisos)
            InventarioPermisos.objects.create(permisos_usuario = permisos)
            CobrosPermisos.objects.create(permisos_usuario = permisos)
            PagosPermisos.objects.create(permisos_usuario = permisos)
            EmpleadosPermisos.objects.create(permisos_usuario = permisos)
        return Response(
            {
                'result': True,
            }
        )




class LogoutApiView(APIView): 
    def get(self,request,format=None):
        logout(request)
        
        return Response(
            {
                'result': True,
            }
        )
    