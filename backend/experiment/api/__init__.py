from django.conf import settings

from .experiment import *

if settings.DEBUG:
    from .dev import *
