from django.utils.translation import gettext_lazy as _

from .base_action import BaseAction


class Playlist(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for playlist selection view

    Relates to client component: Playlist.tsx
    The client component automatically continues if there is only one playlist available.
    """

    view = "PLAYLIST"

    def __init__(self, playlists):
        self.instruction:  _('Select a Playlist')
        self.playlists = [
            {'id': playlist.id, 'name': playlist.name}
            for playlist in playlists
        ]
