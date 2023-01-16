from django.utils.translation import gettext as _

from ..actions.form import ChoiceQuestion, Form
from ..actions.playback import Playback
from ..actions.trial import Trial


def two_alternative_forced(session, section, choices, expected_response=None, comment='', scoring_rule=None, config=None):
    """
    Provide data for a Two Alternative Forced view that (auto)plays a section,
    shows a question and has two customizable buttons
    """
    playback = Playback(
        [section],
        'BUTTON'
    )
    question = ChoiceQuestion(
        key='choice',
        choices=choices,
        view='BUTTON_ARRAY',
        submits=True,
        config = {'button_text_invisible': True, 'buttons_large_gap': True}
    )
    question.prepare_result(session,
        section=section,
        expected_response=expected_response,
        scoring_rule=scoring_rule,
        comment=comment
    )
    feedback_form = Form([question])
    trial = Trial(playback=playback, feedback_form=feedback_form, config=config)
    return trial.action()
