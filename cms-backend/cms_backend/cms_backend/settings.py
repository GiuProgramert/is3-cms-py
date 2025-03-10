0# cms_backend/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Directorio base
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta (debería estar en una variable de entorno en producción)
SECRET_KEY = 'tu_clave_secreta_aqui'

# Debug (en producción debería estar en False)
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ['*']


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms_backend',
    'rest_framework',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cms_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
  
WSGI_APPLICATION = 'cms_backend.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cms',  # Nombre de la base de datos en el contenedor
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',  # Nombre del servicio definido en docker-compose
        'PORT': '5432',
    }
}

# Configuración de archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Configuración de REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': None,
    'LOGIN_URL': None,
    'LOGOUT_URL': None,
}

TIME_ZONE = 'America/Asuncion'  
USE_TZ = True  
load_dotenv()

SENDGRID_API_KEY = 'change-this'
DEFAULT_FROM_EMAIL = 'ma.alexa2000@fpuna.edu.py'

