from event.settings.base import *
from .base import *
import os


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',   # Change the engine to MySQL
#         'NAME': 'django',           # Set your MySQL database name
#         'USER': 'root',           # Set your MySQL database user
#         'PASSWORD': 'root',   # Set your MySQL database password
#         # Set to the MySQL server host (e.g., localhost)
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'challenge',
#         'USER': 'davide',
#         'PASSWORD': 'jw8s0F4',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Emailing setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.parkyeri.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'challenge@parkyeri.com'
EMAIL_HOST_PASSWORD = 'bbbngg123s@2#e'
DEFAULT_FROM_EMAIL = 'challenge@parkyeri.com'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = str(os.getenv('EM_HOST'))
# EMAIL_PORT = 587
# EMAIL_HOST_USER = str(os.getenv('EM_HOST_USER'))
# EMAIL_HOST_PASSWORD = str(os.getenv('EM_HOST_PASSWORD'))
# twilio config


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    BASE_DIR/'static'
]

MEDIA_ROOT = BASE_DIR/'static/images'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
