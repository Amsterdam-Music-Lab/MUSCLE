import random

from django.utils.translation import gettext_lazy as _

from .matching_pairs_lite import MatchingPairsLite
from experiment.actions import Trial
from experiment.actions.playback import VisualMatchingPairs
from result.utils import prepare_result


class VisualMatchingPairsGame(MatchingPairsLite):
    ID = 'VISUAL_MATCHING_PAIRS'
    num_pairs = 8
    contact_email = 'aml.tunetwins@gmail.com'
    show_animation = False
    score_feedback_display = 'small-bottom-right'

    def get_matching_pairs_trial(self, session):
        player_sections = list(session.playlist.section_set.filter(tag__contains='vmp'))
        random.shuffle(player_sections)

        playback = VisualMatchingPairs(
            sections=player_sections,
            show_animation=self.show_animation,
            score_feedback_display=self.score_feedback_display,
        )
        trial = Trial(
            title='Visual Tune twins',
            playback=playback,
            feedback_form=None,
            result_id=prepare_result('visual_matching_pairs', session),
            config={'show_continue_button': False}
        )

        return trial
