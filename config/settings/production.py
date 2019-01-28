from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'www6.gyyv.vd.ch', 'localhost']

HTDOCS_DIR = "/www_repo/htdocs/mentorat/"

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
        'PASSWORD': 'dbmentoratwapiti',
        'HOST': '',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,    #toute les requêtes DB sont inclues dans une transaction
    }
}

ROOT_URLCONF = 'config.urls'

STATIC_ROOT = os.path.join(HTDOCS_DIR, 'static/')

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Security stuff

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

#SECURE_SSL_REDIRECT = False			# Le serveur nginx fait lui même la redirection des requêtes http en https

X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 3600

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

