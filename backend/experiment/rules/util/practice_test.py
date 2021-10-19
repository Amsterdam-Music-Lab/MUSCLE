from django.test import TestCase
from .practice import get_practice_views

class PracticeTest(TestCase):
    fixtures = ['db.json']
    self.participant = Participant()

    self.experiment = Experiment()

    def test_successful_practice(self):
        experiments = Experiment.objects.all()
        participant = Participant()
        participant.save()
        exp = experiments.get(rules='H_BAT')
        session = Session(
            experiment=exp,
            participant=participant,
            playlist=exp.playlists.first())
        session.save()
        counter = 0
        while session.final_score==0:
            counter += 1
            try:
                next_round = exp.get_rules().next_round(session)
            except:
                except Exception as e:
                    print(e)
            result = Result(session=session)
            result.score = 1
        assert counter == 4

        
