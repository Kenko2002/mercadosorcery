import os
import dj_database_url
from datetime import timedelta
from pathlib import Path
import drf_yasg

# With the new folder structure, BASE_DIR is the project root.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-^=6-_k)oh!n9-fpcd1qd0rf(!8y2!!8cc*so1if(!*ydv@*_dc')

# SECURITY WARNING: don't run with debug turned on in production!
# Default to False if DEBUG is not set. Vercel will not set this, so it will be False in production.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# --- ALLOWED_HOSTS & CSRF Configuration ---
# This is crucial for production (when DEBUG=False).
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    # Allow all cloud workstation hosts
    '.cloudworkstations.dev',
    # Allow all App Hosting preview hosts
    '.apphosting.dev',
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ.get('WEB_HOST')}" if os.environ.get('WEB_HOST') else "",
    'https://*.cloudworkstations.dev',
    'https://*.apphosting.dev',
]

# Add Vercel deployment URLs
VERCEL_URL = os.environ.get('VERCEL_URL')
if VERCEL_URL:
    ALLOWED_HOSTS.append(VERCEL_URL)
    # The production URL also needs to be a trusted origin for CSRF
    CSRF_TRUSTED_ORIGINS.append(f"https://{VERCEL_URL}")

VERCEL_BRANCH_URL = os.environ.get('VERCEL_BRANCH_URL')
if VERCEL_BRANCH_URL:
    ALLOWED_HOSTS.append(VERCEL_BRANCH_URL)
    # The preview branch URL also needs to be a trusted origin for CSRF
    CSRF_TRUSTED_ORIGINS.append(f"https://{VERCEL_BRANCH_URL}")

# Clean up any empty values that might have occurred in CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = [origin for origin in CSRF_TRUSTED_ORIGINS if origin]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'socialentities',
    'mercadosorcery',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'
WSGI_APPLICATION = 'base.wsgi.application'

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

# --- Database ---
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
#
# Use SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If a DATABASE_URL environment variable is set (e.g., on Vercel),
# use it to configure the production database.
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Adicionado para que o Django encontre o diretório de imagens das cartas.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'imagens_comprimidas'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = 'socialentities.SocialEntity'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

LOGIN_URL = '/admin/login/'
LOGOUT_URL = '/admin/logout/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
