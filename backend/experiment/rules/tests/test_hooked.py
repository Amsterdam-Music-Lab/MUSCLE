from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock

from experiment.actions import Explainer, Final, Score, Trial
from experiment.models import Experiment, Phase, Block, ExperimentTranslatedContent, SocialMediaConfig
from question.musicgens import MUSICGENS_17_W_VARIANTS
from participant.models import Participant
from question.questions import get_questions_from_series
from result.models import Result
from section.models import Playlist, Section, Song
from session.models import Session
from question.questions import create_default_questions


class HookedTest(TestCase):
    fixtures = ["playlist", "experiment"]

    @classmethod
    def setUpTestData(cls):
        """set up data for Hooked base class"""
        create_default_questions()
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.create(name="Test Eurovision")
        cls.playlist.csv = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,euro2/Karaoke/2018-11-00-07-046-k.mp3,3,201811007\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,euro2/V1/2018-11-00-07-046-v1.mp3,1,201811007\n"
            "Albania 2018 - Eugent Bushpepa,Mall,49.053,45.0,euro/2018-11-00-49-053-c1.mp3,0,201811049\n"
            "Albania 2018 - Eugent Bushpepa,Mall,81.788,45.0,euro2/V2/2018-11-01-21-788-v2.mp3,2,201811082\n"
            "Albania 2018 - Eugent Bushpepa,Mall,113.647,45.0,euro/2018-11-01-53-647-b.mp3,0,201811114\n"
            "Albania 2018 - Eugent Bushpepa,Mall,132.505,45.0,euro/2018-11-02-12-505-c2.mp3,0,201811133\n"
            "Albania 2019 - Jonida Maliqi,Ktheju Tokës,0.0,45.0,euro/2019-17-00-00-000-i.mp3,0,201917000\n"
            "Albania 2019 - Jonida Maliqi,Ktheju Tokës,4.021,45.0,euro/2019-17-00-04-021-v1.mp3,0,201917004\n"
            "Albania 2019 - Jonida Maliqi,Ktheju Tokës,36.829,45.0,euro/2019-17-00-36-829-pc.mp3,0,201917037\n"
            "Albania 2019 - Jonida Maliqi,Ktheju Tokës,52.703,45.0,euro/2019-17-00-52-703-c1.mp3,0,201917053\n"
            "Albania 2019 - Jonida Maliqi,Ktheju Tokës,85.722,45.0,euro/2019-17-01-25-722-b1.mp3,0,201917086\n"
            "Albania 2019 - Jonida Maliqi,Ktheju Tokës,114.295,45.0,euro/2019-17-01-54-295-b2.mp3,0,201917114\n"
            "Albania 2019 - Jonida Maliqi,Ktheju Tokës,146.891,45.0,euro/2019-17-02-26-891-c2.mp3,0,201917147\n"
            "Belgium 2017 - Blanche,City Lights,26.47,45.0,euro2/Karaoke/2017-04-00-26-470-k.mp3,3,201704026\n"
            "Belgium 2017 - Blanche,City Lights,26.47,45.0,euro2/V1/2017-04-00-26-470-v1.mp3,1,201704026\n"
            "Belgium 2017 - Blanche,City Lights,42.0,45.0,euro/2017-04-00-42-000-c1.mp3,0,201704042\n"
            "Belgium 2017 - Blanche,City Lights,64.19,45.0,euro2/V2/2017-04-01-04-190-v2.mp3,2,201704064\n"
            "Belgium 2017 - Blanche,City Lights,104.312,45.0,euro/2017-04-01-44-312-b.mp3,0,201704104\n"
            "Belgium 2017 - Blanche,City Lights,129.637,45.0,euro/2017-04-02-09-637-c2.mp3,0,201704130\n"
            "Bulgaria 2016 - Poli Genova,If Love Was a Crime,8.41,45.0,euro/2016-04-00-08-410-v1.mp3,0,201604008\n"
            "Bulgaria 2016 - Poli Genova,If Love Was a Crime,25.231,45.0,euro/2016-04-00-25-231-pc.mp3,0,201604025\n"
            "Bulgaria 2016 - Poli Genova,If Love Was a Crime,43.693,45.0,euro/2016-04-00-43-693-c1.mp3,0,201604044\n"
            "Bulgaria 2016 - Poli Genova,If Love Was a Crime,67.078,45.0,euro/2016-04-01-07-078-v2.mp3,0,201604067\n"
            "Bulgaria 2016 - Poli Genova,If Love Was a Crime,119.591,45.0,euro/2016-04-01-59-591-b.mp3,0,201604120\n"
            "Bulgaria 2016 - Poli Genova,If Love Was a Crime,128.206,45.0,euro/2016-04-02-08-206-b.mp3,0,201604128\n"
            "Bulgaria 2016 - Poli Genova,If Love Was a Crime,137.95,45.0,euro/2016-04-02-17-950-c2.mp3,0,201604138\n"
            "Bulgaria 2017 - Kristian Kostov,Beautiful Mess,7.306,45.0,euro2/Karaoke/2017-02-00-07-306-k.mp3,3,201702007\n"
            "Bulgaria 2017 - Kristian Kostov,Beautiful Mess,7.306,45.0,euro2/V1/2017-02-00-07-306-v1.mp3,1,201702007\n"
            "Bulgaria 2017 - Kristian Kostov,Beautiful Mess,36.854,45.0,euro/2017-02-00-36-854-c1.mp3,0,201702037\n"
            "Bulgaria 2017 - Kristian Kostov,Beautiful Mess,83.449,45.0,euro2/V2/2017-02-01-23-449-v2.mp3,2,201702083\n"
            "Bulgaria 2017 - Kristian Kostov,Beautiful Mess,113.322,45.0,euro/2017-02-01-53-322-c2.mp3,0,201702113\n"
            "Bulgaria 2017 - Kristian Kostov,Beautiful Mess,135.523,45.0,euro/2017-02-02-15-523-o.mp3,0,201702136\n"
            "United Kingdom 2017 - Lucie Jones,Never Give Up on You,0.0,45.0,euro2/Karaoke/2017-15-00-00-000-k.mp3,3,201715000\n"
            "United Kingdom 2017 - Lucie Jones,Never Give Up on You,0.0,45.0,euro2/V1/2017-15-00-00-000-v1.mp3,1,201715000\n"
            "United Kingdom 2017 - Lucie Jones,Never Give Up on You,37.979,45.0,euro/2017-15-00-37-979-c1.mp3,0,201715038\n"
            "United Kingdom 2017 - Lucie Jones,Never Give Up on You,70.925,45.0,euro2/V2/2017-15-01-10-925-v2.mp3,2,201715071\n"
            "United Kingdom 2017 - Lucie Jones,Never Give Up on You,94.575,45.0,euro/2017-15-01-34-575-c2.mp3,0,201715095\n"
            "United Kingdom 2017 - Lucie Jones,Never Give Up on You,124.004,45.0,euro/2017-15-02-04-004-b.mp3,0,201715124\n"
        )
        cls.playlist._update_sections()

    def score_results(self, actions):
        for action in actions:
            if isinstance(action, Trial) and action.feedback_form:
                result_id = action.feedback_form.form[0].result_id
                result = Result.objects.get(pk=result_id)
                result.score = 42
                result.save()

    def test_hooked(self):
        n_rounds = 18
        experiment = Experiment.objects.create(slug="HOOKED")
        ExperimentTranslatedContent.objects.create(
            experiment=experiment, language="en", name="Hooked", description="Test Hooked"
        )
        SocialMediaConfig.objects.create(experiment=experiment, url="https://app.amsterdammusiclab.nl/hooked")
        phase = Phase.objects.create(experiment=experiment)
        block = Block.objects.create(slug="Hooked", rules="HOOKED", rounds=n_rounds, phase=phase)
        block.add_default_question_series()
        session = Session.objects.create(block=block, participant=self.participant, playlist=self.playlist)
        rules = session.block_rules()
        for i in range(n_rounds + 1):
            actions = rules.next_round(session)
            self.assertNotEqual(actions, None)
            self.score_results(actions)
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
                self.assertEqual(session.result_set.filter(question_key="recognize").count(), 1)
                self.assertEqual(session.result_set.filter(question_key="correct_place").count(), 1)
            elif i == 1:
                self.assertEqual(len(actions), 4)
                score_action = actions[0]
                self.assertEqual(type(score_action), Score)
                self.assertIsNotNone(score_action.last_song)
                # the session.last_song method returns the song related to the most recent result, without filtering
                self.assertNotEqual(score_action.last_song, session.last_song())
                self.assertEqual(session.result_set.filter(question_key="recognize").count(), 2)
                self.assertEqual(session.result_set.filter(question_key="correct_place").count(), 2)
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
                self.assertGreater(session.result_set.filter(question_key="heard_before").count(), 0)
            elif i == n_rounds:
                # final round
                self.assertEqual(type(actions[0]), Score)
                self.assertEqual(type(actions[1]), Final)

    def test_eurovision_same(self):
        self._run_eurovision("same")

    def test_eurovision_different(self):
        self._run_eurovision("different")

    def test_eurovision_karaoke(self):
        self._run_eurovision("karaoke")

    def _run_eurovision(self, session_type):
        n_rounds = 6
        block = Block.objects.create(slug="Test-Eurovision", rules="EUROVISION_2020", rounds=n_rounds)
        session = Session.objects.create(block=block, participant=self.participant, playlist=self.playlist)
        rules = session.block_rules()
        rules.question_offset = 3
        mock_session_type = Mock(return_value=session_type)
        rules.get_session_type = mock_session_type
        for i in range(block.rounds):
            actions = rules.next_round(session)
            self.score_results(actions)
            heard_before_offset = session.json_data.get("heard_before_offset")
            plan = session.json_data.get("plan")
            self.assertIsNotNone(actions)
            if i == heard_before_offset - 1:
                played_sections = session.json_data.get("played_sections")
                self.assertIsNotNone(played_sections)

            elif i >= heard_before_offset:
                plan = session.json_data.get("plan")
                song_sync_sections = list(
                    session.result_set.filter(question_key="recognize").values_list("section", flat=True)
                )
                heard_before_section = session.result_set.filter(question_key="heard_before").last().section
                song_sync_songs = [Section.objects.get(pk=section).song for section in song_sync_sections]
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

    def test_kuiper_same(self):
        self._run_kuiper("same")

    def test_kuiper_different(self):
        self._run_kuiper("different")

    def _run_kuiper(self, session_type):
        self.assertEqual(Result.objects.count(), 0)
        n_rounds = 6
        block = Block.objects.create(slug="Test-Christmas", rules="KUIPER_2020", rounds=n_rounds)
        playlist = Playlist.objects.create(name="Test-Christmas")
        playlist.csv = (
            "Band Aid,1984 - Do They Know It’s Christmas,1.017,45.0,Kerstmuziek/Do They Know It_s Christmas00.01.017.i.s.mp3,0,100000707\n"
            "Band Aid,1984 - Do They Know It’s Christmas,8.393,45.0,Kerstmuziek/Do They Know It_s Christmas00.08.393.v1.s.mp3,0,100000713\n"
            "Band Aid,1984 - Do They Know It’s Christmas,41.329,45.0,Kerstmuziek/Do They Know It_s Christmas00.41.329.v2.s.mp3,0,100000714\n"
            "Band Aid,1984 - Do They Know It’s Christmas,117.755,45.0,Kerstmuziek/Do They Know It_s Christmas01.57.755.c1.s.mp3,0,100000704\n"
            "Band Aid,1984 - Do They Know It’s Christmas,134.887,45.0,Kerstmuziek/Do They Know It_s Christmas02.14.887.b.s.mp3,0,100000701\n"
            "Bing Crosby,1942 - White Christmas,0.0,45.0,Kerstmuziek/White Christmas00.00.000.i.s.mp3,0,100003907\n"
            "Bing Crosby,1942 - White Christmas,10.178,45.0,Kerstmuziek/White Christmas00.10.178.c1.s.mp3,0,100003904\n"
            "Bing Crosby,1942 - White Christmas,29.904,45.0,Kerstmuziek/White Christmas00.29.904.v.s.mp3,0,100003912\n"
            "Bing Crosby,1942 - White Christmas,93.805,45.0,Kerstmuziek/White Christmas01.33.805.c2.s.mp3,0,100003905\n"
            "Bing Crosby,1942 - White Christmas,133.467,45.0,Kerstmuziek/White Christmas02.13.467.c3.s.mp3,0,100003906\n"
            "Britney Spears,2000 - My Only Wish (This Year),13.445,45.0,Kerstmuziek/My Only Wish This Year00.13.445.v1.s.mp3,0,100002413\n"
            "Britney Spears,2000 - My Only Wish (This Year),38.727,45.0,Kerstmuziek/My Only Wish This Year00.38.727.b.s.mp3,0,100002401\n"
            "Britney Spears,2000 - My Only Wish (This Year),52.464,45.0,Kerstmuziek/My Only Wish This Year00.52.464.c1.s.mp3,0,100002404\n"
            "Britney Spears,2000 - My Only Wish (This Year),91.775,45.0,Kerstmuziek/My Only Wish This Year01.31.775.v2.s.mp3,0,100002414\n"
            "Britney Spears,2000 - My Only Wish (This Year),187.642,45.0,Kerstmuziek/My Only Wish This Year03.07.642.c2.s.mp3,0,100002405\n"
            "Bruce Springsteen,1975 - Santa Claus is Comin’ to Town,46.946,45.0,Kerstmuziek/Santa Claus Is Comin_ to Town00.46.946.c1.n.mp3,2,100002904\n"
            "Bruce Springsteen,1975 - Santa Claus is Comin’ to Town,72.178,45.0,Kerstmuziek/Santa Claus Is Comin_ to Town01.12.178.v1.n.mp3,2,100002913\n"
            "Bruce Springsteen,1975 - Santa Claus is Comin’ to Town,95.574,45.0,Kerstmuziek/Santa Claus Is Comin_ to Town01.35.574.v2.n.mp3,2,100002914\n"
            "Bruce Springsteen,1975 - Santa Claus is Comin’ to Town,114.842,45.0,Kerstmuziek/Santa Claus Is Comin_ to Town01.54.842.c2.n.mp3,2,100002905\n"
            "Bruce Springsteen,1975 - Santa Claus is Comin’ to Town,190.384,45.0,Kerstmuziek/Santa Claus Is Comin_ to Town03.10.384.b.n.mp3,2,100002901\n"
            "Christina Aguilera,2000 - Have Yourself a Merry Little Christmas,14.449,45.0,Kerstmuziek/Have Yourself a Merry Little Christmas00.14.449.c1.o.mp3,1,100001004\n"
            "Christina Aguilera,2000 - Have Yourself a Merry Little Christmas,41.68,45.0,Kerstmuziek/Have Yourself a Merry Little Christmas00.41.680.c2.o.mp3,1,100001005\n"
            "Christina Aguilera,2000 - Have Yourself a Merry Little Christmas,70.856,45.0,Kerstmuziek/Have Yourself a Merry Little Christmas01.10.856.v1.o.mp3,1,100001013\n"
            "Christina Aguilera,2000 - Have Yourself a Merry Little Christmas,175.474,45.0,Kerstmuziek/Have Yourself a Merry Little Christmas02.55.474.v2.o.mp3,1,100001014\n"
            "Christina Aguilera,2000 - Have Yourself a Merry Little Christmas,207.012,45.0,Kerstmuziek/Have Yourself a Merry Little Christmas03.27.012.c3.o.mp3,1,100001006\n"
            "Chuck Berry,1959 - Run Rudolph Run,0.0,45.0,Kerstmuziek/Run Rudolph Run00.00.000.i.s.mp3,0,100002707\n"
            "Chuck Berry,1959 - Run Rudolph Run,19.305,45.0,Kerstmuziek/Run Rudolph Run00.19.305.c1.s.mp3,0,100002704\n"
            "Chuck Berry,1959 - Run Rudolph Run,37.58,45.0,Kerstmuziek/Run Rudolph Run00.37.580.v1.s.mp3,0,100002713\n"
            "Chuck Berry,1959 - Run Rudolph Run,73.941,45.0,Kerstmuziek/Run Rudolph Run01.13.941.b.s.mp3,0,100002701\n"
            "Chuck Berry,1959 - Run Rudolph Run,113.301,45.0,Kerstmuziek/Run Rudolph Run01.53.301.v2.s.mp3,0,100002714\n"
        )
        playlist._update_sections()
        session = Session.objects.create(block=block, participant=self.participant, playlist=playlist)
        rules = session.block_rules()
        rules.question_offset = 3
        mock_session_type = Mock(return_value=session_type)
        rules.get_session_type = mock_session_type
        for i in range(n_rounds):
            actions = rules.next_round(session)
            self.score_results(actions)
            heard_before_offset = session.json_data.get("heard_before_offset")
            if i == heard_before_offset - 1:
                played_sections = session.json_data.get("played_sections")
                song_sync_sections = list(
                    session.result_set.filter(question_key="recognize").values_list("section", flat=True)
                )
                self.assertEqual(len(song_sync_sections), 4)
                self.assertEqual(len(played_sections), 1)
                self.assertIn(played_sections[0], song_sync_sections)
            elif i in range(heard_before_offset, n_rounds):
                plan = session.json_data.get("plan")
                song_sync_sections = list(
                    session.result_set.filter(question_key="recognize").values_list("section", flat=True)
                )
                heard_before_section = session.result_set.filter(question_key="heard_before").last().section
                if plan[i] == "old":
                    if session_type == "same":
                        self.assertIn(heard_before_section.id, song_sync_sections)
                    if session_type == "different":
                        song_sync_songs = [Section.objects.get(pk=section).song for section in song_sync_sections]
                        repeated_song = next(
                            (song for song in song_sync_songs if song == heard_before_section.song), None
                        )
                        self.assertIsNotNone(repeated_song)
                        self.assertNotIn(heard_before_section, song_sync_sections)
                else:
                    self.assertNotIn(heard_before_section, song_sync_sections)

    def test_thats_my_song(self):
        musicgen_keys = [q.key for q in MUSICGENS_17_W_VARIANTS]
        block = Block.objects.get(slug="thats_my_song")
        block.add_default_question_series()
        playlist = Playlist.objects.get(name="ThatsMySong")
        playlist._update_sections()
        session = Session.objects.create(block=block, participant=self.participant, playlist=playlist)
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
                self.assertEqual(len(actions), 4)
                self.assertEqual(actions[1].feedback_form.form[0].key, "dgf_generation")
                self.assertEqual(actions[2].feedback_form.form[0].key, "dgf_gender_identity")
                self.assertEqual(actions[3].feedback_form.form[0].key, "playlist_decades")
                result = Result.objects.get(session=session, question_key="playlist_decades")
                result.given_response = "1960s,1970s,1980s"
                result.save()
                generation = Result.objects.get(participant=self.participant, question_key="dgf_generation")
                generation.given_response = "something"
                generation.save()
                gender = Result.objects.get(participant=self.participant, question_key="dgf_gender_identity")
                gender.given_response = "and another thing"
                gender.save()
            elif i == 1:
                assert session.result_set.count() == 3
                assert session.json_data.get("plan") is not None
                assert len(actions) == 3
                assert actions[0].feedback_form.form[0].key == "recognize"
                assert actions[2].feedback_form.form[0].key == "correct_place"
            else:
                assert actions[0].view == "SCORE"
                if i < rules.question_offset + 1:
                    assert len(actions) == 4
                    assert actions[1].feedback_form.form[0].key == "recognize"
                elif i < heard_before_offset + 1:
                    assert len(actions) == 5
                    assert actions[1].feedback_form.form[0].key in musicgen_keys
                elif i == heard_before_offset + 1:
                    assert len(actions) == 3
                    assert actions[1].view == "EXPLAINER"
                    assert actions[2].feedback_form.form[0].key == "heard_before"
                else:
                    assert len(actions) == 3
                    assert actions[1].feedback_form.form[0].key in musicgen_keys
                    assert actions[2].feedback_form.form[0].key == "heard_before"

    def test_hooked_china(self):
        block = Block.objects.get(slug="huang_2022")
        block.add_default_question_series()
        playlist = Playlist.objects.get(name="普通话")
        playlist._update_sections()
        session = Session.objects.create(block=block, participant=self.participant, playlist=playlist)
        rules = session.block_rules()
        self.assertIsNotNone(rules.feedback_info())

        # check that first round is an audio check
        song = Song.objects.create(name="audiocheck")
        Section.objects.create(playlist=playlist, song=song, filename=SimpleUploadedFile("some_audio.wav", b""))
        actions = rules.next_round(session)
        self.assertIsInstance(actions[0], Trial)
        self.assertEqual(actions[0].feedback_form.form[0].key, "audio_check1")

        # check that question trials are as expected
        question_trials = rules.get_open_questions(session)
        total_questions = get_questions_from_series(block.questionseries_set.all())
        self.assertEqual(len(question_trials), len(total_questions))
        keys = [q.feedback_form.form[0].key for q in question_trials]
        questions = rules.question_series[0]["keys"][0:3]
        for question in questions:
            self.assertIn(question, keys)
