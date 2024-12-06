import json

from django.test import TestCase
from django.utils import timezone

from experiment.models import Block
from participant.models import Participant
from section.models import Playlist, Section, Song
from result.models import Result
from session.models import Session


class SessionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(
            rules='RHYTHM_BATTERY_INTRO', slug='test')
        cls.playlist = Playlist.objects.create(
            name='Test playlist'
        )
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )

    def test_create(self):
        data = {
            'block_id': self.block.pk,
            'playlist_id': self.playlist.pk,
            'participant_id': self.participant.pk
        }
        response = self.client.post('/session/create', data)
        assert response.status_code != 500

    def test_finalize(self):
        response = self.client.get('/participant/')
        response_data = json.loads(response.content)
        csrf_token = response_data.get('csrf_token')
        participant = Participant.objects.get(pk=response_data.get('id'))
        session = Session.objects.create(
            block=self.block,
            participant=participant)
        data = {
            'csrfmiddlewaretoken:': csrf_token
        }
        response = self.client.post('/session/{}/finalize/'.format(session.pk), data)
        assert response.status_code == 200
        assert Session.objects.filter(finished_at__isnull=False).count() == 1

    def test_percentile_rank(self):
        # create one session with relatively low score
        Session.objects.create(
            block=self.block,
            participant=self.participant,
            final_score=24,
            finished_at=timezone.now()
        )
        # create one unfinished session with relatively high score
        Session.objects.create(
            block=self.block,
            participant=self.participant,
            final_score=180
        )
        finished_session = Session.objects.create(
            block=self.block,
            participant=self.participant,
            final_score=42,
            finished_at=timezone.now()
        )
        rank = finished_session.percentile_rank(exclude_unfinished=True)
        assert rank == 75.0
        rank = finished_session.percentile_rank(exclude_unfinished=False)
        assert rank == 62.5

    def test_last_result(self):
        result = self.session.last_result()
        self.assertIsNone(result)
        Result.objects.create(session=self.session, question_key="ins")
        Result.objects.create(session=self.session, question_key="outs")
        result = self.session.last_result()
        self.assertIsNotNone(result)
        self.assertEqual(result.question_key, "outs")
        result = self.session.last_result(question_keys=["ins"])
        self.assertIsNotNone(result)
        self.assertEqual(result.question_key, "ins")

    def test_last_n_results(self):
        results = self.session.last_n_results()
        self.assertEqual(results, [])
        Result.objects.create(session=self.session, question_key="ins")
        Result.objects.create(session=self.session, question_key="outs")
        results = self.session.last_n_results(n_results=2)
        self.assertEqual(len(results), 2)
        results = self.session.last_n_results(question_keys=["ins"], n_results=2)
        self.assertEqual(len(results), 1)

    def test_last_song(self):
        song = Song.objects.create(artist='Beavis', name='Butthead')
        section = Section.objects.create(playlist=self.playlist, song=song)
        Result.objects.create(
            session=self.session,
            section=section,
            question_key='preference',
            score=0
        )
        last_section = self.session.last_section()
        assert last_section
        last_song = self.session.last_song()
        assert last_song == 'Beavis - Butthead'

    def test_last_score(self):
        for i in range(10):
            keys = ['a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'd']
            Result.objects.create(
                session=self.session,
                question_key=keys[i],
                score=i
            )
        score = self.session.last_score(["c", "d"])
        self.assertEqual(score, 9)

    def test_get_rounds_passed(self):
        Result.objects.create(session=self.session, question_key='some random key')
        self.assertEqual(self.session.get_rounds_passed(), 1)
        self.assertEqual(self.session.get_rounds_passed(self.block.get_rules().counted_result_keys), 1)
        new_block = Block.objects.create(rules='HOOKED', slug='hooked_test')
        new_playlist = Playlist.objects.create(name='another_test')
        new_session = Session.objects.create(block=new_block, playlist=new_playlist, participant=self.participant)
        self.assertEqual(new_session.get_rounds_passed(new_block.get_rules().counted_result_keys), 0)
        Result.objects.create(session=new_session, question_key='recognize')
        self.assertEqual(new_session.get_rounds_passed(new_block.get_rules().counted_result_keys), 1)
        Result.objects.create(session=new_session, question_key='another random key')
        self.assertEqual(new_session.get_rounds_passed(new_block.get_rules().counted_result_keys), 1)
        Result.objects.create(session=new_session, question_key='heard_before')
        self.assertEqual(new_session.get_rounds_passed(new_block.get_rules().counted_result_keys), 2)

    def test_json_data(self):
        self.session.save_json_data({'test': 'tested'})
        self.assertEqual(self.session.json_data, {"test": "tested"})
        self.session.save_json_data({'test_len': 'tested_len'})
        self.assertEqual(len(self.session.json_data), 2)

    def test_json_data_direct(self):
        self.session.json_data.update({'test_direct': 'tested_direct'})
        self.session.save()
        self.assertEqual(self.session.json_data['test_direct'], 'tested_direct')
        self.session.save_json_data({'test_direct_len': 'tested_direct_len'})
        self.session.save()
        self.assertEqual(len(self.session.json_data), 2)
        self.session.json_data.pop('test_direct_len')
        self.assertEqual(len(self.session.json_data), 1)
        self.assertEqual(self.session.json_data.get('test_direct_len', 'temp_value'), 'temp_value')
