"""Settings for production environment"""

import os
from aml.base_settings import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Static url is set to /django_static/ in the nginx configuration
# to avoid conflicts with the frontend's static files in /static/
STATIC_URL = '/django_static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('SQL_DATABASE'),
        'USER': os.getenv('SQL_USER'),
        'PASSWORD': os.getenv('SQL_PASSWORD'),
        'HOST': os.getenv('SQL_HOST'),
        'PORT': os.getenv('SQL_PORT'),
    }
}

SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '\n --> %(asctime)s %(levelname)s in '
            '%(pathname)s:%(lineno)d\n%(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/server/logs/aml-experiments.log',
            'maxBytes': 1024*100, # 0.1 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'aml': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'experiment': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

RELOAD_PARTICIPANT_TARGET = '/tunetwins/'

TESTING = os.getenv('AML_TESTING', '') != 'False'

BASE_URL = os.getenv('BASE_URL', '')
