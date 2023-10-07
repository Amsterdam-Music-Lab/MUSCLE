import logging
import copy

from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.actions import Trial, Explainer, Consent, StartSession, Step
from experiment.actions.form import ChoiceQuestion, Form
from experiment.actions.playback import Playback
from experiment.actions.utils import final_action_with_optional_button, render_feedback_trivia
from result.utils import prepare_result

logger = logging.getLogger(__name__)


class BeatAlignment(Base):
    """Rules for the beat alignment test by Mullensiefen et al. (2014)"""

    ID = 'BEAT_ALIGNMENT'

    def first_round(self, experiment):
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
            button_label=_('Ok'),
            step_numbers=True
        )

        # 2. Consent with default text
        consent = Consent()
        
        # 3. Start session
        start_session = StartSession()
        return [
            explainer,
            consent,
            start_session
        ]

    def next_round(self, session, request_session=None):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds
        # Close the session and return data for the final_score view
        if session.rounds_complete():
            # Finish session
            session.finish()
            session.save()
            percentage = int(
                (sum([r.score for r in session.result_set.all()]) / session.experiment.rounds) * 100)
            feedback = _('Well done! You’ve answered {} percent correctly!').format(
                percentage)
            trivia = _('In the UK, over 140.000 people did \
                this test when it was first developed?')
            final_text = render_feedback_trivia(feedback, trivia)
            return final_action_with_optional_button(session, final_text, request_session)
        
        # Next round number, can be used to return different actions
        next_round_number = session.get_next_round()

        # Practice rounds
        if not session.load_json_data().get('done_practice'):
            practice_list = session.playlist
            practice_rounds = []
            for i in range(1, 4):
                this_round = self.next_practice_action(practice_list, i)
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
                step_numbers=True,
                button_label=_('Start'))
            )
            session.save_json_data({'done_practice': True})
            return practice_rounds

        return self.next_trial_action(session, next_round_number)

    def next_practice_action(self, playlist, count):
        """Get action data for the next practice round"""
        section = playlist.section_set.filter(
            song__name__startswith='ex{}'.format(count)).first()
        if not section:
            return None

        if count == 1:
            presentation_text = _(
                "In this example the beeps are ALIGNED TO THE BEAT of the music.")
        else:
            presentation_text = _(
                "In this example the beeps are NOT ALIGNED TO THE BEAT of the music.")
        playback = Playback([section],
                            instruction=presentation_text,
                            preload_message=presentation_text,
                            )
        view = Trial(
            playback=playback,
            feedback_form=None,
            title=_('Example {}').format(count),
            config={
                'response_time': section.duration + .1,
                'listen_first': True, 'auto_advance': True,
                'show_continue_button': False
            }
        )
        return view

    def next_trial_action(self, session, this_round):
        """Get next section for given session"""
        filter_by = {'tag': '0'}
        section = session.section_from_unused_song(filter_by)
        condition = section.song.name.split('_')[-1][:-4]
        expected_response = 'ON' if condition == 'on' else 'OFF'
        key = 'aligned'
        question = ChoiceQuestion(
            question=_(
                "Are the beeps ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT?"),
            key=key,
            choices={
                'ON': _('ALIGNED TO THE BEAT'),
                'OFF': _('NOT ALIGNED TO THE BEAT')
            },
            view='BUTTON_ARRAY',
            result_id=prepare_result(key, session, section=section,
                expected_response=expected_response, scoring_rule='CORRECTNESS'),
            submits=True
        )
        form = Form([question])
        playback = Playback([section])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Beat alignment'),
            config={
                'response_time': section.duration + .1,
                'listen_first': True
            }
        )
        return view
