from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import Http404
from django.db.models import Avg
from operator import ne

from .views.form import Form, Question, ChoiceQuestion
from .views import Consent, Explainer, Score, StartSession, TwoAlternativeForced, Trial, Final

from .util.actions import combine_actions
from .util.iso_languages import ISO_LANGUAGES

from .base import Base
import random


SCORE_AVG_MIN_TRAINING = 0.8


class Categorization(Base):
    ID = 'CATEGORIZATION'

    @classmethod
    def first_round(cls, experiment):
        explainer = Explainer(
            instruction=_(
                "This is a listening experiment in which you have to respond to short sound sequences."),
            steps=[],
            button_label=_('Ok')
        ).action()
        # read consent from file
        rendered = render_to_string(
            'consent/consent_categorization.html')
        consent = Consent.action(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))
        explainer2 = Explainer(
            instruction=_(
                "The experiment will now begin. Click to start a sound sequence."),
            steps=[],
            button_label=_('Ok')
        ).action()
        start_session = StartSession.action()
        return [explainer, consent] + questionaire + [explainer2, start_session]

    @classmethod
    def next_round(cls, session):

        json_data = session.load_json_data()

        # Plan experiment on the first call to next_round
        if not json_data:
            json_data = cls.plan_experiment(session)

        # Check if this participant already has a session
        if json_data == 'REPEAT':
            json_data = {'phase': 'REPEAT'}
            session.merge_json_data(json_data)
            session.save()
            final = Final(
                session=session,
                final_text="You already have participated in this experiment.",
                rank=None,
                show_social=False,
                show_profile_link=False
            ).action()
            return final

        # Total participants reached - Abort with message
        if json_data == 'FULL':
            json_data = {'phase': 'FULL'}
            session.merge_json_data(json_data)
            session.save()
            final = Final(
                session=session,
                final_text="The maximimum number of participants has been reached.",
                rank=None,
                show_social=False,
                show_profile_link=False
            ).action()
            return final

        # Calculate round number from passed training rounds
        rounds_passed = (session.rounds_passed() -
                         int(json_data['training_rounds']))

        # Change phase to enable collecting results of second half of training-1
        if session.rounds_passed() == 10:
            json_data['phase'] = 'training-1B'
            session.merge_json_data(json_data)
            session.save()

        if rounds_passed == 0:
            # Check if participants wants to exit after failed traning
            profiles = session.participant.profile()
            for profile in profiles:
                # Delete results and json from session and exit
                if profile.answer == 'aborted':
                    session.result_set.all().delete()
                    json_data = {'phase': 'ABORTED',
                                 'training_rounds': json_data['training_rounds']}
                    session.save_json_data(json_data)
                    session.save()
                    profile.delete()
                    final = Final(
                        session=session,
                        final_text="Thanks for your participation!",
                        rank=None,
                        show_social=False,
                        show_profile_link=False
                    ).action()
                    return final
            # Prepare sections for next phase
            json_data = cls.plan_phase(session)

        if 'training' in json_data['phase']:

            # Get next training action
            if rounds_passed < len(json_data['sequence']):
                return cls.next_trial_action(session) if rounds_passed == 0 else cls.get_trial_with_feedback(session)

            # Training phase completed, get the results
            training_rounds = int(json_data['training_rounds'])

            if training_rounds == 0:
                this_results = session.result_set.filter(comment='training-1B')
            elif training_rounds == 20:
                this_results = session.result_set.filter(comment='training-2')
            elif training_rounds == 30:
                this_results = session.result_set.filter(comment='training-3')
            # calculate the score for this sequence
            score_avg = this_results.aggregate(Avg('score'))['score__avg']

            # End of training?
            if score_avg >= SCORE_AVG_MIN_TRAINING:
                json_data['phase'] = "testing"
                json_data['training_rounds'] = session.rounds_passed()
                session.merge_json_data(json_data)
                session.save()
                explainer = Explainer(
                    instruction=_(
                        "You are entering the main phase of the experiment. From now on you will only occasionally get feedback on your responses. Simply try to keep responding to the sound sequences as you did before."),
                    steps=[],
                    button_label=_('Ok')
                ).action()
            else:
                # Update passed training rounds for calc round_number
                json_data['training_rounds'] = session.rounds_passed()
                session.merge_json_data(json_data)
                session.save()

                # Failed the training? exit experiment
                if json_data['training_rounds'] == 40:
                    # Clear group from session for reuse
                    end_data = {
                        'assigned_group': json_data['assigned_group'],
                        'button_colors': json_data['button_colors'],
                        'pair_colors': json_data['pair_colors'],
                        'phase': 'FAILED_TRAINING',
                        'training_rounds': json_data['training_rounds'],
                    }
                    session.save_json_data(end_data)
                    session.final_score = 0
                    session.save()
                    profiles = session.participant.profile()
                    for profile in profiles:
                        # Delete failed_training tag from profile
                        if profile.question == 'failed_training':
                            profile.delete()
                    final = Final(
                        session=session,
                        final_text="Thanks for your participation!",
                        rank=None,
                        show_social=False,
                        show_profile_link=True
                    ).action()
                    return final
                else:
                    # Show continue to next training phase or exit option
                    config = {
                        'style': 'boolean'
                    }
                    explainer = Trial(title=_("Training failed"), feedback_form=Form(
                        [repeat_training_or_quit], is_profile=True), config=config).action()

            feedback = cls.get_feedback(session)
            return combine_actions(feedback, explainer)

        elif json_data['phase'] == 'testing':
            if rounds_passed < len(json_data['sequence']):

                # Determine wether this round has feedback
                if rounds_passed in json_data['feedback_sequence']:
                    return cls.get_trial_with_feedback(session)
                return cls.next_trial_action(session)

            # Testing phase completed get results
            this_results = session.result_set.filter(comment='testing')

            # Calculate percentage of correct response to training stimuli
            final_score = 0
            for result in this_results:
                if 'T' in result.section.name and result.score == 1:
                    final_score += 1
            score_percent = 100 * (final_score / 30)

            # assign rank based on percentage of correct response to training stimuli
            if score_percent == 100:
                rank = 'PLATINUM'
                final_text = "Congratulations! You did great and won a platinum medal!"
            elif score_percent >= 80:
                rank = 'GOLD'
                final_text = "Congratulations! You did great and won a gold medal!"
            elif score_percent >= 60:
                rank = 'SILVER'
                final_text = "Congratulations! You did very well and won a silver medal!"
            else:
                rank = 'BRONZE'
                final_text = "Congratulations! You did well and won a bronze medal!"

            # calculate the final score for the entire test sequence
            # final_score = sum([result.score for result in training_results])
            end_data = {
                'assigned_group': json_data['assigned_group'],
                'button_colors': json_data['button_colors'],
                'pair_colors': json_data['pair_colors'],
                'phase': 'FINISHED',
                'training_rounds': json_data['training_rounds'],
                'group': json_data['group']
            }
            session.save_json_data(end_data)
            session.finish()
            session.final_score = final_score
            session.save()
            profiles = session.participant.profile()
            for profile in profiles:
                # Delete failed_training tag from profile
                if profile.question == 'failed_training':
                    profile.delete()
            final = Final(
                session=session,
                final_text=final_text,
                rank=rank,
                show_social=False,
                show_profile_link=False,
                total_score=round(score_percent),
                points='% correct'
            ).action()
            return final

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

        # Set total size per group:
        group_size = 20
        group_count = group_size
        group = None

        # Check for unfinished sessions older then 24 hours caused by closed browser
        all_sessions = session.experiment.session_set.filter(
            finished_at=None).filter(
            started_at__lte=timezone.now()-timezone.timedelta(hours=24)).exclude(
            json_data__contains='ABORTED').exclude(
            json_data__contains='FAILED_TRAINING').exclude(
            json_data__contains='REPEAT').exclude(
            json_data__contains='FULL').exclude(
            json_data__contains='CLOSED_BROWSER')
        for closed_session in all_sessions:
            # Release the group for assignment to a new participant
            closed_json_data = {'phase': 'CLOSED_BROWSER'}
            # Delete results
            closed_session.save_json_data(closed_json_data)
            closed_session.result_set.all().delete()
            closed_session.save()

        # Count sessions with an assigned group
        used_group_count = 0
        used_group_count += session.experiment.session_count_groups('S1')
        used_group_count += session.experiment.session_count_groups('S2')
        used_group_count += session.experiment.session_count_groups('C1')
        used_group_count += session.experiment.session_count_groups('C2')

        # Get sessions for current participant
        current_sessions = session.experiment.session_set.filter(
            participant=session.participant)

        # Check if this participant already has a previous session
        if current_sessions.count() > 1:
            json_data = 'REPEAT'
        else:
            # Total participants reached - Abort with message
            if used_group_count <= (group_size * 4):
                # Assign a group, if that group is full try again
                while group_count >= group_size:
                    group = random.choice(['S1', 'S2', 'C1', 'C2'])
                    group_count = session.experiment.session_count_groups(
                        group)
                # Assign a random correct response color for 1A, 2A
                stimuli_a = random.choice(['BLUE', 'ORANGE'])
                # Determine which button is orange and which is blue
                button_order = random.choice(['neutral', 'neutral-inverted'])
                # Set expected resonse accordingly
                ph = '___'  # placeholder
                if button_order == 'neutral' and stimuli_a == 'BLUE':
                    choices = {'A': ph, 'B': ph}
                elif button_order == 'neutral-inverted' and stimuli_a == 'ORANGE':
                    choices = {'A': ph, 'B': ph}
                else:
                    choices = {'B': ph, 'A': ph}
                if group == 'S1':
                    assigned_group = 'Same direction, Pair 1'
                elif group == 'S2':
                    assigned_group = 'Same direction, Pair 2'
                elif group == 'C1':
                    assigned_group = 'Crossed direction, Pair 1'
                else:
                    assigned_group = 'Crossed direction, Pair 2'
                if button_order == 'neutral':
                    button_colors = 'Blue left, Orange right'
                else:
                    button_colors = 'Orange left, Blue right'
                if stimuli_a == 'BLUE':
                    pair_colors = 'A = Blue, B = Orange'
                else:
                    pair_colors = 'A = Orange, B = Blue'
                json_data = {
                    'assigned_group': assigned_group,
                    'button_colors': button_colors,
                    'pair_colors': pair_colors,
                    'group': group,
                    'stimuli_a': stimuli_a,
                    'button_order': button_order,
                    'choices': choices,
                    'phase': "training",
                    'training_rounds': "0"
                }

                session.merge_json_data(json_data)
                session.save()
            else:
                json_data = 'FULL'
        return json_data

    @classmethod
    def plan_phase(cls, session):

        json_data = session.load_json_data()

        if 'training' in json_data['phase']:
            # Retrieve training stimuli for the assigned group
            if json_data["group"] == 'S1':
                sections = session.playlist.section_set.filter(
                    group='SAME', tag__contains='1', artist__contains='Training')
            elif json_data["group"] == 'S2':
                sections = session.playlist.section_set.filter(
                    group='SAME', tag__contains='2', artist__contains='Training')
            elif json_data["group"] == 'C1':
                sections = session.playlist.section_set.filter(
                    group='CROSSED', tag__contains='1', artist__contains='Training')
            elif json_data["group"] == 'C2':
                sections = session.playlist.section_set.filter(
                    group='CROSSED', tag__contains='2', artist__contains='Training')
            # Generate randomized sequence for the testing phase
            section_sequence = []
            # Add 10 x 2 training stimuli
            if int(json_data['training_rounds']) == 0:
                new_rounds = 10
                json_data['phase'] = 'training-1A'
            elif int(json_data['training_rounds']) == 20:
                json_data['phase'] = 'training-2'
                new_rounds = 5
            else:
                json_data['phase'] = 'training-3'
                new_rounds = 5
            for _ in range(0, new_rounds):
                section_sequence.append(sections[0].id)
                section_sequence.append(sections[1].id)
            random.shuffle(section_sequence)
            json_data['sequence'] = section_sequence

        else:
            # Retrieve test & training stimuli for the assigned group
            if json_data["group"] == 'S1':
                training_sections = session.playlist.section_set.filter(
                    group='SAME', tag__contains='1', artist__contains='Training')
                test_sections = session.playlist.section_set.filter(
                    group='SAME', tag__contains='1').exclude(artist__contains='Training')
            elif json_data["group"] == 'S2':
                training_sections = session.playlist.section_set.filter(
                    group='SAME', tag__contains='2', artist__contains='Training')
                test_sections = session.playlist.section_set.filter(
                    group='SAME', tag__contains='2').exclude(artist__contains='Training')
            elif json_data["group"] == 'C1':
                training_sections = session.playlist.section_set.filter(
                    group='CROSSED', tag__contains='1', artist__contains='Training')
                test_sections = session.playlist.section_set.filter(
                    group='CROSSED', tag__contains='1').exclude(artist__contains='Training')
            elif json_data["group"] == 'C2':
                training_sections = session.playlist.section_set.filter(
                    group='CROSSED', tag__contains='2', artist__contains='Training')
                test_sections = session.playlist.section_set.filter(
                    group='CROSSED', tag__contains='2').exclude(artist__contains='Training')
            # Generate randomized sequence for the testing phase
            section_sequence = []
            # Add 15 x 2 training stimuli
            for _ in range(0, 15):
                section_sequence.append(training_sections[0].id)
                section_sequence.append(training_sections[1].id)
            # add 5 x 10 test stimuli
            length = len(test_sections)
            for _ in range(0, 5):
                for stimulus in range(length):
                    section_sequence.append(test_sections[stimulus].id)
            random.shuffle(section_sequence)
            # Randomly choose 2 x 10 training stimuli for feedback
            sequence_length = len(section_sequence)
            sequence_a = []
            sequence_b = []
            for stimulus in range(sequence_length-1):
                if section_sequence[stimulus] == training_sections[0].id:
                    sequence_a.append((stimulus+1))
                elif section_sequence[stimulus] == training_sections[1].id:
                    sequence_b.append((stimulus+1))
            random.shuffle(sequence_a)
            random.shuffle(sequence_b)
            feedback_sequence = sequence_a[0:10] + sequence_b[0:10]
            json_data['feedback_sequence'] = feedback_sequence
            json_data['sequence'] = section_sequence

        session.merge_json_data(json_data)
        session.save()

        return json_data

    @classmethod
    def get_feedback(cls, session):

        last_score = session.last_score()

        if session.last_result().given_response == "TIMEOUT":
            icon = "ti-help"  # "ti-time"
        elif last_score == 1:
            icon = 'ti-face-smile'
        elif last_score == 0:
            icon = 'ti-face-sad'
        else:
            pass  # throw error

        return Score(session, icon=icon, timer=1, title=cls.get_title(session)).action()

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
        json_data = session.load_json_data()

        # Retrieve next section in the sequence
        rounds_passed = (session.rounds_passed() -
                         int(json_data['training_rounds']))
        sequence = json_data['sequence']
        this_section = sequence[rounds_passed]
        section = session.section_from_song(this_section)
        # Determine expected response
        if section.tag == '1A' or section.tag == '2A':
            expected_response = 'A'
        else:
            expected_response = 'B'
        result_pk = cls.prepare_result(session, section, expected_response)
        # Set the current phase in the result comment
        this_result = session.last_result()
        this_result.comment = json_data['phase']
        this_result.save()
        choices = json_data["choices"]
        trial = TwoAlternativeForced(
            section, choices, result_pk, title=cls.get_title(session))
        trial.config['listen_first'] = True
        trial.config['auto_advance'] = True
        trial.config['auto_advance_timer'] = 2500
        trial.config['style'] = json_data["button_order"]
        trial.config['time_pass_break'] = False

        return trial.action()

    @staticmethod
    def calculate_score(result, data, form_element):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            expected_response = None
        if expected_response and expected_response == form_element['value']:
            return 1
        else:
            return 0

    @classmethod
    def get_title(cls, session):
        json_data = session.load_json_data()
        rounds_passed = (session.rounds_passed() -
                         int(json_data['training_rounds']))
        return _('Round {} / {}').format(rounds_passed, len(json_data['sequence']))


age_question = Question(
    key='age',
    view='STRING',
    question=_('What is your age?')
)

gender_question = ChoiceQuestion(
    key='gender',
    view='RADIOS',
    question="What is your gender?",
    choices={
        'M': "Male",
        'F': "Female",
        'X': "Other",
        'U': "Undisclosed"
    },
    is_skippable=True
)

language_question = ChoiceQuestion(
    key='native_language',
    view='DROPDOWN',
    question="What is your native language?",
    choices=ISO_LANGUAGES,
    is_skippable=True
)

musical_experience_question = ChoiceQuestion(
    key='musical_experience',
    view='RADIOS',
    question="Please select your level of musical experience:",
    choices={
        'none': "None",
        'moderate': "Moderate",
        'extensive': "Extensive",
        'professional': "Professional"
    },
    is_skippable=True
)

questions = [age_question, gender_question,
             language_question, musical_experience_question]
questionaire = [
    Trial(
        title=_("Questionnaire"),
        feedback_form=Form([question], is_profile=True)).action()
    for question in questions
]

repeat_training_or_quit = ChoiceQuestion(
    key='failed_training',
    view='BUTTON_ARRAY',
    question='You seem to have difficulties reacting correctly to the sound sequences. Is your audio on? If you want to give it another try, click on Ok.',
    choices={
        'continued': "OK",
        'aborted': "Exit"
    },
    submits=True,
    is_skippable=False,
    config={'buttons_large_gap': True}
)
