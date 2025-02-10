import random

from django.utils.translation import gettext_lazy as _

from .matching_pairs import MatchingPairsGame
from experiment.actions import Playlist, Info
from experiment.actions.utils import final_action_with_optional_button


class MatchingPairsLite(MatchingPairsGame):
    ID = "MATCHING_PAIRS_LITE"
    num_pairs = 8
    show_animation = False
    score_feedback_display = "small-bottom-right"
    contact_email = "aml.tunetwins@gmail.com"

    def next_round(self, session):
        playlist = Playlist(session.block.playlists.all())
        info = Info("", heading="Press start to enter the game", button_label="Start")
        if session.get_rounds_passed() < 1:
            trial = self.get_matching_pairs_trial(session)
            return [playlist, info, trial]
        else:
            return final_action_with_optional_button(
                session, final_text="End of the game", title="Score", button_text="Back to dashboard"
            )

    def select_sections(self, session):
        pairs = list(session.playlist.section_set.order_by().distinct("group").values_list("group", flat=True))
        selected_pairs = pairs[: self.num_pairs]
        originals = session.playlist.section_set.filter(group__in=selected_pairs, tag="Original")
        degradations = session.playlist.section_set.exclude(tag="Original").filter(group__in=selected_pairs)
        if degradations:
            sections = list(originals) + list(degradations)
            return self.shuffle_sections(sections)
        else:
            sections = list(originals) * 2
            return self.shuffle_sections(sections)

    def shuffle_sections(self, sections):
        random.seed(self.random_seed)
        random.shuffle(sections)
        return sections
