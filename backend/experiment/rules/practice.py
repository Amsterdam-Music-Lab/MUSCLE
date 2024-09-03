from django.utils.translation import gettext_lazy as _

from experiment.actions import ChoiceQuestion, Form, Explainer, Score, Step, Trial
from experiment.actions.playback import Autoplay
from experiment.rules.base import Base
from result.utils import prepare_result
from section.models import Section
from session.models import Session

class Practice(Base):
    ''' Practice is a rules class which presents a trial n_practice_round times
    At the end of a set of practice rounds, it tests whether the partcipant performed well enough to proceed
    '''
    n_practice_rounds = 4
    n_catches = 2

    def next_round(self, session: Session):
        round_number = session.get_rounds_passed()
        if round_number == 0:
            return [self.get_intro_explainer(), self.get_practice_trial(session, round_number)]
        if round_number % self.n_practice_rounds == 0:
            if self.training_successful(session):
                return [self.get_continuation_explainer()]
            else:
                return [self.get_restart_explainer(), self.get_intro_explainer(), self.get_practice_trial(session, round_number)]
        else:
            return [self.get_feedback(session), self.get_practice_trial(session, round_number)]

    def get_intro_explainer(self):
        return Explainer(
            instruction=_('In this test you will hear two tones'),
            steps=[
                Step(_("It's your job to decide if the second tone is LOWER or HIGHER than the second tone")),
                Step(_(
                    'During the experiment it will become more difficult to hear the difference.')),
                Step(_(
                    "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_(
                    'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'))
            ],
            button_label='Ok',
            step_numbers=True
        )

    def get_restart_explainer(self):
        return Explainer(
            instruction=_(
                "You have answered 1 or more practice trials incorrectly."),
            steps=[
                Step(_("We will therefore practice again.")),
                Step(_(
                    'But first, you can read the instructions again.')),
            ],
            button_label=_('Continue')
        )

    def get_continuation_explainer(self):
        return Explainer(
            instruction=_(
                'Now we will start the real experiment.'),
            steps=[
                Step(_('Pay attention! During the experiment it will become more difficult to hear the difference between the tones.')),
                Step(_(
                        "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_(
                        "Remember that you don't move along or tap during the test.")),
            ],
            step_numbers=True,
            button_label=_('Start')
        )

    def get_feedback(self, session: Session) -> Score:
        pass

    def get_condition(self, round_number: int) -> str:
        pass

    def get_practice_trial(self, session: Session, round_number: int) -> Trial:
        """
        Provide the next trial action
        Arguments:
        - session: the session
        - condition: 'lower' or 'higher', corresponding to section tag
        """
        condition = self.get_condition(round_number)
        try:
            section = session.playlist.get_section({'group': 'practice', 'tag': condition})
        except Section.DoesNotExist:
            raise
        expected_response = 'LOWER' if condition == 'lower' else 'HIGHER'
        key = 'higher_or_lower'
        question = ChoiceQuestion(
            question=_('Is the second tone LOWER or HIGHER than the first tone?'),
            key=key,
            choices={
                'LOWER': _('LOWER'),
                'HIGHER': _('HIGHER')
            },
            view='BUTTON_ARRAY',
            result_id=prepare_result(key, session, section=section, expected_response=expected_response),
            submits=True
        )
        playback = Autoplay([section])
        form = Form([question])
        return Trial(
            playback=playback,
            feedback_form=form,
            title=_('%(title)s duration discrimination') % {
                'title': self.condition},
            config={
                'listen_first': True,
                'response_time': section.duration + .1
            }
        )

    def training_successful(self) -> bool:
        pass
