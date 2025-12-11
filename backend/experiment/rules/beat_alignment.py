import logging
import copy

from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from experiment.actions.explainer import Explainer, Step
from experiment.actions.form import Form
from experiment.actions.playback import Autoplay
from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.trial import Trial
from experiment.actions.utils import (
    final_action_with_optional_button,
    render_feedback_trivia,
)
from result.utils import prepare_result
from section.models import Playlist

logger = logging.getLogger(__name__)


class BeatAlignment(BaseRules):
    """Rules for the beat alignment test by Mullensiefen et al. (2014)"""

    ID = 'BEAT_ALIGNMENT'

    def get_intro_explainer(self):
        """ Explainer at start of experiment """
        return Explainer(
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

    def next_round(self, session):
        """Get action data for the next round"""

        # If the number of results equals the number of block.rounds
        # Close the session and return data for the final_score view
        if session.rounds_complete():
            # Finish session
            session.finish()
            session.save()
            percentage = int(
                (sum([r.score for r in session.result_set.all()]) / session.block.rounds) * 100)
            feedback = _('Well done! You’ve answered {} percent correctly!').format(
                percentage)
            trivia = _('In the UK, over 140.000 people did \
                this test when it was first developed?')
            final_text = render_feedback_trivia(feedback, trivia)
            return final_action_with_optional_button(session, final_text)

        # Practice rounds
        if not session.json_data.get("done_practice"):
            practice_rounds = [self.get_intro_explainer()]
            for i in range(1, 4):
                this_round = self.next_practice_action(session, i)
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

        return self.next_trial_action(session)

    def next_practice_action(self, session, count):
        """Get action data for the next practice round"""
        section = session.playlist.get_section(
            {'song__name__startswith': f'ex{count}'})
        if not section:
            return None

        if count == 1:
            presentation_text = _(
                "In this example the beeps are ALIGNED TO THE BEAT of the music.")
        else:
            presentation_text = _(
                "In this example the beeps are NOT ALIGNED TO THE BEAT of the music.")
        playback = Autoplay([section],
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

    def next_trial_action(self, session):
        """Get next section for given session"""
        filter_by = {'tag': '0'}
        section = session.playlist.get_section(filter_by, song_ids=session.get_unused_song_ids())
        condition = section.song.name.split('_')[-1]
        expected_response = 'ON' if condition == 'on' else 'OFF'
        key = 'aligned'
        question = ButtonArrayQuestion(
            text=_("Are the beeps ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT?"),
            key=key,
            choices={
                'ON': _('ALIGNED TO THE BEAT'),
                'OFF': _('NOT ALIGNED TO THE BEAT'),
            },
            result_id=prepare_result(
                key,
                session,
                section=section,
                expected_response=expected_response,
                scoring_rule='CORRECTNESS',
            ),
        )
        form = Form([question])
        playback = Autoplay([section])
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

    def validate_playlist(self, playlist: Playlist):
        errors = []
        errors += super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        n_examples = sections.filter(song__name__startswith="ex").count()
        if n_examples != 3:
            errors.append(
                "There should be three example files, with associated song objects whose names start with `ex`"
            )
        trial_stimuli = sections.exclude(song__name__startswith="ex")
        if trial_stimuli.count() != 17:
            errors.append("There should be 17 files to be played during the experiment")
        song_names = trial_stimuli.values_list("song__name", flat=True)
        try:
            groups, tags = zip(*[s.split("_") for s in song_names])
            try:
                [int(g) for g in groups]
            except:
                errors.append("The first part of the song name should be an integer")
            if len(list(set(groups))) != 9:
                errors.append("There should be 9 different audio files")
            if sorted(list(set(tags))) != ["on", "phase", "tempo"]:
                errors.append(
                    "The sections should have song names which contain condition on, phase or tempo"
                )
        except:
            errors.append(
                "The sections should have song names with an integer, followed by a condition"
            )
        return errors
