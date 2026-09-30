from django.db.models import Count
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock

from experiment.actions.explainer import Explainer
from experiment.actions.final import Final
from experiment.actions.score import Score
from experiment.actions.trial import Trial
from experiment.models import (
    Block,
    Experiment,
    Phase,
    SocialMediaConfig,
)
from participant.models import Participant
from question.banks import get_question_bank
from question.models import QuestionList
from result.models import Result
from section.models import Playlist, Section, Song
from session.models import Session


def score_results(actions):
    for action in actions:
        if isinstance(action, Trial) and action.feedback_form:
            result_id = action.feedback_form.form[0].result_id
            result = Result.objects.get(pk=result_id)
            result.score = 42
            result.save()


class HookedTest(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "goldsmiths_msi",
        "musicgens",
        "stomp",
        "tipi",
        "vanderbilt",
        "questions_hooked",
        "eurovision_2020",
    ]

    @classmethod
    def setUpTestData(cls):
        """set up data for Hooked base class"""
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name="Eurovision 2021")
        cls.playlist._update_sections()

    def test_hooked(self):
        n_rounds = 18
        experiment = Experiment.objects.create(
            identifier="HOOKED", name="Hooked", description="Test Hooked"
        )
        SocialMediaConfig.objects.create(
            experiment=experiment, url="https://app.amsterdammusiclab.nl/hooked"
        )
        phase = Phase.objects.create(experiment=experiment)
        block = Block.objects.create(
            identifier="Hooked", rules="HOOKED", rounds=n_rounds, phase=phase
        )
        QuestionList.objects.all().update(block=block)
        session = Session.objects.create(
            block=block, participant=self.participant, playlist=self.playlist
        )
        rules = session.block_rules()
        for i in range(n_rounds + 1):
            actions = rules.next_round(session)
            self.assertNotEqual(actions, None)
            score_results(actions)
            heard_before_offset = session.json_data.get("heard_before_offset")
            self.assertEqual(heard_before_offset, 12)
            if i == 0:
                plan = session.json_data.get("plan")
                self.assertIsNotNone(plan)
                self.assertEqual(len(plan), n_rounds)
                self.assertEqual(len([p for p in plan if p == "free"]), 9)
                self.assertEqual(len([p for p in plan if p == "returning"]), 3)
                self.assertEqual(len([p for p in plan if p == "new"]), 3)
                self.assertEqual(len([p for p in plan if p == "old"]), 3)
                self.assertEqual(len(actions), 5)
                self.assertEqual(
                    session.result_set.filter(question_identifier="recognize").count(),
                    1,
                )
                self.assertEqual(
                    session.result_set.filter(
                        question_identifier="correct_place"
                    ).count(),
                    1,
                )
            elif i == 1:
                self.assertEqual(len(actions), 4)
                score_action = actions[0]
                self.assertEqual(type(score_action), Score)
                self.assertIsNotNone(score_action.last_song)
                # the session.last_song method returns the song related to the most recent result, without filtering
                self.assertNotEqual(score_action.last_song, session.last_song())
                self.assertEqual(
                    session.result_set.filter(question_identifier="recognize").count(),
                    2,
                )
                self.assertEqual(
                    session.result_set.filter(
                        question_identifier="correct_place"
                    ).count(),
                    2,
                )
            elif i == rules.question_offset:
                self.assertEqual(len(actions), 5)
                self.assertEqual(self.participant.result_set.count(), 1)
            elif i == heard_before_offset:
                self.assertEqual(len(actions), 3)
                # Explainer of the Heard Before rounds is second object (after Score)
                self.assertEqual(type(actions[1]), Explainer)
            elif i in range(heard_before_offset, n_rounds):
                # we have a score, heard_before trial, and a question trial
                self.assertEqual(len(actions), 3)
                # at least one heard_before result should have been created
                self.assertGreater(
                    session.result_set.filter(
                        question_identifier="heard_before"
                    ).count(),
                    0,
                )
            elif i == n_rounds:
                # final round
                self.assertEqual(type(actions[0]), Score)
                self.assertEqual(type(actions[1]), Final)


class EurovisionTest(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "goldsmiths_msi",
        "musicgens",
        "stomp",
        "tipi",
        "eurovision_2020",
        "questions_hooked",
    ]

    @classmethod
    def setUpTestData(cls):
        """set up data for Eurovision test"""
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name="Eurovision 2021")
        cls.playlist._update_sections()
        cls.block = Block.objects.get(identifier="eurovision_2021")
        cls.block.rounds = 6
        cls.block.save()

    def test_eurovision_same(self):
        self._run_eurovision("same")

    def test_eurovision_different(self):
        self._run_eurovision("different")

    def test_eurovision_karaoke(self):
        self._run_eurovision("karaoke")

    def _run_eurovision(self, session_type):
        session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist
        )
        rules = session.block_rules()
        rules.question_offset = 3
        mock_session_type = Mock(return_value=session_type)
        rules.get_session_type = mock_session_type
        for i in range(self.block.rounds):
            actions = rules.next_round(session)
            score_results(actions)
            heard_before_offset = session.json_data.get("heard_before_offset")
            plan = session.json_data.get("plan")
            self.assertIsNotNone(actions)
            if i == heard_before_offset - 1:
                played_sections = session.json_data.get("played_sections")
                self.assertIsNotNone(played_sections)

            elif i >= heard_before_offset:
                plan = session.json_data.get("plan")
                song_sync_sections = list(
                    session.result_set.filter(
                        question_identifier="recognize"
                    ).values_list("section", flat=True)
                )
                heard_before_section = (
                    session.result_set.filter(question_identifier="heard_before")
                    .last()
                    .section
                )
                song_sync_songs = [
                    Section.objects.get(pk=section).song
                    for section in song_sync_sections
                ]
                if plan[i] == "old":
                    if session_type == "same":
                        self.assertIn(heard_before_section.id, song_sync_sections)
                    elif session_type == "different":
                        self.assertIn(heard_before_section.song, song_sync_songs)
                        self.assertNotIn(heard_before_section, song_sync_sections)
                        self.assertNotEqual(heard_before_section.tag, "3")
                    elif session_type == "karaoke":
                        self.assertIn(heard_before_section.song, song_sync_songs)
                        self.assertNotIn(heard_before_section, song_sync_sections)
                        self.assertEqual(heard_before_section.tag, "3")


class KuiperTest(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "goldsmiths_msi",
        "musicgens",
        "stomp",
        "tipi",
        "eurovision_2020",
        "kuiper_2020",
        "questions_hooked",
    ]

    @classmethod
    def setUpTestData(cls):
        """set up data for Kuiper tests"""
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name="Eurovision 2021")
        cls.playlist._update_sections()
        cls.block = Block.objects.get(
            identifier="christmas_2020",
        )
        cls.block.rounds = 6
        cls.block.save()
        QuestionList.objects.all().update(block=cls.block)
        cls.playlist = Playlist.objects.get(name="Kuiper 2020")
        cls.playlist._update_sections()

    def test_kuiper_same(self):
        self._run_kuiper("same")

    def test_kuiper_different(self):
        self._run_kuiper("different")

    def _run_kuiper(self, session_type):
        self.assertEqual(Result.objects.count(), 0)
        session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist
        )
        rules = session.block_rules()
        rules.question_offset = 3
        mock_session_type = Mock(return_value=session_type)
        rules.get_session_type = mock_session_type
        for i in range(self.block.rounds):
            actions = rules.next_round(session)
            score_results(actions)
            heard_before_offset = session.json_data.get("heard_before_offset")
            if i == heard_before_offset - 1:
                played_sections = session.json_data.get("played_sections")
                song_sync_sections = list(
                    session.result_set.filter(
                        question_identifier="recognize"
                    ).values_list("section", flat=True)
                )
                self.assertEqual(len(song_sync_sections), 4)
                self.assertEqual(len(played_sections), 1)
                self.assertIn(played_sections[0], song_sync_sections)
            elif i in range(heard_before_offset, self.block.rounds):
                plan = session.json_data.get("plan")
                song_sync_sections = list(
                    session.result_set.filter(
                        question_identifier="recognize"
                    ).values_list("section", flat=True)
                )
                heard_before_section = (
                    session.result_set.filter(question_identifier="heard_before")
                    .last()
                    .section
                )
                if plan[i] == "old":
                    if session_type == "same":
                        self.assertIn(heard_before_section.id, song_sync_sections)
                    if session_type == "different":
                        song_sync_songs = [
                            Section.objects.get(pk=section).song
                            for section in song_sync_sections
                        ]
                        repeated_song = next(
                            (
                                song
                                for song in song_sync_songs
                                if song == heard_before_section.song
                            ),
                            None,
                        )
                        self.assertIsNotNone(repeated_song)
                        self.assertNotIn(heard_before_section, song_sync_sections)
                else:
                    self.assertNotIn(heard_before_section, song_sync_sections)


class ThatsMySongTest(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "musicgens",
        "vanderbilt",
        "thats_my_song",
    ]

    @classmethod
    def setUpTestData(cls):
        """set up data for That's My Song test"""
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name="ThatsMySong")
        cls.playlist._update_sections()

    def test_thats_my_song(self):
        tms_identifiers = get_question_bank('VANDERBILT_FIXED')
        block = Block.objects.get(identifier="thats_my_song")
        block.add_default_question_lists()
        playlist = Playlist.objects.get(name="ThatsMySong")
        playlist._update_sections()
        session = Session.objects.create(
            block=block, participant=self.participant, playlist=playlist
        )
        rules = session.block_rules()
        assert rules.feedback_info() is None

        # need to add 1 to the index, as there is double round counted as 0 in the rules files
        for i in range(0, block.rounds + 1):
            actions = rules.next_round(session)
            heard_before_offset = session.json_data.get("heard_before_offset")
            if i == block.rounds + 1:
                assert len(actions) == 2
                assert actions[1].view == "FINAL"
            elif i == 0:
                self.assertEqual(len(actions), 3)
                self.assertEqual(
                    actions[2].feedback_form.form[0].identifier, "playlist_decades"
                )
                result = Result.objects.get(
                    session=session, question_identifier="playlist_decades"
                )
                result.given_response = "1960s,1970s,1980s"
                result.save()
            elif i == 1:
                assert session.result_set.count() == 3
                assert session.json_data.get("plan") is not None
                assert len(actions) == 3
                assert actions[0].feedback_form.form[0].identifier == "recognize"
                assert actions[2].feedback_form.form[0].identifier == "correct_place"
            else:
                assert actions[0].view == "SCORE"
                if i < rules.question_offset + 1:
                    assert len(actions) == 4
                    assert actions[1].feedback_form.form[0].identifier == "recognize"
                elif i < heard_before_offset + 1:
                    assert len(actions) == 5
                    assert (
                        actions[1].feedback_form.form[0].identifier in tms_identifiers
                    )
                elif i == heard_before_offset + 1:
                    assert len(actions) == 3
                    assert actions[1].view == "EXPLAINER"
                    assert actions[2].feedback_form.form[0].identifier == "heard_before"
                else:
                    assert len(actions) == 3
                    assert (
                        actions[1].feedback_form.form[0].identifier in tms_identifiers
                    )
                    assert actions[2].feedback_form.form[0].identifier == "heard_before"


class Huang2022Test(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "goldsmiths_msi",
        "questions_china",
        "huang_2022",
    ]

    @classmethod
    def setUpTestData(cls):
        """set up data for Hooked base class"""
        cls.participant = Participant.objects.create()

    def test_hooked_china(self):
        block = Block.objects.get(identifier="huang_2022")
        playlist = Playlist.objects.get(name="Cantpop")
        playlist._update_sections()
        session = Session.objects.create(block=block, participant=self.participant, playlist=playlist)
        rules = session.block_rules()
        self.assertIsNotNone(rules.feedback_info())

        # check that first round is an audio check
        song = Song.objects.create(name="audiocheck")
        Section.objects.create(playlist=playlist, song=song, filename=SimpleUploadedFile("some_audio.wav", b""))
        actions = rules.next_round(session)
        self.assertIsInstance(actions[0], Trial)
        self.assertEqual(actions[0].feedback_form.form[0].identifier, "audio_check1")

        # check that question trials are as expected
        question_trials = rules.get_profile_question_trials(session, None)
        n_total_questions = block.questionlist_set.aggregate(Count("questions"))[
            'questions__count'
        ]
        self.assertEqual(len(question_trials), n_total_questions)
        identifiers = [q.feedback_form.form[0].identifier for q in question_trials]
        questions = rules.question_lists[0]["question_identifiers"][0:3]
        for question in questions:
            self.assertIn(question, identifiers)
