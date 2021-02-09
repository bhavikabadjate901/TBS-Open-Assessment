from .base import *

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'FNG-User-Service1',
       'USER': 'postgres',
       'PASSWORD': 'Bhavika@123',
    }
}


# EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'wefreaksngeeks@gmail.com'
EMAIL_HOST_PASSWORD = 'hbnlftpoiwzsdaft'