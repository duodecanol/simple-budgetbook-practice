"""
Django settings for simplebudgetbook project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import config
from os import path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["*"]  # FIXME: Production 환경에서 변경 필요

# CORS_ORIGIN_ALLOW_ALL, CORS_ORIGIN_WHITELIST  # TODO: open CORS later

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# allauth settings
AUTH_USER_MODEL = 'userprofile.User'

REST_SESSION_LOGIN = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_USER_MODEL_USERNAME_FIELD =None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ]
}

# DJ_REST_AUTH Configuration  see: https://dj-rest-auth.readthedocs.io/en/latest/configuration.html
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'userprofile.serializers.UserSerializer',
    'LOGIN_SERIALIZER': 'userprofile.serializers.UserLoginSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'userprofile.serializers.UserSignUpSerializer',
}

# Application definition
#
AUTHENTICATION_BACKENDS = [
    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    # Needed to login by username in Django admin, regardless of allauth
    'django.contrib.auth.backends.ModelBackend',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Externals
    'django_filters',
    'django_extensions',
    # DjangoRestFramework
    'rest_framework',
    'rest_framework.authtoken',
    # rest-auth | allauth
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    # Custom apps
    'userprofile',
    'budgetbook',
    'api.v1',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simplebudgetbook.urls'

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

WSGI_APPLICATION = 'simplebudgetbook.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '3306',  # port y of 'x:y' of docker-compose->db
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE', default='ko-kr')

TIME_ZONE = config('TIME_ZONE', default='Asia/Seoul')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
