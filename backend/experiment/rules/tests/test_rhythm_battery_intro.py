from django.test import TestCase
from section.models import Section, Song, Playlist as PlaylistModel
from participant.models import Participant
from session.models import Session
from experiment.models import Block
from experiment.rules.rhythm_battery_intro import RhythmBatteryIntro
from experiment.actions.explainer import Explainer
from experiment.actions.final import Final
from experiment.actions.form import Form
from experiment.actions.playback import Playback
from experiment.actions.trial import Trial


class RhythmBatteryIntroTest(TestCase):

    def setUp(self):
        playlist = PlaylistModel.objects.create(
            name='test'
        )
        song = Song.objects.create(
            artist="Cheese Shop",
            name="Gouda"
        )
        Section.objects.create(
            playlist=playlist,
            song=song,
            filename="not/to_be_found.mp3",
            tag=0
        )
        self.block = Block.objects.create(slug="TEST", rules="RHYTHM_BATTERY_INTRO")
        participant = Participant.objects.create()
        self.session = Session.objects.create(
            block=Block.objects.first(),
            participant=participant,
            playlist=playlist
        )

    def test_first_round(self):
        listening_conditions = RhythmBatteryIntro()
        actions = listening_conditions.next_round(self.session)
        self.assertIsInstance(actions[0], Explainer)
        self.assertIsInstance(actions[1], Explainer)
        self.assertIsInstance(actions[2], Trial)
        self.assertIsInstance(actions[2].feedback_form, Form)
        self.assertEqual(len(actions[2].feedback_form.form), 1)
        self.assertEqual(actions[2].feedback_form.form[0].key, 'quiet_room')

    def test_next_round_last_time(self):
        listening_conditions = RhythmBatteryIntro()
        listening_conditions.next_round(self.session)
        listening_conditions.next_round(self.session)
        listening_conditions.next_round(self.session)
        listening_conditions.next_round(self.session)
        actions = listening_conditions.next_round(self.session)

        self.assertIsInstance(actions[0], Trial)
        self.assertIsInstance(actions[0].playback, Playback)
        # Assuming no feedback form for the final round
        self.assertIsNone(actions[0].feedback_form)
        self.assertIsInstance(actions[1], Final)

    def test_next_round_does_not_throw_error(self):
        listening_conditions = RhythmBatteryIntro()
        listening_conditions.next_round(self.session)
