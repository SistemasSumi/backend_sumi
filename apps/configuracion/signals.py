from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
from apps.configuracion.models import Notificacion
from apps.users.serializers import  NotificacionSerializer

# Importa tu modelo Notificacion aquí

@receiver(post_save, sender=Notificacion)
def crear_notificacion(sender, instance, **kwargs):
    
    # Enviar la notificación a través de WebSocket
    message_data = NotificacionSerializer(instance).data

    # El canal se puede personalizar según tus necesidades
    canal = "notificaciones"

    channel_layer = get_channel_layer()

    # print("signal",message_data)


    # Envía el mensaje a través del canal
    try:
        async_to_sync(channel_layer.group_send)(canal, {
            "type": "enviar.notificacion",
            "message": message_data
        })

        print("enviar_notificacion")    
    except Exception as e:
        # Enviar una respuesta de error al cliente
        print({'error': str(e)})
   
