from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .models import Productos
# from apps.users.serializers import NotificacionSerializer
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

class ProductosConsumer(AsyncWebsocketConsumer):
    

    room_name = None
    room_group_name = None
    resp = dict()

    async def connect(self):
        # Aquí puedes realizar acciones cuando se establece la conexión WebSocket.
        # from apps.users.serializers import NotificacionSerializer
        
        self.room_name = 'general'
        self.room_group_name = 'productos'
        user = self.scope["user"]
        print(user)

      
        sin_stock = await self.obtener_listado_sin_stock()
        ventas = await self.obtener_listado_ventas()
        # print(self.resp['listado'])

        # Realiza acciones con el usuario (por ejemplo, verifica permisos)
       
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # listado_json = json.dumps(listado)
        await self.send(text_data=json.dumps({
            'sin_stock': sin_stock,
            'ventas': ventas,
            'type':'connect'
        }))
        
        
        


    async def disconnect(self, close_code):
        # Aquí puedes realizar acciones cuando se cierra la conexión WebSocket.
        pass

    async def update_producto(self, event):
        try:
            print("entro aqui")
            sin_stock = await self.obtener_listado_sin_stock()
            ventas = await self.obtener_listado_ventas()
            await self.send(text_data=json.dumps({
                'sin_stock': sin_stock,
                'ventas': ventas,
                'type':'update_producto'
            }))
         
          
        except Exception as e:
            # Enviar una respuesta de error al cliente
            await self.send({'error': str(e)})
       

    
 

    
    @database_sync_to_async
    def obtener_listado_sin_stock(self):
       from .functions import getProductos_SinStock
       from .serializers import ProductosSerializer

    #    print(getProductos_SinStock())
       return ProductosSerializer(getProductos_SinStock(),many = True).data
    
    @database_sync_to_async
    def obtener_listado_ventas(self):
       from .functions import getProductosVentas
       from .serializers import ProductosSerializer

    #    print(getProductos_SinStock())
       return ProductosSerializer(getProductosVentas(),many = True).data