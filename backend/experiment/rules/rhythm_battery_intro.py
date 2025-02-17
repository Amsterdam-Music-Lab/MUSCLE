from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from experiment.actions import Explainer, Step, Trial
from experiment.actions.form import ChoiceQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.actions.styles import ColorScheme
from experiment.actions.utils import final_action_with_optional_button
from result.utils import prepare_result


class RhythmBatteryIntro(BaseRules):
    ID = 'RHYTHM_BATTERY_INTRO'

    def next_round(self, session):
        round_number = session.get_rounds_passed()
        playback = None
        feedback_form = None
        actions = []
        if round_number == 0:
            explainer = Explainer(
                instruction=_('General listening instructions:'),
                steps=[
                    Step(
                        _(
                            "To make sure that you can do the experiment as well as possible, please do it a quiet room with a stable internet connection."
                        ),
                    ),
                    Step(
                        _(
                            "Please use headphones, and turn off sound notifications from other devices and applications (e.g., e-mail, phone messages)."
                        ),
                    ),
                ],
                step_numbers=True,
                button_label=_('Ok'),
            )
            actions.append(explainer)
            key = 'quiet_room'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ChoiceQuestion(
                        key=key,
                        question=_("Are you in a quiet room?"),
                        choices={
                            'YES': _('YES'),
                            'MODERATELY': _('MODERATELY'),
                            'NO': _('NO'),
                        },
                        result_id=result_pk,
                        view='BUTTON_ARRAY',
                        submits=True,
                        style=[ColorScheme.BOOLEAN],
                    )
                ]
            )
        elif round_number == 1:
            key = 'internet_connection'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ChoiceQuestion(
                        key='internet_connection',
                        question=_("Do you have a stable internet connection?"),
                        choices={
                            'YES': _('YES'),
                            'MODERATELY': _('MODERATELY'),
                            'NO': _('NO'),
                        },
                        view='BUTTON_ARRAY',
                        result_id=result_pk,
                        submits=True,
                        style=[ColorScheme.BOOLEAN],
                    )
                ]
            )
        elif round_number == 2:
            key = 'headphones'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ChoiceQuestion(
                        key=key,
                        question=_("Are you wearing headphones?"),
                        choices={'YES': _('YES'), 'NO': _('NO')},
                        view='BUTTON_ARRAY',
                        result_id=result_pk,
                        submits=True,
                        style=[ColorScheme.BOOLEAN],
                    )
                ]
            )
        elif round_number == 3:
            key = 'notifications_off'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ChoiceQuestion(
                        key=key,
                        question=_(
                            "Do you have sound notifications from other devices turned off?"
                        ),
                        choices={'YES': _('YES'), 'NO': _('NO')},
                        view='BUTTON_ARRAY',
                        result_id=result_pk,
                        submits=True,
                        style=[ColorScheme.BOOLEAN],
                    ),
                ]
            )
        elif round_number == 4:
            section = session.playlist.section_set.first()
            instruction = _("You can now set the sound to a comfortable level. \
                    You can then adjust the volume to as high a level as possible without it being uncomfortable. \
                    When you are satisfied with the sound level, click Continue")
            playback = Autoplay([section], instruction=instruction)
            message = _(
                "Please keep the eventual sound level the same over the course of the experiment.")
            actions = [
                Trial(playback, feedback_form),
                final_action_with_optional_button(
                    session, message)
            ]
            return actions

        view = Trial(playback, feedback_form=feedback_form)
        actions.append(view)
        return actions

    def get_intro_explainer(self):
        return Explainer(
            instruction=_(
                "You are about to take part in an experiment about rhythm perception."),
            steps=[
                Step(_(
                    "We want to find out what the best way is to test whether someone has a good sense of rhythm!"),
                ),
                Step(_(
                    "You will be doing many little tasks that have something to do with rhythm."),
                ),
                Step(_(
                    "You will get a short explanation and a practice trial for each little task."),
                ),
                Step(_(
                    "You can get reimbursed for completing the entire experiment! Either by earning 6 euros, or by getting 1 research credit (for psychology students at UvA only). You will get instructions for how to get paid or how to get your credit at the end of the experiment."),
                )
            ],
            button_label=_("Continue")
        )
