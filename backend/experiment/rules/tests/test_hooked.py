from django.test import TestCase
from unittest import mock

from experiment.actions import Explainer, Score
from experiment.models import Block
from question.musicgens import MUSICGENS_17_W_VARIANTS
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session


class HookedTest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        ''' set up data for Hooked base class '''
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.create(name='Test Eurovision')
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
        cls.playlist.update_sections()

    def test_hooked(self):
        n_rounds = 6
        block = Block.objects.create(name='Hooked', rules='HOOKED', rounds=n_rounds)
        block.add_default_question_series()
        session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=self.playlist
        )
        rules = session.block_rules()
        rules.question_offset = 3
        rules.plan_sections(session)
        plan = session.load_json_data().get('plan')
        self.assertNotEqual(plan, None)
        heard_before_offset = len(plan['song_sync_sections'])
        self.assertEqual(heard_before_offset, 4)
        self.assertEqual(len(plan['heard_before_sections']), 2)
        for round_number in range(n_rounds):
            actions = rules.next_round(session)
            self.assertNotEqual(actions, None)
            if round_number == 0:
                self.assertEqual(len(actions), 3)
            elif round_number == 1:
                self.assertEqual(len(actions), 4)
                self.assertEqual(type(actions[0]), Score)
            elif round_number == rules.question_offset:
                self.assertEqual(len(actions), 5)
            elif round_number == heard_before_offset:
                self.assertEqual(len(actions), 3)
                # Explainer of the Heard Before rounds is second object (after Score)
                self.assertEqual(type(actions[1]), Explainer)

    @mock.patch('experiment.rules.eurovision_2020.get_condition')
    def test_eurovision(self, mock_condition):
        block = Block.objects.create(name='Hooked-Eurovision', rules='EUROVISION_2020', rounds=6)
        session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=self.playlist
        )
        rules = session.block_rules()
        mock_condition.return_value = 'karaoke'
        rules.plan_sections(session)
        plan = session.load_json_data().get('plan')
        breakpoint()
        self.assertIsNotNone(plan)
        # for i in range(0, block.rounds):
        #     actions = rules.next_round(session)
        #     self.assertIsNotNone(actions)
        #     if i == 1:
        #         plan = session.load_json_data().get('plan')
        #         self.assertIsNotNone(plan)

    def test_thats_my_song(self):
        musicgen_keys = [q.key for q in MUSICGENS_17_W_VARIANTS]
        block = Block.objects.get(name='ThatsMySong')
        block.add_default_question_series()
        playlist = Playlist.objects.get(name='ThatsMySong')
        playlist.update_sections()
        session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=playlist
        )
        rules = session.block_rules()
        assert rules.feedback_info() is None

        for i in range(0, block.rounds):
            actions = rules.next_round(session)
            if i == block.rounds + 1:
                assert len(actions) == 2
                assert actions[1].ID == 'FINAL'
            elif i == 0:
                assert len(actions) == 3
                assert actions[0].feedback_form.form[0].key == 'dgf_generation'
                assert actions[1].feedback_form.form[0].key == 'dgf_gender_identity'
                assert actions[2].feedback_form.form[0].key == 'playlist_decades'
                result = Result.objects.get(
                    session=session,
                    question_key='playlist_decades'
                )
                result.given_response = '1960s,1970s,1980s'
                result.save()
                generation = Result.objects.get(
                    participant=self.participant,
                    question_key='dgf_generation'
                )
                generation.given_response = 'something'
                generation.save()
                gender = Result.objects.get(
                    participant=self.participant,
                    question_key='dgf_gender_identity'
                )
                gender.given_response = 'and another thing'
                gender.save()
            elif i == 1:
                assert session.result_set.count() == 3
                assert session.load_json_data().get('plan') is not None
                assert len(actions) == 3
                assert actions[0].feedback_form.form[0].key == 'recognize'
                assert actions[2].feedback_form.form[0].key == 'correct_place'
            else:
                plan = session.load_json_data().get('plan')
                heard_before_offset = len(plan['song_sync_sections'])
                assert actions[0].ID == 'SCORE'
                if i < 5:
                    assert len(actions) == 4
                    assert actions[1].feedback_form.form[0].key == 'recognize'
                elif i < heard_before_offset:
                    assert len(actions) == 5
                    assert actions[1].feedback_form.form[0].key in musicgen_keys
                elif i == heard_before_offset:
                    assert len(actions) == 3
                    assert actions[1].ID == 'EXPLAINER'
                    assert actions[2].feedback_form.form[0].key == 'heard_before'
                else:
                    assert len(actions) == 3
                    assert actions[1].feedback_form.form[0].key in musicgen_keys
                    assert actions[2].feedback_form.form[0].key == 'heard_before'

    def test_hooked_china(self):
        block = Block.objects.get(name='Hooked-China')
        block.add_default_question_series()
        playlist = Playlist.objects.get(name='普通话')
        playlist.update_sections()
        session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=playlist
        )
        rules = session.block_rules()
        assert rules.feedback_info() is not None
        question_trials = rules.get_questionnaire(session)
        # assert len(question_trials) == len(rules.questions)
        keys = [q.feedback_form.form[0].key for q in question_trials]
        questions = rules.question_series[0]['keys'][0:3]
        assert set(keys).difference(set(questions)) == set()
