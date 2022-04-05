import math
from django.utils.translation import gettext as _

from .form import ChoiceQuestion, Form
from .playback import Playback
from .trial import Trial


class TwoAlternativeForced(Trial):
    """
    Provide data for a TwoAlternativeForced view that (auto)plays a section,
    shows a question and has two customizable buttons
    """
    def __init__(self, section, choices, result_pk, **kwargs):
        super().__init__(**kwargs)
        self.playback = Playback(
            [section],
            'BUTTON'
        )
        question = ChoiceQuestion(
            key='choice',
            choices=choices,
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        self.feedback_form = Form([question])
