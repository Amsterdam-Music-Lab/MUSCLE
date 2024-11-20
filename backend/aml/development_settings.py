"""Settings for development environment"""

import os
import socket
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


def is_debugpy_running(port):
    """Check if debugpy is already running on the specified port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


if DEBUG:
    try:
        import debugpy

        if not is_debugpy_running(5678):
            print("Starting debugpy on port 5678 🐛")
            debugpy.listen(("0.0.0.0", 5678))
        else:
            print("Debugpy is already running on port 5678 👍")

    except Exception as e:
        print(f"Failed to attach debugger: {e}")

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_ALLOW_ALL_ORIGINS = True

BASE_URL = os.getenv("BASE_URL") or "http://localhost:8000"

GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}
