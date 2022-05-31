from .views.playback import Playback
from .views.form import Form, Question
from .views import Consent, StartSession, TwoAlternativeForced

from .util.actions import combine_actions

from .base import Base
import random


class Categorization(Base):
    ID = 'CATEGORIZATION'

    @classmethod
    def first_round(cls, experiment):
        consent = Consent.action()
        start_session = StartSession.action()

        return combine_actions(
            consent,
            start_session
        )

    @classmethod
    def next_round(cls, session):
        next_round_number = session.get_next_round()

        if next_round_number == 1:
            cls.plan_experiment(session)
            section = session.playlist.section_set.all()[0]
        else:
            section = session.playlist.section_set.all()[next_round_number]
        # logic for retrieving sections
        # for now: get first 2 sections

        # retrieve expected response from json_data
        # for now: set it arbitrarily to "up"
        result_pk = Base.prepare_result(session, section, 'B')
        choices = {'A': 'A', 'B': 'B'}
        view = TwoAlternativeForced(section, choices, result_pk)
        return view.action()

    @classmethod
    def plan_experiment(cls, session):
        """
        Randomly assign one of four (equal sized) groups to participants        
        S1 = Same direction, Pair 1
        S2 = Same direction, Pair 2
        C1 = Crossed direction, Pair 1
        C2 = Crossed direction, Pair 2
        """

        # Set total size per group
        group_count = 2

        if session.experiment.session_count() <= (group_count * 4):
            group = None
            # Assign a group, if that group is full try again
            while group_count >= 2:
                group = random.choice(['S1', 'S2', 'C1', 'C2'])
                group_count = session.experiment.session_count_groups(group)
            stimuli_a = random.choice(['BLUE', 'ORANGE'])
            session.json_data = {'group': group,
                                 'stimuli_a': stimuli_a}
            session.save()
        return

    def get_trial_with_feedback(session):
        explainer = Explainer()
        trial = Trial()
        return combine_actions(explainer, trial)
