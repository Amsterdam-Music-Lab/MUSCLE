from .hooked import Hooked
import random
from django.utils.translation import gettext_lazy as _

from section.models import Section
from session.models import Session


class Eurovision2020(Hooked):
    """Rules for the Eurovision 2020 version of the Hooked experiment.

    Based on the MBCS internship projects of Ada Orken and and Leanne Kuiper.
    """

    ID = 'EUROVISION_2020'
    play_method = 'BUFFER'

    def select_song_sync_section(self, session: Session, condition: str) -> Section:
        if condition == 'returning':
            # select unused songs which have tags greater than 0 (i.e., variants and karaoke) available
            # select sections from these songs with tag values greater than 0
            return session.playlist.get_section({'tag__gt': 0},
                                                song_ids=session.get_unused_song_ids({'tag__gt': 0}))
        else:
            # from all unused songs, select sections with tag values lower than 3 (i.e., exclude karaoke)
            return session.playlist.get_section({'tag__lt': 3},
                                                song_ids=session.get_unused_song_ids())

    def select_heard_before_section(self, session: Session, condition: str) -> Section:
        session_type = self.get_session_type(session)
        if condition == 'new' or session_type == 'same':
            return super().select_heard_before_section(session, condition)
        current_section_id = self.get_returning_section_id(session)
        played_section = Section.objects.get(pk=current_section_id)
        filter = {'song__id': played_section.song.id}
        if session_type == 'karaoke':
            filter.update({'tag': 3})
        elif session_type == 'different':
            previous_tag = played_section.tag
            allowed_tags = list(set(['0', '1', '2', '3']) - set([previous_tag, '3']))
            filter.update({'tag__in': allowed_tags})
        return session.playlist.get_section(filter)

    def get_session_type(self, session: Session) -> str:
        ''' get same / different / karaoke condition
        as we set the random seed to the session.id, the value will be the same throughout the session
        '''
        random.seed(session.id)
        return random.choice(['same', 'different', 'karaoke'])

