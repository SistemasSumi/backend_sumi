from django.urls import re_path

from apps.stock.consumers import ProductosConsumer

websocket_urlpatterns_stock = [
    re_path(r"ws/productos/$", ProductosConsumer.as_asgi()),
]