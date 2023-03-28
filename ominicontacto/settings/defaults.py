# -*- coding: utf-8 -*-
# Copyright (C) 2018 Freetech Solutions

# This file is part of OMniLeads

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3, as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

"""
Django settings for ominicontacto project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 's1+*bfrvb@=k@c&9=pm!0sijjewneu5p5rojil#q+!a2y&as-4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'configuracion_telefonia_app.apps.ConfiguracionTelefoniaAppConfig',
    'crispy_forms',
    'compressor',
    'defender',
    'formtools',
    'ominicontacto_app.apps.OminicontactoAppConfig',
    'reciclado_app.apps.RecicladoAppConfig',
    'reportes_app.apps.ReportesAppConfig',
    'supervision_app.apps.SupervisionAppConfig',
    'notification_app.apps.NotificationAppConfig',
    'notification_app.message.apps.Config',
    'simple_history',
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    'api_app.apps.ApiAppConfig',
    'constance',
    'django_js_reverse',
    'import_export',
    'django_extensions',
    'constance.backends.database',
    'django_sass',
    'django_sendfile',
    'easyaudit'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'defender.middleware.FailedLoginMiddleware',
    'ominicontacto_app.middleware.permiso_oml.PermisoOMLMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]


# django-compressor settings
COMPRESS_OFFLINE = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

ROOT_URLCONF = 'ominicontacto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(os.path.dirname(__file__),'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ominicontacto_app.context_processors.global_settings',
                'ominicontacto_app.context_processors.addon_menu_items',
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "ominicontacto_app.template_backends_jinja2.environment",
            "keep_trailing_newline": False,
            "lstrip_blocks": True,
            "trim_blocks": True,
        }
    },
]

ASGI_APPLICATION = 'ominicontacto.asgi.application'
WSGI_APPLICATION = 'ominicontacto.wsgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Password hashers available
# https://docs.djangoproject.com/en/1.9/topics/auth/passwords/

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 600
SESSION_SAVE_EVERY_REQUEST = True
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

TIME_ZONE = 'America/Argentina/Cordoba'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

USE_S3 = os.getenv('CALLREC_DEVICE') == 's3-aws'
if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    ("omnileads-ui-supervision", os.path.join(BASE_DIR, "omnileads_ui/supervision/dist")),
]

AUTH_USER_MODEL = 'ominicontacto_app.User'

TEST_RUNNER = "tests.tests.ManagedModelTestRunner"
OML_TESTING_MODE = False

LOGIN_REDIRECT_URL = 'index'

OL_SIP_LIMITE_INFERIOR = 1000
OL_SIP_LIMITE_SUPERIOR = 3000

OL_NRO_EXT_BPX_LARGO_MIN = 3
"""Largo minimo permitido de nros de extensiones BPX"""

OL_NRO_TELEFONO_LARGO_MIN = 5
"""Largo minimo permitido de nros telefonicos"""

OL_NRO_TELEFONO_LARGO_MAX = 15
"""Largo maximo permitido de nros telefonicos"""

OL_MAX_CANTIDAD_CONTACTOS = 60000
"""Límite de contactos que pueden ser importados a la base de datos."""

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

OML_DUMP_HTTP_AMI_RESPONSES = False

# ==============================================================================
# Settings de DEPLOY (para ser customizados en distintos deploys)
#     Nota: Los settings que siguen, pueden (y algunos DEBEN) ser modificados
#        en los distintos ambientes / deploys
# ==============================================================================

# ==============================================================================
# DEPLOY -> Asterisk
# ==============================================================================

OML_OMNILEADS_HOSTNAME = None
OML_ASTERISK_REMOTEPATH = None
OML_SIP_FILENAME = None
OML_QUEUES_FILENAME = None
OML_RUTAS_SALIENTES_FILENAME = None
"""Path completo (absoluto) al archivo donde se debe generar queues

Ejemplos:

.. code-block:: python

    OML_ASTERISK_REMOTEPATH = "/etc/asterisk/"
    OML_SIP_FILENAME = "/etc/asterisk/sip_fts.conf"
    OML_QUEUES_FILENAME = "/etc/asterisk/queues_fts.conf"
    OML_RUTAS_SALIENTES_FILENAME = "/etc/asterisk/oml_extensions_outr.conf"
"""

ASTERISK = {
    'AMI_USERNAME': None,  # Usuario para AMI
    'AMI_PASSWORD': None,  # Password para usuario para AMI
    # URL usado por Daemon p/acceder a Asterisk AMI via HTTP
    # Ej:
    #    "http://1.2.3.4:7088"
}


DJANGO_DEBUG_TOOLBAR = None

######################
# Defender variables #
######################

DEFENDER_BEHIND_REVERSE_PROXY = None
# Variable obligatoria, se tiene que saber que el defender está detras de un proxy

#######################################
# Ephemeral SIP credentials variables #
#######################################

SIP_SECRET_KEY = None
# Secret key usada para SIP credentials

EPHEMERAL_USER_TTL = None
# Tiempo de duración de credenciales efimeras

OML_KAMAILIO_HOSTNAME = None
# Hostname para conectarse a Kamailio

"""Comando para obtener el secret_key de kamailio y asi poder generar la SIP password

Ejemplo:

    OML_KAMAILIO_CMD = \
        "kamcmd -s /opt/omnileads/kamailio/run/kamailio/kamailio_ctl autheph.dump_secrets"

"""

TMPL_OML_AUDIO_CONVERSOR = None
"""Comando para convertir audios (wav a gsm)

Ejemplos:

.. code-block:: python

    TMPL_OML_AUDIO_CONVERSOR = ["sox", "<INPUT_FILE>", "<OUTPUT_FILE>"]

Para transformar WAV (cualquier formato) -> WAV (compatible con Asterisk):

.. code-block:: python

    TMPL_OML_AUDIO_CONVERSOR = ["sox", "-t", "wav", "<INPUT_FILE>",
        "-r", "8k", "-c", "1", "-e", "signed-integer",
        "-t", "wav", "<OUTPUT_FILE>"
    ]

"""

TMPL_OML_AUDIO_CONVERSOR_EXTENSION = None
"""Extension a usar para archivo generado por `TMPL_OML_AUDIO_CONVERSOR`

Ejemplo: `.wav` (con el . incluido):  el archivo `<OUTPUT_FILE>`
tendra la extension `.wav`
"""

OML_AUDIO_PATH_ASTERISK = None
"""Directory donde se guardan los audios de asterisk en el server de asterisk

Ejemplo:
    OML_WOMBAT_FILENAME = "/var/lib/asterisk/sounds/oml/"
"""

OML_PLAYLIST_PATH_ASTERISK = None
"""Directory donde se guardan las playlist de music on hold en el server de asterisk

Ejemplo:
    OML_PLAYLIST_PATH_ASTERISK = '/var/lib/asterisk/sounds/moh/'
"""

# ==============================================================================
# WOMBAT Config
# ==============================================================================

OML_WOMBAT_URL = None
"""Url de discador de Wombat

Ejemplo:
    OML_WOMBAT_URL = "http://172.16.20.222/wombat"
"""


OML_WOMBAT_FILENAME = None
"""Directory donde se guardan los json de config de wombat

Ejemplo:
    OML_WOMBAT_FILENAME = "/home/freetech/"
"""

OML_WOMBAT_USER = None
OML_WOMBAT_PASSWORD = None
OML_WOMBAT_TIMEOUT = None
"""
User y password por el cual se conectan con la api de WOMBAT DIALER
Ejemplo:
    OML_WOMBAT_USER = "user_test"
    OML_WOMBAT_PASSWORD = "user123"
OML_WOMBAT_TIMEOUT es el tiempo de timeout de la request hacia Wombat API
"""

CALIFICACION_REAGENDA = None

# configuración de Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'api_app.authentication.ExpiringTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'api_app/locale'),
    os.path.join(BASE_DIR, 'configuracion_telefonia_app/locale'),
    os.path.join(BASE_DIR, 'notification_app/locale'),
    os.path.join(BASE_DIR, 'ominicontacto_app/locale'),
    os.path.join(BASE_DIR, 'reportes_app/locale'),
    os.path.join(BASE_DIR, 'reciclado_app/locale'),
    os.path.join(BASE_DIR, 'supervision_app/locale'),
)

LANGUAGES = (
    ('pt-br', 'Portuguese-Br'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fa', 'Persian'),
)

LANGUAGE_CODE = 'es'

TOKEN_EXPIRED_AFTER_SECONDS = None

ALLOW_FEEDBACK = False

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

DJANGO_EASY_AUDIT_REGISTERED_CLASSES = [
    'ominicontacto_app.campana',
    'ominicontacto_app.queue',
    'ominicontacto_app.agenteprofile'
]

DJANGO_EASY_AUDIT_REGISTERED_URLS = [
    r'^/reporte/llamadas/',
    r'^/reportes/agentes_tiempos/',
    r'^/auditar_gestion/buscar/(\d+)/',
    r'^/campana/(\d+)/reporte_grafico/',
    r'^/reporte_de_resultados/(\d+)/',
    r'^/campana/(\d+)/reporte_calificacion/',
    r'^/premium_reports/',
    r'^/grabacion/buscar/(\d+)/',
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
