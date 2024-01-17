from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(tiposDeConcepto)
admin.site.register(Concepto)
admin.site.register(FondoCesantias)
admin.site.register(FondoPension)

admin.site.register(Empleado)