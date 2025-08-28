from typing import Final
from django.utils.translation import gettext_lazy as _

from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.explainer import Explainer, Step
from experiment.actions.final import Final
from experiment.actions.form import Form
from experiment.actions.playback import Autoplay
from experiment.actions.trial import Trial
from experiment.rules.base import BaseRules
from result.utils import prepare_result
from session.models import Session


class NewBlockRuleset(BaseRules):
    ''' A block type that could be used to test musical preferences '''
    ID = 'NEW_BLOCK_RULESET'
    contact_email = 'info@example.com'

    def __init__(self):

        # Add your questions here
        self.question_series = [
            {
                "name": "Demographics",
                "keys": [
                    'dgf_gender_identity',
                    'dgf_generation',
                    'dgf_musical_experience',
                    'dgf_country_of_origin',
                    'dgf_education_matching_pairs'
                ],
                "randomize": False
            },
        ]

    def get_intro_explainer(self):
        return Explainer(
            instruction='Welcome to this new experiment',
            steps=[
                Step(description=_('Please read the instructions carefully')),
                Step(description=_('Next step of explanation')),
                Step(description=_('Another step of explanation')),
            ],
            step_numbers=True
        )

    def next_round(self, session: Session) -> list:
        # ask any questions defined in the admin interface
        if session.get_rounds_passed() == 0:
            actions = [self.get_intro_explainer()]
            questions = self.get_profile_question_trials(session)
            if questions:
                actions.extend(questions)
            return actions

        elif session.rounds_complete():
            # we have as many results as rounds in this block
            # finish session and show Final view
            session.finish()
            session.save()
            return [
                Final(
                    session,
                    final_text=_('Thank you for participating!'),
                    feedback_info=self.feedback_info()  # show feedback bar, this line can be removed
                )
            ]
        else:
            return self.get_next_trial(session)

    def get_next_trial(self, session) -> Trial:
        # define a key, by which responses to this trial can be found in the database
        key = 'test_trial'
        # get a random section
        section = session.playlist.get_section()
        question = ButtonArrayQuestion(
            text=_("Do you like this song?"),
            key=key,
            result_id=prepare_result(key, session, section=section),
        )
        form = Form([question])
        playback = Autoplay([section])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Test block'),
            config={
                'response_time': section.duration,
                'listen_first': True
            }
        )
        return view
