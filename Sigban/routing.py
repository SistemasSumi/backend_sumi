from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from apps.stock.consumers import ProductosConsumer # Reemplaza con tus importaciones
from apps.configuracion.consumers import NotificacionConsumer  # Reemplaza con tus importaciones
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r"^ws/notificaciones/$", NotificacionConsumer.as_asgi()),
                re_path(r"^ws/productos/$", ProductosConsumer.as_asgi()),
                
            ])
        ),
    ),
})
