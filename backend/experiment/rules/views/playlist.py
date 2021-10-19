class Playlist:  # pylint: disable=too-few-public-methods
    """
    Provide data for playlist selection view

    Relates to client component: Playlist.js 
    The client component automatically continues if there is only one playlist available.
    """

    ID = "PLAYLIST"

    @staticmethod
    def action(playlists):
        """Get data for playlist action"""
        return {
            'view': Playlist.ID,
            'playlists': [
                {'id': playlist.id, 'name': playlist.name}
                for playlist in playlists
            ],
        }
