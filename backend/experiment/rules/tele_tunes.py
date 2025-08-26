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
    default_consent_file = 'consent/consent_teletunes.html'

    # def __init__(self):
    #     self.question_series = [
    #         {"name": "DEMOGRAPHICS", "keys": QUESTION_GROUPS["DEMOGRAPHICS"], "randomize": True}, # 1. Demographic questions (7 questions)
    #         {"name": "MUSICGENS_17_W_VARIANTS", "keys": QUESTION_GROUPS["MUSICGENS_17_W_VARIANTS"], "randomize": True}, # 2. Musicgens questions with variants
    #     ]
