from django.utils.translation import gettext_lazy as _

from .matching_pairs import MatchingPairsGame
from experiment.actions.form import TextQuestion


class MatchingPairsICMPC(MatchingPairsGame):
    ID = 'MATCHING_PAIRS_ICMPC'

    def __init__(self):
        super().__init__()
        self.question_series[0]['keys'].append('fame_name')
