from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  True

ALLOWED_HOSTS = ["localhost","*","127.0.0.1","https://backend.sumiprodelacosta.com","https://sarpsoft-5482d.web.app","app.sumiprodelacosta.com","https://app.sumiprodelacosta.com"]




# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# import dj_database_url
# from decouple  import config
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL')
#     )
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', 
#         'NAME': 'u301041877_hospimed',
#         'USER': 'u301041877_hospimed',
#         'PASSWORD': 'Gerencia12345',
#         'HOST': '194.195.84.154',
#         'PORT': '3306',
#         'OPTIONS': {
#          "init_command": "SET foreign_key_checks = 0;",
#         },
#     }
# }

#DATABASES['default'] =  dj_database_url.config()
DATABASES = {
     'default': {
       		'ENGINE': 'django.db.backends.postgresql_psycopg2',
 		'NAME' : 'farmacia',
 		'USER' : 'postgres',
 		'PASSWORD' : '8520+',
 		'HOST' : 'localhost', #si tienes otra dirección host debes remplazar esta
 		'PORT' : '5432', #si lo dejas vacío tomara el puerto por default
     },
}



STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CORS_ALLOW_HEADERS = "access-control-allow-origin"




CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS  =  [  
    "http://localhost:4200", 
    "http://127.0.0.1:4200",
    "http://192.168.1.6:4200",
    "https://backend.sumiprodelacosta.com",
    "https://sarpsoft-5482d.web.app",
]

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-origin'
)   

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
}

