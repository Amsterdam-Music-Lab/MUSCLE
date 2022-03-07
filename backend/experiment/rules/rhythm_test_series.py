import random
from os.path import join

from django.conf import settings
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string

from .base import Base
from .util.actions import combine_actions
from .views import Consent, Explainer, Step, CompositeView, Final, StartSession

class RhythmTestSeries(Base):
    ID = 'TEST_BATTERY'

    @classmethod
    def intro_explainer(cls):
        return Explainer(
            instruction=_("You are about to take part in an experiment about rhythm perception."),
            steps=[
                Step(_(
                        "We want to find out what the best way is to test whether someone has a good sense of rhythm!"),
                ),
                Step(_(
                        "You will be doing many little tasks that have something to do with rhythm."),
                ),
                Step(_(
                        "You will get a short explanation and a practice trial for each little task."),
                ),
                Step(_(
                        "You can get reimbursed for completing the entire experiment! Either by earning 5 euros, or by getting study credit (for psychology students at UvA only). You will get instructions for how to get paid or how to get your credit at the end of the experiment."),
                )
            ],
            button_label=_("Continue")
        ).action()
    
    @classmethod
    def listening_explainer(cls):
        return Explainer(
            instruction=_(
                'General listening instructions:'),
            steps=[
                Step(_(
                        "To make sure that you can do the experiment as well as possible, please do it a quiet room with a stable internet connection."),
                ),
                Step(_("Please use headphones, and turn off sound notifications from other devices and applications (e.g., e-mail, phone messages)."),
                )],
            button_label=_('OK')
        ).action(True)
    
    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""
        print('in first roound')
        consent = Consent.action()
        start_session = StartSession.action()
        return combine_actions(
            cls.intro_explainer(),
            cls.listening_explainer(),
            consent,
            start_session
        )
    
    @classmethod
    def next_round(cls, session):
        data = session.load_json_data()
        experiment_data = data.get('experiments')
        rendered = render_to_string(join('final', 
            'test_series.html'))
        return Final.action(
            session, 
            title='testing',
            score_template=rendered,
            show_profile=True
        )
        # )
        # experiment_number = int(session.final_score)
        # if not experiment_data:
        #     experiment_data = prepare_experiments(session)
        # if experiment_number == len(experiment_data):
        #     return Final.action(
        #         session,
        #         title=_("Thank you very much for participating!"),
        #         score_message=_(""))
        # slug = experiment_data[experiment_number]
        # session.save()
        # button = {
        #     'text': _('Continue'),
        #     'link': '{}/{}'.format(settings.CORS_ORIGIN_WHITELIST[0], slug)
        # }
        # return Final.action(session, title=_('Next experiment (%d to go!)' % (len(experiment_data) - experiment_number)), button=button)


def prepare_experiments(session):
    """ Given the session and a list of experiments, generate a random order of experiments 
    merge this into the session data.
    """
    lists = get_experiment_lists(session)
    random_list = lists['random']
    random.shuffle(random_list)
    experiment_list = lists['first'] + random_list + lists['last']
    register_consent(session, experiment_list)
    session.merge_json_data({'experiments': experiment_list})
    session.save()
    return experiment_list

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

def get_experiment_lists(session):
    series = session.experiment.test_series
    first_list = get_associated_experiments(series.first_experiments)
    random_list = get_associated_experiments(series.random_experiments)
    last_list = get_associated_experiments(series.last_experiments)
    experiments = {
        'first': first_list,
        'random': random_list,
        'last': last_list
    }
    return experiments

def get_associated_experiments(pk_list):
    from ..models import Experiment
    return [Experiment.objects.get(pk=pk).slug for pk in pk_list]
 