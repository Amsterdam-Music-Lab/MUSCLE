from django.conf import settings

from .experiment import *
from experiment.api.profile import *

if settings.DEBUG:
    from .dev import *
