import random

from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect

from .base import Base
from .util.actions import combine_actions
from .views import Consent, Explainer, CompositeView, Final, Redirect, StartSession

class TestBattery(Base):
    ID = 'TEST_BATTERY'

    @classmethod
    def intro_explainer(cls):
        return Explainer.action(
            instruction=_("You are about to take part in an experiment about rhythm perception."),
            steps=[
                Explainer.step(
                    description=_(
                        "We want to find out what the best way is to test whether someone has a good sense of rhythm!"),
                ),
                Explainer.step(
                    description=_(
                        "You will be doing many little tasks that have something to do with rhythm."),
                ),
                Explainer.step(
                    description=_(
                        "You will get a short explanation and a practice trial for each little task."),
                ),
                Explainer.step(
                    description=_(
                        "You can get reimbursed for completing the entire experiment! Either by earning 5 euros, or by getting study credit (for psychology students at UvA only). You will get instructions for how to get paid or how to get your credit at the end of the experiment."),
                )
            ],
            button_label=_("Continue")
        )
    
    @classmethod
    def listening_explainer(cls):
        return Explainer.action(
            instruction=_(
                'General listening instructions:'),
            steps=[
                Explainer.step(
                    description=_(
                        "To make sure that you can do the experiment as well as possible, please do it a quiet room with a stable internet connection."),
                    number=1
                ),
                Explainer.step(
                    description=_("Please use headphones, and turn off sound notifications from other devices and applications (e.g., e-mail, phone messages)."),
                    number=2
                )],
            button_label=_('Start!')
        )
    
    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""
        consent = Consent.action()
        start_session = StartSession.action()
        return combine_actions(
            cls.intro_explainer(),
            cls.listening_explainer(),
            consent,
            start_session
        )
    
    @staticmethod
    def next_round(session):
        this_round = session.get_next_round()
        if session.final_score == 0:
            prepare_experiments(session)
        elif session.final_score == session.experiment.rounds:
            print("Finalize experiment battery")
        data = session.load_json_data()
        experiment_data = data.get('experiments')
        slug = experiment_data.pop()
        session.merge_json_data({'experiments': experiment_data})
        session.final_score +=1
        session.save()
        return Redirect.action(slug)


def prepare_experiments(session):
    """ Given the session and a list of experiments, generate a random order of experiments 
    merge this into the session data.
    """
    experiment_list = get_experiment_list(session)
    register_consent(session, experiment_list)
    random.shuffle(experiment_list)
    session.merge_json_data({'experiments': experiment_list})
    session.save()

def register_consent(session, experiment_list):
    from ..models import Profile
    participant = session.participant
    for slug in experiment_list:
        question = 'consent_{}'.format(slug)
        answer = True
        try:
            profile = Profile.objects.get(
                participant=participant, question=question)
            profile.answer = answer
        except Profile.DoesNotExist:
            profile = Profile(participant=participant,
                question=question, answer=answer)
        profile.save()

def get_experiment_list(session):
    from ..models import Experiment
    pk_list = session.experiment.nested_experiments
    experiments = [Experiment.objects.get(pk=pk).slug for pk in pk_list]
    return experiments
    
        