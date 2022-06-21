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
        # Get the next trial action
        action = cls.next_trial_action(session)

        return action

    @classmethod
    def next_trial_action(cls, session, *kwargs):
        """
        Get the next action for the experiment
        """
        next_round_number = session.get_next_round()
        # Determine the group for this session
        if next_round_number == 1:
            assigned_group = cls.plan_experiment(session)
        else:
            assigned_group = session.json_data.get('group')
        # Retrieve secions for the assigned group
        if assigned_group == 'S1':
            section = session.playlist.section_set.filter(
                group='SAME', tag='1A')[next_round_number-1]
        elif assigned_group == 'S2':
            section = session.playlist.section_set.filter(
                group='SAME', tag='2A')[next_round_number-1]
        elif assigned_group == 'C1':
            section = session.playlist.section_set.filter(
                group='CROSSED', tag='1A')[next_round_number-1]
        elif assigned_group == 'C2':
            section = session.playlist.section_set.filter(
                group='CROSSED', tag='2A')[next_round_number-1]
        # retrieve expected response from json_data
        # for now: set it arbitrarily to "B"
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

        BLUE / ORANGE = Correct response for Pair 1A, Pair 2A
        """        
        # Make sure to delete existing sessions before starting the real experiment
        # as the creation of groups looks at the sessions to balance out the participants 
        # Set total size per group:
        group_count = 20

        if session.experiment.session_count() <= (group_count * 4):
            group = None
            # Assign a group, if that group is full try again
            while group_count >= 2:
                group = random.choice(['S1', 'S2', 'C1', 'C2'])
                group_count = session.experiment.session_count_groups(group)
            # assign a correct response for 1A, 2A
            stimuli_a = random.choice(['BLUE', 'ORANGE'])
            session.json_data = {'group': group,
                                 'stimuli_a': stimuli_a}
            session.save()
        return group

    def get_trial_with_feedback(session):
        explainer = Explainer()
        trial = Trial()
        return combine_actions(explainer, trial)

    @staticmethod
    def calculate_score(result, form_element, data):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            # logger.log(e)
            expected_response = None
        if expected_response and expected_response == form_element['value']:
            return 1
        else:
            return 0
