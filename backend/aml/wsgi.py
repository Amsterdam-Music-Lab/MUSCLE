"""
WSGI config for aml project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)

application = get_wsgi_application()
