import unittest
from unittest.mock import MagicMock

from experiment.actions.playlist import PlaylistSelection


class TestPlaylistSeleection(unittest.TestCase):

    def setUp(self):
        self.mock_playlists = [
            MagicMock(id=1, name='Playlist 1'),
            MagicMock(id=2, name='Playlist 2')
        ]

        self.mock_playlists[0].name = 'Playlist 1'
        self.mock_playlists[1].name = 'Playlist 2'

    def test_initialization_with_playlists(self):
        playlist_action = PlaylistSelection(playlists=self.mock_playlists)
        self.assertEqual(len(playlist_action.playlists), 2)
        self.assertEqual(playlist_action.playlists[0]['id'], 1)
        self.assertEqual(playlist_action.playlists[0]['name'], 'Playlist 1')

    def test_initialization_with_empty_list(self):
        playlist_action = PlaylistSelection(playlists=[])
        self.assertEqual(playlist_action.playlists, [])

    def test_playlists_structure(self):
        playlist_action = PlaylistSelection(playlists=self.mock_playlists)
        for playlist in playlist_action.playlists:
            self.assertIn('id', playlist)
            self.assertIn('name', playlist)
            self.assertIsInstance(playlist['id'], int)
            self.assertIsInstance(playlist['name'], str)


if __name__ == '__main__':
    unittest.main()
