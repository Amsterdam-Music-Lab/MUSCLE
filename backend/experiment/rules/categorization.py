from operator import ne
from .views.playback import Playback
from .views.form import Form, Question, ChoiceQuestion
from .views import Consent, Explainer, Score, StartSession, TwoAlternativeForced, Trial, Final
from django.http import Http404, HttpResponseServerError
from .util.actions import combine_actions
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg

from .base import Base
import random


N_ROUNDS_TRAINING = 5# 20
SCORE_AVG_MIN_TRAINING = 0.8

class Categorization(Base):
    ID = 'CATEGORIZATION'

    @classmethod
    def first_round(cls, experiment):
        explainer = Explainer(
            instruction=_("This is a listening experiment in which you have to categorize short sound fragments"),
            steps = [],
            button_label=_('Ok')
            ).action()
        consent = Consent.action()
        start_session = StartSession.action()
        return [explainer,consent] + questionaire + [start_session]

    @classmethod
    def next_round(cls, session):

        json_data = session.load_json_data()

        # Plan experiment on the first call to next_round
        if not json_data:
            json_data = cls.plan_experiment(session)

        rounds_passed = session.rounds_passed()

        if json_data['phase'] == 'training':
            if rounds_passed < N_ROUNDS_TRAINING:
                return cls.next_trial_action(session) if rounds_passed == 0 else cls.get_trial_with_feedback(session)
            else:
                # End of training?
                score_avg = session.result_set.aggregate(Avg('score'))['score__avg']

                if score_avg > SCORE_AVG_MIN_TRAINING:
                    json_data['phase'] = "testing"
                    session.merge_json_data(json_data)
                    session.save()
                    explainer = Explainer(
                        instruction=_("You are entering the main phase of the experiment. From now on you will only occasionally get feedback on your responses. Simply try to keep on categorizing the sound sequences as you did before."),
                        steps = [],
                        button_label=_('Ok')
                    ).action()
                else:
                    explainer = Explainer(
                        instruction=_("<REPEAT TRAINING>"),
                        steps = [],
                        button_label=_('Ok')
                    ).action()

                feedback = cls.get_feedback(session)
                session.result_set.all().delete()

                return combine_actions(feedback, explainer)

        elif json_data['phase'] == 'testing':
            if session.rounds_complete():
                session.final_score = session.result_set.aggregate(Avg('score'))['score__avg']
                session.finish()
                session.save()

                final = Final(
                    session=session,
                    final_text="WOOHOO!",#Huang2022.final_score_message(session),
                    rank=1,#Huang2022.rank(session),
                    show_social=False,
                    show_profile_link=True
                ).action()

                return final
            else:
                # To do: switch between trial with feedback and without
                return cls.next_trial_action(session) if rounds_passed == 0 else cls.get_trial_with_feedback(session)


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
            if button_order == 'neutral' and stimuli_a == 'BLUE':
                choices = {'A': 'A', 'B': 'B'}
            elif button_order == 'neutral-inverted' and stimuli_a == 'ORANGE':
                choices = {'A': 'A', 'B': 'B'}
            else:
                choices = {'B': 'B', 'A': 'A'}
            json_data = {'group': group,
                         'stimuli_a': stimuli_a,
                         'button_order': button_order,
                         'choices': choices,
                         'phase': "training"
                         }
            session.merge_json_data(json_data)
            session.save()
        else:
            raise Http404(
                "The maximum number of participants for this experiment has been reached")
        return json_data

    @classmethod
    def get_feedback(cls, session):

        last_score = session.last_score()

        if session.last_result().given_response == "TIMEOUT":
            icon = "ti-alarm-clock"  # "ti-time"
        elif last_score == 1:
            icon = 'ti-face-smile'
        elif last_score == 0:
            icon = 'ti-face-sad'
        else:
            pass #throw error

        return Score(session, icon=icon, timer=3).action()

    @classmethod
    def get_trial_with_feedback(cls, session):

        score = cls.get_feedback(session)
        trial = cls.next_trial_action(session)

        return combine_actions(score, trial)

    @classmethod
    def next_trial_action(cls, session):
        """
        Get the next action for the experiment
        """
        section = session.playlist.section_set.all()[0]
        # retrieve expected response from json_data
        # for now: set it arbitrarily to "up"
        result_pk = cls.prepare_result(session, section, 'A')
        choices = {'A': 'A', 'B': 'B'}
        trial = TwoAlternativeForced(section, choices, result_pk)
        trial.config['listen_first'] = True
        trial.config['auto_advance'] = True
        trial.config['auto_advance_timer'] = 3000
        #trial.config['show_continue_button'] = True
        return trial.action()

        # Retrieve the group data for this session
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
        result_pk = cls.prepare_result(session, section, expected_response)
        choices = json_data["choices"]
        config = {
            'decision_time': 5,
            'auto_advance': False,
            'listen_first': False,
            'style': json_data["button_order"],
            'time_pass_break': False
        }
        view = TwoAlternativeForced(section, choices, result_pk, config=config)
        return view.action()

    @staticmethod
    def calculate_score(result, data, form_element):
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



age_question = Question(
    key='age',
    view='STRING',
    question=_('What is your age?')
)

gender_question = ChoiceQuestion(
    key='gender_identity',
    view='RADIOS',
    question="What is your gender?",
    choices={
        'male': "Male",
        'Female': "Female",
        'Others': "Other",
        'no_answer': "Prefer not to disclose"
    },
    is_skippable=True
)

musical_expertise_question = ChoiceQuestion(
    key='musical_expertise',
    view='RADIOS',
    question="Please select your level of musical expertise:",
    choices={
        'none': "None",
        'moderate': "Moderate",
        'experienced': "Experienced",
        'professional': "Professional"
    },
    is_skippable=True
)

questions = [age_question, gender_question, musical_expertise_question]
questionaire = [ 
    Trial(
        title=_("Questionnaire"),
        feedback_form=Form([question], is_profile=True)).action() 
    for question in questions
]

