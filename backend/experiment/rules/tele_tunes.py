from experiment.questions.musicgens import MUSICGENS_17_W_VARIANTS
from experiment.questions.demographics import DEMOGRAPHICS
from experiment.questions.utils import copy_shuffle
from .hooked import Hooked


class HookedTeleTunes(Hooked):
    """ Hooked experiment rules for the Teletunes dataset
    Shorter recognition / sync and jitter times due to shorter duration of sections
    """
    ID = 'HOOKED_TELETUNES'
    recognition_time = 10
    sync_time = 6
    min_jitter = 5
    max_jitter = 10
    consent_file = 'consent/consent_teletunes.html'

    def __init__(self):
        self.questions = [
            # 1. Demographic questions (7 questions)
            *copy_shuffle(DEMOGRAPHICS),
            # 2. Musicgens questions with variants
            *copy_shuffle(MUSICGENS_17_W_VARIANTS)
        ]

