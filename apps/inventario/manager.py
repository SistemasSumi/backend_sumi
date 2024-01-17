from django.db import models
# from .models import *

# class OrdenManager(models.Manager):
#     def getOrden(self,id):
#         orden = self.prefetch_related('orden_detalle').get(id = id)
#         return orden
    
#     def getOrdenes(self):
#         orden = self.select_related(
#                     'tercero',
#                     'tercero__departamento',
#                     'tercero__municipio',

#                     'empresa',
#                     'usuario__empresa',
        
#                     'usuario'
#                     ).prefetch_related('orden_detalle').all().order_by('-id')[:1]
#         return orden

    
