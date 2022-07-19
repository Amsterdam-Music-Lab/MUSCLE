import random
from .base import Base
from .util.actions import combine_actions
from django.http import Http404, HttpResponseServerError
from .views import Consent, StartSession, TwoAlternativeForced, Trial
from .views.form import Form, Question, ChoiceQuestion
from .views import Consent, Score, StartSession, TwoAlternativeForced
from .views.form import Form, Question
from .views.playback import Playback
<< << << < HEAD
== == == =
>>>>>> > categorization


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
        # Determine or retrieve the group data for this session
        if next_round_number == 1:
            json_data = cls.plan_experiment(session)
        else:
            json_data = session.load_json_data()
        # Retrieve random section for the assigned group
        if json_data["group"] == 'S1':
            section = session.section_from_unused_song(
                {'group': 'SAME', 'tag__contains': '1'})
        elif json_data["group"] == 'S2':
            section = session.section_from_unused_song(
                {'group': 'SAME', 'tag__contains': '2'})
        elif json_data["group"] == 'C1':
            section = session.section_from_unused_song(
                {'group': 'CROSSED', 'tag__contains': '1'})
        elif json_data["group"] == 'C2':
            section = session.section_from_unused_song(
                {'group': 'CROSSED', 'tag__contains': '2'})
        # Determine expected response
        if section.tag == '1A' or section.tag == '2A':
            expected_response = 'A'
        else:
            expected_response = 'B'
        print(expected_response)
        result_pk = Base.prepare_result(session, section, expected_response)
        choices = json_data["choices"]
        config = {
            'decision_time': 5,
            'auto_advance': False,
            'listen_first': True,
            'style': json_data["button_order"],
            'time_pass_break': False
        }
        view = TwoAlternativeForced(section, choices, result_pk, config=config)
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
        group_size = 20
        group_count = group_size
        group = None

        if session.experiment.session_count() <= (group_size * 4):
            # Assign a group, if that group is full try again
            while group_count >= group_size:
                group = random.choice(['S1', 'S2', 'C1', 'C2'])
                group_count = session.experiment.session_count_groups(group)
            # Assign a random correct response color for 1A, 2A
            stimuli_a = random.choice(['BLUE', 'ORANGE'])
            # Determine which button is orange and which is blue
            button_order = random.choice(['neutral', 'neutral-inverted'])
            # Set expected resonse accordingly
            # in the final version the buttons won't show the A/B
            if button_order == 'neutral':
                choices = {'A': 'A', 'B': 'B'}
            else:
                choices = {'B': 'B', 'A': 'A'}
            json_data = {'group': group,
                         'stimuli_a': stimuli_a,
                         'button_order': button_order,
                         'choices': choices
                         }
            session.merge_json_data(json_data)
            session.save()
        else:
            raise Http404(
                "The maximum number of participants for this experiment has been reached")
        return json_data

    def get_trial_with_feedback(session):
        score = Score(session, icon='ti-face-smile', timer=5).action()
        section = session.playlist.section_set.all()[0]
        # retrieve expected response from json_data
        # for now: set it arbitrarily to "up"
        result_pk = cls.prepare_result(session, section, 'up')
        choices = {'A': 'A', 'B': 'B'}
        trial = TwoAlternativeForced(section, choices, result_pk).action()
        return combine_actions(score, trial)

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
