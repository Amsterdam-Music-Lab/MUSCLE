from .hooked import Hooked


class HookedTeleTunes(Hooked):
    """Superclass for Hooked experiment rules"""
    ID = 'HOOKED_TELETUNES'
    recognition_time = 10
    sync_time = 6
    min_jitter = 5
    max_jitter = 10
