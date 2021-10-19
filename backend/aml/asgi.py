"""
ASGI config for aml project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

from dotenv import load_dotenv
from pathlib import Path
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aml.production_settings')
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

application = get_asgi_application()
