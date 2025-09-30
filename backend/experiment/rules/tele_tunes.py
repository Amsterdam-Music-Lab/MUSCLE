from .hooked import Hooked

from question.preset_catalogues import get_preset_catalogue

class HookedTeleTunes(Hooked):
    """ Hooked experiment rules for the Teletunes dataset
    Shorter recognition / sync and jitter times due to shorter duration of sections
    """
    ID = 'HOOKED_TELETUNES'
    recognition_time = 10
    sync_time = 6
    min_jitter = 5
    max_jitter = 10
    default_consent_file = 'consent/consent_teletunes.html'

    def __init__(self):
        self.question_catalogues = [
            {
                "name": "DEMOGRAPHICS",
                "question_keys": get_preset_catalogue('DEMOGRAPHICS'),
                "randomize": True,
            },  # 1. Demographic questions (7 questions)
            {
                "name": "MUSICGENS_17_W_VARIANTS",
                "question_keys": get_preset_catalogue('MUSICGENS_17_W_VARIANTS'),
                "randomize": True,
            },  # 2. Musicgens questions with variants
        ]
