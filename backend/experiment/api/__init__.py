from django.conf import settings

if settings.DEBUG:
    from .dev import *
