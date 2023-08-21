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

    def test_eurovision(self):
        experiment = Experiment.objects.get(name='Hooked-Eurovision')
        playlist = Playlist.objects.get(name='Eurovision 2021')
        playlist.update_sections()
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=playlist
        )
        Eurovision2020.plan_sections(session)
        assert session.load_json_data().get('plan') != None
        action = Eurovision2020.next_song_sync_action(session)
        assert action != None
        action = Eurovision2020.next_heard_before_action(session)
        assert action != None
    
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
        assert ThatsMySong.feedback_info() == None
        
        for i in range(1, experiment.rounds + 3):
            actions = ThatsMySong.next_round(session)
            if i == experiment.rounds + 2:
                assert len(actions) == 2
                assert actions[1].ID == 'FINAL'
            elif i == 1:
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
            elif i == 2:
                assert session.result_set.count() == 2
                assert session.load_json_data().get('plan') != None
                assert len(actions) == 1
                assert actions[0].key == 'song_sync'
            else:
                plan = session.load_json_data().get('plan')
                heard_before_offset = len(plan['song_sync_sections']) + 2
                assert actions[0].ID == 'SCORE'
                if i < 6:
                    assert len(actions) == 2
                    assert actions[1].key == 'song_sync'
                elif i < heard_before_offset:
                    assert len(actions) == 3
                    assert actions[1].feedback_form.form[0].key in musicgen_keys
                elif i == heard_before_offset:
                    assert len(actions) == 3
                    assert actions[1].ID == 'EXPLAINER'
                else:
                    assert len(actions) == 3
                    assert actions[2].feedback_form.form[0].key == 'heard_before'
                    assert actions[1].feedback_form.form[0].key in musicgen_keys
            session.increment_round()
    
    def test_hooked_china(self):
        experiment = Experiment.objects.get(name='Hooked-China')
        playlist = Playlist.objects.get(name='普通话')
        playlist.update_sections()
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=playlist
        )
        assert Huang2022.feedback_info() != None
        question_trials = Huang2022.get_questionnaire(session)
        assert len(question_trials) == len(Huang2022.questions)
        keys = [q.feedback_form.form[0].key for q in question_trials]
        questions = [q.key for q in Huang2022.questions]
        assert set(keys).difference(set(questions)) == set()


