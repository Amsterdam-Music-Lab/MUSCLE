from django.test import TestCase
from section.models import Section, Song, Playlist as PlaylistModel
from participant.models import Participant
from session.models import Session
from experiment.models import Experiment
from experiment.rules.listening_conditions import ListeningConditions
from experiment.actions import Consent, Explainer, Final, Playback, Playlist, Trial, Form
from experiment.actions.form import Form
from experiment.actions.playback import Playback


class ListeningConditionsTest(TestCase):

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
        self.experiment = Experiment.objects.create(
            name='test',
            slug='TEST',
        )
        participant = Participant.objects.create()
        self.session = Session.objects.create(
            experiment=Experiment.objects.first(),
            participant=participant,
            playlist=playlist
        )

    def test_first_round(self):
        listening_conditions = ListeningConditions()
        actions = listening_conditions.first_round(self.experiment)

        self.assertIsInstance(actions[0], Consent)
        self.assertIsInstance(actions[1], Explainer)
        self.assertIsInstance(actions[2], Playlist)

    def test_next_round_first_round(self):
        listening_conditions = ListeningConditions()
        listening_conditions.first_round(self.experiment)
        actions = listening_conditions.next_round(self.session)

        self.assertIsInstance(actions[0], Trial)

        self.assertIsInstance(actions[0].feedback_form, Form)
        self.assertEqual(len(actions[0].feedback_form.form), 1)
        self.assertEqual(actions[0].feedback_form.form[0].key, 'quiet_room')

    def test_next_round_final_round(self):
        listening_conditions = ListeningConditions()
        listening_conditions.first_round(self.experiment)
        listening_conditions.next_round(self.session)
        listening_conditions.next_round(self.session)
        listening_conditions.next_round(self.session)
        listening_conditions.next_round(self.session)
        actions = listening_conditions.next_round(self.session)

        self.assertIsInstance(actions[0], Trial)
        self.assertIsInstance(actions[0].playback, Playback)
        self.assertIsNone(actions[0].feedback_form)  # Assuming no feedback form for the final round
        self.assertIsInstance(actions[1], Final)

    def test_next_round_does_not_throw_error(self):
        listening_conditions = ListeningConditions()
        listening_conditions.next_round(self.session)

