# This is a dedicated Django settings file intended to be used
# with the graphviz Docker image to generate the ERD.

import os
from aml.base_settings import *

# Database (SQLite3)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Some installed apps neeed to be prepended to the list and some appended
INSTALLED_APPS = ["django_extensions"] + INSTALLED_APPS

CSRF_TRUSTED_ORIGINS = []
