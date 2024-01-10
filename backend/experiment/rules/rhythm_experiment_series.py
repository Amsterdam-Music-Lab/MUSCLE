import random
from os.path import join

from django.conf import settings
from django.utils.translation import gettext as _
from django.template.loader import render_to_string

from .base import Base
from experiment.actions import Consent, Explainer, Final, StartSession, Step


class RhythmExperimentSeries(Base):
    ID = 'TEST_BATTERY'
    consent_form = 'consent/consent_rhythm.html'
    debrief_form = 'final/experiment_series.html'
    show_participant_final = True

    def intro_explainer(self):
        return Explainer(
            instruction=_(
                "You are about to take part in an experiment about rhythm perception."),
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
                    "You can get reimbursed for completing the entire experiment! Either by earning 6 euros, or by getting 1 research credit (for psychology students at UvA only). You will get instructions for how to get paid or how to get your credit at the end of the experiment."),
                )
            ],
            button_label=_("Continue")
        )
    
    def first_round(self, experiment):
        """Create data for the first experiment rounds."""
        # read consent form from file
        rendered = render_to_string(self.consent_form)
        consent = Consent(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))
        start_session = StartSession()
        return [
            consent,
            self.intro_explainer(),
            start_session
        ]
    
    def next_round(self, session):
        data = session.load_json_data()
        experiment_data = data.get('experiments')
        experiment_number = int(session.final_score)
        if not experiment_data:
            experiment_data = prepare_experiments(session)
        if experiment_number == len(experiment_data):
            rendered = render_to_string(self.debrief_form)
            return Final(
                session,
                title=_("Thank you very much for participating!"),
                final_text=rendered,
                show_participant_link=self.show_participant_final,
                show_participant_id_only=self.show_participant_final,
            )
        slug = experiment_data[experiment_number]
        session.save()
        button = {
            'text': _('Continue'),
            'link': '{}/{}'.format(settings.CORS_ORIGIN_WHITELIST[0], slug)
        }
        return Final(session,
                     title=_('Next experiment (%d to go!)') % (
                         len(experiment_data) - experiment_number),
                     button=button)


def prepare_experiments(session):
    """ Given the session and a list of experiments, generate a random order of experiments
    merge this into the session data.
    """
    lists = get_experiment_lists(session)
    random_list = lists['random']
    random.shuffle(random_list)
    experiment_list = lists['first'] + random_list + lists['last']
    register_consent(session, experiment_list)
    session.save_json_data({'experiments': experiment_list})
    session.save()
    return experiment_list


def register_consent(session, experiment_list):
    from result.models import Result
    participant = session.participant
    for slug in experiment_list:
        question = 'consent_{}'.format(slug)
        answer = 'agreed'
        try:
            profile = Result.objects.get(
                participant=participant, question_key=question)
            profile.given_response = answer
        except Result.DoesNotExist:
            profile = Result(participant=participant,
                              question_key=question, given_response=answer)
        profile.save()


def get_experiment_lists(session):
    series = session.experiment.experiment_series
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
