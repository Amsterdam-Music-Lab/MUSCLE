import math
from django.utils.translation import gettext as _

from . import ChoiceQuestion, Form, Playback, Trial


class TwoAlternativeForced(Trial):
    """
    Provide data for a TwoAlternativeForced view that (auto)plays a section,
    shows a question and has two customizable buttons
    """
    def __init__(self, sections, show_button_labels=False, **kwargs):
        super().__init__(**kwargs)
        self.playback = Playback(
            sections,
            'MULTIPLAYER'
        )
        question = ChoiceQuestion(
            choices = {'section.group_id': section.name for section in sections},
            view='BUTTON_ARRAY'
        )
        self.feedback_form = Form([question])
        self.config['show_button_labels'] = show_button_labels


