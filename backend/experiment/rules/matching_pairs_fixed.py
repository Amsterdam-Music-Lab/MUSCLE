from django.utils.translation import gettext_lazy as _

from .matching_pairs_lite import MatchingPairsLite


class MatchingPairsFixed(MatchingPairsLite):
    ID = 'MATCHING_PAIRS_FIXED'
    random_seed = 'fixed'
