from django.db import models
#
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)
    

    def actualizar_datos(self,id,nombres,apellidos,email,genero,avatar):
        user = self.get(pk = id)
        user.avatar_url = avatar
        user.nombres = nombres
        user.apellidos = apellidos
        user.genero = genero
        user.email = email
        user.save()
        return user
    
    # def cod_validation(self, id_user, cod_registro):
    #     if self.filter(id=id_user, codregistro=cod_registro).exists():
    #         return True
    #     else:
    #         return False