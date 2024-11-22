"""Settings for development environment"""

import os
from aml.base_settings import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("SQL_DATABASE"),
        "USER": os.getenv("SQL_USER"),
        "PASSWORD": os.getenv("SQL_PASSWORD"),
        "HOST": os.getenv("SQL_HOST"),
        "PORT": os.getenv("SQL_PORT"),
    }
}

TESTING = DEBUG

if DEBUG and not TESTING:
    # apps & middleware neeed to be appended for the debug toolbar
    INSTALLED_APPS += ["debug_toolbar"]

    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_ALLOW_ALL_ORIGINS = True

BASE_URL = os.getenv("BASE_URL") or "http://localhost:8000"

GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}
