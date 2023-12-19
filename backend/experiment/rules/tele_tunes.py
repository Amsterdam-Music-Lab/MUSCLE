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
    consent_file = 'consent_teletunes.html'
