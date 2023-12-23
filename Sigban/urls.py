"""Sigban URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', lambda request: redirect('admin/')),
    path('admin/', admin.site.urls),
    path('auth/users/', include('apps.users.urls')),
    path('contabilidad/', include('apps.contabilidad.urls')),
    path('settings/', include('apps.configuracion.urls')),
    path('inventario/', include('apps.stock.urls')),
    path('facturacion/', include('apps.docVentas.urls')),
    path('nomina/', include('apps.nomina.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    # path('nomina/', include('apps.nomina.urls')),
    # path('taxis/', include('apps.taxis.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
