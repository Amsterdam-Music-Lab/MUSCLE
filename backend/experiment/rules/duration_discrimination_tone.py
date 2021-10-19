from django.utils.translation import gettext as _

from .duration_discrimination import DurationDiscrimination

class DurationDiscriminationTone(DurationDiscrimination):
    ID = 'DURATION_DISCRIMINATION_TONE'
    condition = _('tone')