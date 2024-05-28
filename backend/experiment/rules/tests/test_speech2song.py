from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session

from experiment.actions import Trial
from experiment.rules.speech2song import next_repeated_representation, next_single_representation, sound, Speech2Song
from experiment.serializers import serialize_actions


class Speech2SongTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        section_csv = ("transforming,Sometimes behave so strangely.wav,0,2.14,s2s/TEST/Sometimes behave so strangely.wav,1,0\n"
                       "transforming,And a joy it would be.wav,0,0.94,s2s/EN/Transforming/And a joy it would be.wav,1,1\n"
                       "non-transforming,The limpid Walbrook.wav,0,1.20,s2s/EN/Non-Transforming/The limpid Walbrook.wav,0,1\n"
                       "transforming,De abacaxi não tem.wav,0,1.19,s2s/BP/Transforming/De abacaxi não tem.wav,1,2\n"
                       "non-transforming,Minha sobrinha.wav,0,0.99,s2s/BP/Non-Transforming/Minha sobrinha.wav,0,2\n"
                       "transforming,三分钟读一页书.wav,0,1.51,s2s/MC/Transforming/三分钟读一页书.wav,1,3\n"
                       "non-transforming,网上有地图.wav,0,1.13,s2s/MC/Non-Transforming/网上有地图.wav,0,3\n"
                       "transforming,Hermit Thrush1.wav,0,1.19,s2s/ENV/Transforming/Hermit Thrush1.wav,1,4\n"
                       "non-transforming,Snow walking.wav,0,1.30,s2s/ENV/Non-Transforming/Snow walking.wav,0,4\n"
                       )
        cls.playlist = Playlist.objects.create(name='TestSpeech2Song')
        cls.playlist.csv = section_csv
        cls.playlist.update_sections()
        cls.participant = Participant.objects.create()
        cls.experiment = Experiment.objects.create(
            rules='SPEECH_TO_SONG', slug='s2s', rounds=42)
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
            playlist=cls.playlist
        )

    def test_sound_method(self):
        section = self.playlist.section_set.first()
        view = sound(section)
        self.assertEqual(type(view), Trial)

    def test_single_presentation(self):
        group = self.playlist.section_set.first().group
        actions = next_single_representation(self.session, True, int(group))
        self.assertEqual(type(actions), list)

    def test_repeated_presentation(self):
        section = self.playlist.section_set.first()
        Result.objects.create(
            question_key='speech2song',
            session=self.session,
            section=section,
            score=2
        )
        actions = next_repeated_representation(self.session, True)
        self.assertEqual(type(actions), list)

    def test_next_round(self):
        speech2song = Speech2Song()
        actions = speech2song.next_round(self.session)
        self.assertEqual(type(actions), list)

    def test_next_round_serialization(self):
        speech2song = Speech2Song()
        actions = speech2song.next_round(self.session)
        serialized = serialize_actions(actions)
        self.assertEqual(type(serialized), list)
        for s in serialized:
            self.assertEqual(type(s), dict)
