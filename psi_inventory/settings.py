"""
Django settings for psi_inventory project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#import ldap
from django.contrib import messages
#from django_auth_ldap.config import LDAPGroupQuery, GroupOfNamesType, LDAPSearchUnion, LDAPSearch

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$%@@elg%)=%i4n3bzdxnpkm(9(4oa$m1=y$torz-au(n#a(&jj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#ALLOWED_HOSTS = []

ALLOWED_HOSTS = ["inventory.psiug.org","10.10.10.11","127.0.0.1","41.190.132.148"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'assets',
    # 'home.apps.HomeConfig',
    'home',
    'base',
    'searchapi',
    'django_filters',
    'qrcodegen',
    'disposal',
    'reports',
    'jinjax',
    'rest_framework',
    'api',
    'django.contrib.humanize',
    'approvals',
    'itadmin',
    'corsheaders',
    'storages',
    'django_jinja',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = 'psi_inventory.urls'

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
    
        {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {}
    },
]

WSGI_APPLICATION = 'psi_inventory.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'inventory',
         'USER': 'thejoker',
         'PASSWORD': 'Theingloriusb@stards?',
         'HOST': '10.10.10.2',
         'PORT': '3306',
     }
 }


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'inventory',
#         'USER': 'francis',
#         'PASSWORD': 'DontWakemeup10',
#         'HOST': '10.129.129.21',
#         'PORT': '3306',
#     }
# }


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

DATE_FORMAT = '%m/%d/%Y'
#
DATE_INPUT_FORMATS = '%m/%d/%Y'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/img')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/img/'

CORS_ALLOW_ALL_ORIGINS = True

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/home/fssemanda/gunicorn.errors',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        }
    },
    'loggers': {
        'gunicorn.errors': {
            'level': 'DEBUG',
            'handlers': ['gunicorn'],
            'propagate': True,
        },
    }
}


# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'macho.francis2@gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = 'ShowMeTheWay@30'
# EMAIL_HOST_USER = 'macho.francis2@gmail.com'
# SERVER_EMAIL = 'macho.francis2@gmail.com'

# EMAIL_HOST = 'smtp.office365.com'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'fssemanda@pace.org.ug'
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = 'DontWakemeup10'
# EMAIL_HOST_USER = 'fssemanda@pace.org.ug'
# SERVER_EMAIL = 'fssemanda@pace.org.ug'


# EMAIL_HOST = 'smtp.office365.com'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'fssemanda@psiug.org'
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = 'Gangstarapmademedoit'
# EMAIL_HOST_USER = 'fssemanda@psiug.org'
# SERVER_EMAIL = 'fssemanda@psiug.org'

EMAIL_HOST = 'smtp.office365.com'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'helpdesk@psiug.org'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'Uganda@123'
EMAIL_HOST_USER = 'helpdesk@psiug.org'
SERVER_EMAIL = 'helpdesk@psiug.org'


SESSION_EXPIRE_SECONDS = 3600

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

#SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60

SESSION_TIMEOUT_REDIRECT = '/login/'


AWS_ACCESS_KEY_ID = "AKIAR3ZT64FR6M2MJCPL"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "attachments-psiug"
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = "us-east-2"

AWS_S3_SIGNATURE_VERSION = "s3v4"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


