from django.test import TestCase

from experiment.models import Experiment
from experiment.rules import Eurovision2020, Huang2022, ThatsMySong
from experiment.questions.musicgens import MUSICGENS_17_W_VARIANTS
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
    
    def test_hooked(self):
        experiment = Experiment.objects.create(name='Hooked', rules='HOOKED', rounds=3)
        playlist = Playlist.objects.get(name='Eurovision 2021')
        playlist.update_sections()
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=playlist
        )
        rules = session.experiment_rules()
        rules.plan_sections(session)
        plan = session.load_json_data().get('plan')
        assert plan != None
        actions = rules.next_song_sync_action(session)
        assert len(actions) == 3
        actions = rules.next_song_sync_action(session)
        assert len(actions) == 3
        action = rules.next_heard_before_action(session)
        assert action != None

    def test_eurovision(self):
        experiment = Experiment.objects.get(name='Hooked-Eurovision')
        playlist = Playlist.objects.get(name='Eurovision 2021')
        playlist.update_sections()
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=playlist
        )
        rules = session.experiment_rules()
        for i in range(0, experiment.rounds):
            actions = rules.next_round(session)
            assert actions
    
    def test_thats_my_song(self):
        musicgen_keys = [q.key for q in MUSICGENS_17_W_VARIANTS]
        experiment = Experiment.objects.get(name='ThatsMySong')
        playlist = Playlist.objects.get(name='ThatsMySong')
        playlist.update_sections()
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=playlist
        )
        rules = session.experiment_rules()
        assert rules.feedback_info() == None
        
        for i in range(0, experiment.rounds):
            actions = rules.next_round(session)
            if i == experiment.rounds + 1:
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
                assert session.load_json_data().get('plan') != None
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
        experiment = Experiment.objects.get(name='Hooked-China')
        playlist = Playlist.objects.get(name='普通话')
        playlist.update_sections()
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=playlist
        )
        rules = session.experiment_rules()
        assert rules.feedback_info() != None
        question_trials = rules.get_questionnaire(session)
        # assert len(question_trials) == len(rules.questions)
        keys = [q.feedback_form.form[0].key for q in question_trials]
        questions = [q.key for q in rules.questions]
        assert set(keys).difference(set(questions)) == set()


