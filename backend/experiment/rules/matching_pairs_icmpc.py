from django.utils.translation import gettext_lazy as _

from .matching_pairs import MatchingPairs
from experiment.actions.form import TextQuestion

class MatchingPairsICMPC(MatchingPairs):
    ID = 'MATCHING_PAIRS_ICMPC'
    questions = [*MatchingPairs.questions, TextQuestion(
        key='fame_name',
        question=_("Enter a name to enter the ICMPC hall of fame"),
        is_skippable=True
    )]
