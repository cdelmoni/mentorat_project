from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Administrateur admin/config


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'mentorat', # le nom de notre base de donnees creee precedemment
        'USER': 'mentorat', # attention : remplacer par votre nom d'utilisateur
        'PASSWORD': 'mentorat',
        'HOST': '',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,    #toute les requêtes DB sont inclues dans une transaction
    }
}


# Activer ou desactiver le debug toolbar
# INSTALLED_APPS +=[
#     'debug_toolbar',
# ]

# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware'
# ]

# Specific url file for local dev environment
ROOT_URLCONF = 'config.urls-local'
