from django.test import TestCase

from experiment.actions.utils import COLLECTION_KEY, get_current_collection_url, randomize_playhead
from experiment.models import Block
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestActions(TestCase):

    def setUp(self) -> None:
        self.playlist = Playlist.objects.create(name='TestPlaylist')
        self.participant = Participant.objects.create()
        self.block = Block.objects.create(name='TestBlock')
        self.session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist)

    def test_collection_url(self):
        self.assertEqual(get_current_collection_url(self.session), None)
        self.session.save_json_data({COLLECTION_KEY: 'superdupercollection'})
        self.assertEqual(get_current_collection_url(self.session), '/collection/superdupercollection')
        self.participant.participant_id_url = 'participant42'
        self.assertEqual(get_current_collection_url(self.session), '/collection/superdupercollection?participant_id=participant42')


    def test_randomize_playhead(self):
        min_jitter = 5
        max_jitter = 10
        unjittered_playhead = randomize_playhead(min_jitter, max_jitter, True)
        assert unjittered_playhead == 0
        jittered_playhead = randomize_playhead(min_jitter, max_jitter, False)
        assert jittered_playhead >= min_jitter
