import logging
from django.utils.translation import gettext_lazy as _

from experiment.models import Section
from .views import Trial, Explainer, Step, Consent, StartSession, Playlist
from .views.form import ChoiceQuestion, Form
from .views.playback import Playback
from .util.actions import render_feedback_trivia
from .base import Base
from .duration_discrimination import DurationDiscrimination

logger = logging.getLogger(__name__)

class Anisochrony(DurationDiscrimination):
    ID = 'ANISOCHRONY'
    start_diff = 180000
    practice_diff = 270000
    max_turnpoints = 8
    catch_condition = 'REGULAR'

    @classmethod
    def get_response_explainer(cls, correct, correct_response, button_label=_('Next fragment')):
        correct_response = _('REGULAR') if correct_response=='REGULAR' else _('IRREGULAR')
        if correct:
            instruction = _(
                    'The tones were {}. Your answer was CORRECT.').format(correct_response)
        else:
            instruction = _(
                    'The tones were {}. Your answer was INCORRECT.').format(correct_response)
        return Explainer(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )

    @classmethod
    def next_trial_action(cls, session, trial_condition, difficulty):
        """
        Provide the next trial action
        Arguments:
        - session: the session
        - trial_condition: 1 for catch trial, 0 for normal trial
        - difficulty: the current difficulty (in ms) of the trial
        """
        if trial_condition == 1:
            # catch trial
            difference = 0
        else:
            difference = difficulty
        try:
            section = session.playlist.section_set.get(name=difference)
        except Section.DoesNotExist:
            return None
        expected_result = 'REGULAR' if difference == 0 else 'IRREGULAR'
        # create Result object and save expected result to database
        result_pk = Base.prepare_result(session, section, expected_result)
        question = ChoiceQuestion(
            key='if_regular',
            question=_(
                    "Were the tones REGULAR or IRREGULAR?"),
            choices={
                'REGULAR': _('REGULAR'),
                'IRREGULAR': _('IRREGULAR')
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        play_config = {
            'decision_time': section.duration + .7
        }
        playback = Playback('AUTOPLAY', [section], play_config=play_config)
        form = Form([question])
        config = {
            'listen_first': True,
        }
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Anisochrony'),
            config=config
        )
        return view.action()

    @classmethod
    def intro_explanation(cls, *args):
        return Explainer(
            instruction=_(
                'In this test you will hear a series of tones for each trial.'),
            steps=[
                Step(_(
                        "It's your job to decide if the tones sound REGULAR or IRREGULAR")),
                Step(_(
                        'During the experiment it will become more difficult to hear the difference.')),
                Step(_(
                        "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_(
                        "Remember: try not to move or tap along with the sounds")),
                Step(_(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'))
            ],
            button_label='Ok'
        )

    @staticmethod
    def calculate_score(result, form_element, data):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == form_element['value']:
            if expected_response == 'IRREGULAR':
                return 1
            else:
                return 2
        else:
            return 0

    @classmethod
    def get_final_text(cls, difference):
        percentage = round(difference / 6000, 2)
        feedback = _(
            "Well done! You heard the difference when we shifted a tone by {} percent.").format(percentage)
        trivia = _("Many sounds in nature have regularity like a metronome. \
            Our brains use this to process rhythm even better!")
        return render_feedback_trivia(feedback, trivia)

    @classmethod
    def get_difficulty(cls, session, multiplier=1.0):
        if session.final_score == 0:
            return cls.practice_diff
        else:
            return super(Anisochrony, cls).get_difficulty(session, multiplier)
