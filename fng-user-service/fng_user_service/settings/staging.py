from .base import *

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'd9uasph004c50l',
       'USER': 'diuyxnhmfqbmoc',
       'PASSWORD': '1a9835d89d1ca1c326dc5607edd7a9cef5217462e8ceabbf6ef857db98f9f4aa',
       'HOST': 'ec2-54-211-99-192.compute-1.amazonaws.com',
       'PORT': '5432',
    }
}


# EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'wefreaksngeeks@gmail.com'
EMAIL_HOST_PASSWORD = 'hbnlftpoiwzsdaft'