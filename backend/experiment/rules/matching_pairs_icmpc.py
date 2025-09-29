from django.utils.translation import gettext_lazy as _

from experiment.actions.question import TextQuestion
from .matching_pairs import MatchingPairsGame


class MatchingPairsICMPC(MatchingPairsGame):
    ID = "MATCHING_PAIRS_ICMPC"

    def __init__(self):
        self.add_custom_questions([ICMPC_HALL_OF_FAME])
        super().__init__()
        self.question_series[0]["question_keys"].append("fame_name")


ICMPC_HALL_OF_FAME = TextQuestion(
    key='fame_name', text=_("Enter a name to enter the ICMPC hall of fame")
)
