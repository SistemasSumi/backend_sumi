from django.urls import re_path

from apps.configuracion.consumers import NotificacionConsumer
from apps.stock.consumers import ProductosConsumer

websocket_urlpatterns = [
    # re_path(r"ws/notificaciones/$", ProductosConsumer.as_asgi()),
    # re_path(r"ws/productos/$", ProductosConsumer.as_asgi()),
]