from decouple import config
from django.conf.global_settings import CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE, SECURE_SSL_REDIRECT

from .base import *

DEBUG = False

ADMINS = [
    ('Jack Sporrow', 'jack@example.com'),
]

ALLOWED_HOSTS = ['.educaproject.com', 'localhost:8000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

REDIS_URL = 'redis://cache:6379'
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True