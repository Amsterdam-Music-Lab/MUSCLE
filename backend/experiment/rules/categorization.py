from .views.playback import Playback
from .views.form import Form, Question
from .views import Consent, Score, StartSession, TwoAlternativeForced

from .util.actions import combine_actions

from .base import Base

class Categorization(Base):
    ID = 'CATEGORIZATION'

    @classmethod
    def first_round(cls, experiment):
        consent = Consent.action()
        start_session = StartSession.action()
        cls.plan_experiment()
        return [
            consent,
            start_session
        ]

    @classmethod
    def next_round(cls, session):
        if session.get_next_round()==0:
            # logic for retrieving sections
            # for now: get first 2 sections
            section = session.playlist.section_set.all()[0]
            # retrieve expected response from json_data
            # for now: set it arbitrarily to "up"
            result_pk = cls.prepare_result(session, section, 'up')
            choices = {'A': 'A', 'B': 'B'}
            view = TwoAlternativeForced(section, choices, result_pk)
            return view.action()
        else:
            return cls.get_trial_with_feedback(session)

    @classmethod
    def plan_experiment(cls):
        # check which group participant belongs to
        # set assignment blue / orange etc.
        # save to session.json_data
        pass

    def get_trial_with_feedback(session):
        score = Score(session, icon='ti-face-smile', timer=5).action()
        section = session.playlist.section_set.all()[0]
        # retrieve expected response from json_data
        # for now: set it arbitrarily to "up"
        result_pk = cls.prepare_result(session, section, 'up')
        choices = {'A': 'A', 'B': 'B'}
        trial = TwoAlternativeForced(section, choices, result_pk).action()
        return combine_actions(score, trial)
