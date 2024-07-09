from .hooked import Hooked
import random
from django.utils.translation import gettext_lazy as _

from section.models import Song
from session.models import Session


class Eurovision2020(Hooked):
    """Rules for the Eurovision 2020 version of the Hooked experiment.

    Based on the MBCS internship projects of Ada Orken and and Leanne Kuiper.
    """

    ID = 'EUROVISION_2020'
    play_method = 'BUFFER'


    def get_song_sync_sections(self, session: Session, songs: list[int], n_song_sync_rounds: int) -> list[int]:
        n_returning_sections = round(n_song_sync_rounds / 4)
        returning_sections = [session.get_random_section(
            {'song__id': song, 'tag__gt': 0}).id for song in songs[:n_returning_sections]]
        free_sections = [session.get_random_section(
            {'song__id': song, 'tag__lt': 3}).id for song in songs[n_returning_sections:n_song_sync_rounds]]
        return returning_sections + free_sections

    def get_heard_before_old_sections(self, session: Session, song_sync_sections: list[int], n_heard_before_old_rounds: int) -> list[int]:
        condition = get_condition()
        session.save_json_data({'condition': condition})
        if condition == 'same':
            return [song_sync_sections[:n_heard_before_old_rounds]]
        elif condition == 'karaoke':
            return [session.get_random_section({'song__id': section.song.id, 'tag': 3}).id for section in song_sync_sections[:n_heard_before_old_rounds]]
        else:
            return [session.get_random_section({'song__id': section.song.id}, exclude={'tag__in': [section.tag, 3]}).id for section in song_sync_sections[:n_heard_before_old_rounds]]


def get_condition():
    ''' outfactored so this function can be mocked '''
    return random.choice(['same', 'different', 'karaoke'])

