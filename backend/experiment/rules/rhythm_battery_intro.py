from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from experiment.actions.button import Button
from experiment.actions.explainer import Explainer, Step
from experiment.actions.form import Form
from experiment.actions.playback import Autoplay, PlaybackSection
from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.trial import Trial
from experiment.actions.wrappers import final_action_with_optional_button
from question.models import ChoiceList
from result.utils import prepare_result
from theme.styles import ColorScheme

boolean_and_middle_choices = [
    {
        "value": "YES",
        "label": _('YES'),
        "color": "colorPositive",
    },
    {
        "value": "MODERATELY",
        "label": _('MODERATELY'),
        "color": "colorNeutral1",
    },
    {"value": "NO", "label": _('NO'), "color": "colorNegative"},
]

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
                button=Button(_('Ok')),
            )
            actions.append(self.get_intro_explainer())
            actions.append(explainer)
            key = 'quiet_room'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ButtonArrayQuestion(
                        key=key,
                        text=_("Are you in a quiet room?"),
                        choices=boolean_and_middle_choices,
                        result_id=result_pk,
                        style=[ColorScheme.BOOLEAN],
                    )
                ],
                submit_button=None,
            )
        elif round_number == 1:
            key = 'internet_connection'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ButtonArrayQuestion(
                        key='internet_connection',
                        text=_("Do you have a stable internet connection?"),
                        choices=boolean_and_middle_choices,
                        result_id=result_pk,
                        style=[ColorScheme.BOOLEAN],
                    )
                ],
                submit_button=None,
            )
        elif round_number == 2:
            key = 'headphones'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ButtonArrayQuestion(
                        key=key,
                        text=_("Are you wearing headphones?"),
                        choices=ChoiceList.objects.get(pk="BOOLEAN").to_dict(),
                        result_id=result_pk,
                        style=[ColorScheme.BOOLEAN],
                    )
                ],
                submit_button=None,
            )
        elif round_number == 3:
            key = 'notifications_off'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form(
                [
                    ButtonArrayQuestion(
                        key=key,
                        text=_(
                            "Do you have sound notifications from other devices turned off?"
                        ),
                        choices=[
                            {
                                "value": "YES",
                                "label": _('YES'),
                                "color": "colorPositive",
                            },
                            {"value": "NO", "label": _('NO'), "color": "colorNegative"},
                        ],
                        result_id=result_pk,
                        style=[ColorScheme.BOOLEAN],
                    ),
                ],
                submit_button=None,
            )
        elif round_number == 4:
            section = session.playlist.section_set.first()
            instruction = _("You can now set the sound to a comfortable level. \
                    You can then adjust the volume to as high a level as possible without it being uncomfortable. \
                    When you are satisfied with the sound level, click Continue")
            playback = Autoplay(
                sections=[PlaybackSection(section)], instruction=instruction
            )
            message = _(
                "Please keep the eventual sound level the same over the course of the experiment.")
            actions = [
                Trial(playback, feedback_form),
                final_action_with_optional_button(
                    session, message)
            ]
            session.finish()
            session.save()
            return actions

        view = Trial(playback, feedback_form=feedback_form)
        actions.append(view)
        return actions

    def get_intro_explainer(self):
        return Explainer(
            instruction=_(
                "You are about to take part in an experiment about rhythm perception."
            ),
            steps=[
                Step(
                    _(
                        "We want to find out what the best way is to test whether someone has a good sense of rhythm!"
                    ),
                ),
                Step(
                    _(
                        "You will be doing many little tasks that have something to do with rhythm."
                    ),
                ),
                Step(
                    _(
                        "You will get a short explanation and a practice trial for each little task."
                    ),
                ),
                Step(
                    _(
                        "You can get reimbursed for completing the entire experiment! Either by earning 6 euros, or by getting 1 research credit (for psychology students at UvA only). You will get instructions for how to get paid or how to get your credit at the end of the experiment."
                    ),
                ),
            ],
            button=Button(_("Continue")),
        )
