from .base import *
from .prod import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'django.educaproject.com', 'vataman.ru']

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

    }

}
