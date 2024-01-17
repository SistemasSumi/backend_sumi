from django.urls import path
from apps.users import views
from .views import CrearUsuario,ActualizarPefil,PermisosPorDefecto



app_name = 'apps.users'

urlpatterns = [
   path('api/tradicional-login/',views.tradicionalLoginView.as_view(), name="users-tradicional_login" ),
   path('api/logout/',views.LogoutApiView.as_view(), name="users-logout"),
   path('api/users/',views.UserAPIListView.as_view(), name="users-api"),
   path('api/users/create/',CrearUsuario, name="users-api"),
   path('api/users/update/',ActualizarPefil, name="users-api"),
   path('api/users/PermisosPorDefecto/',PermisosPorDefecto, name="users-api"),

]