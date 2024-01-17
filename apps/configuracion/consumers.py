from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .models import Notificacion
from apps.users.serializers import NotificacionSerializer
from apps.users.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from channels.auth import AuthMiddleware
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async  
import json


class DRFTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Obten el token del WebSocket desde la URL
        query_string = scope.get("query_string").decode("utf-8")
        token_param = query_string.split("=")[1]

        # Verifica el token y obtén el usuario
        user = await self.get_user_from_token(token_param)

        # Asigna el usuario al alcance (scope) del WebSocket
        scope["user"] = user
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token_param):
        try:
            # Busca el token en la base de datos
            
            token = Token.objects.get(key=token_param)

            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()

class NotificacionConsumer(AsyncWebsocketConsumer):
    

    room_name = None
    room_group_name = None
    
    notify = dict()
    notify['notificacion'] = None
    notify['listado'] = None

    async def connect(self):
        # Aquí puedes realizar acciones cuando se establece la conexión WebSocket.
        # from apps.users.serializers import NotificacionSerializer
        
        self.room_name = 'general'
        self.room_group_name = 'notificaciones'
        user = self.scope["user"]
        print(user)
        self.notify['listado'] = await self.obtener_listado(user)

        # Realiza acciones con el usuario (por ejemplo, verifica permisos)
        if user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps(self.notify))
        else:
            await self.close()
        
        


    async def disconnect(self, close_code):
        # Aquí puedes realizar acciones cuando se cierra la conexión WebSocket.
        pass

    async def enviar_notificacion(self, event):
        try:
            # Tu código para procesar el evento
            # Este método se utiliza para enviar notificaciones a los clientes conectados.
            
            user = self.scope["user"]   
            notify = dict()
            notify['notificacion'] = None
            notify['listado'] = None


            self.notify['listado'] = await self.obtener_listado(user)


            self.notify['notificacion'] =  event['message']

            # Enviar la notificación al cliente
            await self.send(text_data=json.dumps(self.notify))
        except Exception as e:
            # Enviar una respuesta de error al cliente
            await self.send(text_data=json.dumps({'error': str(e)}))
       

    
    async def enviar_notificacion_cliente(self, event):
        message = event['message']
        print(message)

    # Q(grupo = user.grupo)
    @database_sync_to_async
    def obtener_listado(self,user):
       return NotificacionSerializer(
            Notificacion.objects.filter(
                Q(receiver_users__in=[user.pk])
                
                
            ).order_by('-id'),
             many=True  # Agrega many=True si estás serializando una lista de objetos)
        ).data