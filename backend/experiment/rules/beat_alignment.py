import random
import logging
import copy

from django.utils.translation import gettext_lazy as _

from .base import Base
from .views import Trial, Explainer, Consent, StartSession, Step, Question
from .views.form import ChoiceQuestion, Form
from .views.playback import Playback
from .util.questions import question_by_key
from .util.actions import combine_actions, final_action_with_optional_button, render_feedback_trivia

logger = logging.getLogger(__name__)

class BeatAlignment(Base):
    """Rules for the beat alignment test by Mullensiefen et al. (2014)"""

    ID = 'BEAT_ALIGNMENT'

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds"""

        # 1. General explainer
        explainer = Explainer(
            instruction=_(
                "This test measures your ability to recognize the beat in a piece of music."),
            steps=[
                Step(_(
                        "Listen to the following music fragments. In each fragment you hear a series of beeps.")),
                Step(_(
                        "It's you job to decide if the beeps are ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT of the music.")),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_(
                        "Listen carefully to the following examples. Pay close attention to the description that accompanies each example."))
            ],
            button_label=_('Ok')
            ).action(True)

        # 2. Consent with default text
        consent = Consent.action()

        # 3. Practice rounds
        practice_list = experiment.playlists.first()
        practice_rounds = []
        for i in range(1,4):
            this_round = cls.next_practice_action(practice_list, i)
            practice_rounds.append(copy.deepcopy(this_round))
        practice_rounds.append(Explainer(
            instruction=_('You will now hear 17 music fragments.'),
            steps=[
                Step(_(
                        'With each fragment you have to decide if the beeps are ALIGNED TO THE BEAT, or NOT ALIGNED TO THE BEAT of the music.')),
                Step(_(
                        'Note: a music fragment can occur several times.')),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_('In total, this test will take around 6 minutes to complete. Try to stay focused for the entire duration!'))
            ],
            button_label=_('Start')).action(True)
        )

        # 5. Start session
        start_session = StartSession.action()
        return combine_actions(
            explainer,
            consent,
            *practice_rounds,
            start_session
        )


    @classmethod
    def next_round(cls, session, request_session=None):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds
        # Close the session and return data for the final_score view
        if session.rounds_complete():
            # Finish session
            session.finish()
            session.save()
            percentage = int((sum([r.score for r in session.result_set.all()]) / session.experiment.rounds) * 100)
            feedback = _('Well done! You’ve answered {} percent correctly!').format(percentage)
            trivia = _('In the UK, over 140.000 people did \
                this test when it was first developed?')
            final_text = render_feedback_trivia(feedback, trivia)
            return final_action_with_optional_button(session, final_text, request_session)

        # Next round number, can be used to return different actions
        next_round_number = session.get_next_round()
        return cls.next_trial_action(session, next_round_number)

    @classmethod
    def next_practice_action(cls, playlist, count):
        """Get action data for the next practice round"""
        section = playlist.section_set.filter(name__startswith='ex{}'.format(count)).first()
        if not section:
            return None

        if count==1:
            presentation_text = _(
                "In this example the beeps are ALIGNED TO THE BEAT of the music.")
        else:
            presentation_text = _(
                "In this example the beeps are NOT ALIGNED TO THE BEAT of the music.")

        play_config = {
            'decision_time': section.duration + .1,
        }
        playback = Playback([section], instruction=presentation_text, play_config=play_config)
        view = Trial(
            playback=playback,
            feedback_form=None,
            title=_('Example {}').format(count),
            config={'listen_first': True, 'auto_advance': True}
        )
        return view.action()

    @classmethod
    def next_trial_action(cls, session, this_round):
        """Get next section for given session"""
        filter_by = {'tag_id': 0}
        section = session.section_from_unused_song(filter_by)
        condition = section.filename.split('_')[-1][:-4]
        expected_result = 'ON' if condition=='on' else 'OFF'
        result_pk = Base.prepare_result(session, section, expected_result)
        question = ChoiceQuestion(
            question=_("Are the beeps ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT?"),
            key='aligned',
            choices={
                'ON': _('ALIGNED TO THE BEAT'),
                'OFF': _('NOT ALIGNED TO THE BEAT')
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])
        play_config = {
            'decision_time': section.duration + .1,
        }
        playback = Playback('AUTOPLAY', [section], play_config=play_config)
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Beat alignment'),
            config={
                'listen_first': True
            }
        )
        return view.action()

    @staticmethod
    def calculate_score(result, form_element, data):
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == form_element['value']:
            return 1
        else:
            return 0
