import random
import logging

from django.utils.translation import gettext_lazy as _

from .base import Base
from .views import CompositeView, Explainer, Consent, StartSession, Question
from .views.form import ChoiceQuestion, Form
from .util.questions import question_by_key
from .util.actions import combine_actions, final_action_with_optional_button

logger = logging.getLogger(__name__)

class BeatAlignment(Base):
    """Rules for the beat alignment test by Mullensiefen et al. (2014)"""

    ID = 'BEAT_ALIGNMENT'

    @staticmethod
    def first_round(experiment):
        """Create data for the first experiment rounds"""

        # 1. General explainer
        explainer = Explainer.action(
            instruction=_(
                "This test measures your ability to recognize the beat in a piece of music."),
            steps=[
                Explainer.step(
                    description=_(
                        "Listen to the following music fragments. In each fragment you hear a series of beeps."),
                    number=1),
                Explainer.step(
                    description=_(
                        "It's you job to decide if the beeps are ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT of the music."),
                    number=2
                ),
                Explainer.step(
                    description=_(
                        "Listen carefully to this. Pay close attention to the description that accompanies each example."),
                    number=3
                )
            ], button_label=_('Ok')
            )

        # 2. Consent with default text
        consent = Consent.action()

        # 3. Practice rounds
        practice_list = experiment.playlists.first()
        practice_rounds = [BeatAlignment.next_practice_action(practice_list, i) for i in range(1,4)]
        practice_rounds.append(Explainer.action(
            instruction=_('You will now hear 17 music fragments.'),
            steps=[
                Explainer.step(
                    description=_(
                        'With each fragment you have to decide if the beeps are ALIGNED TO THE BEAT, or NOT ALIGNED TO THE BEAT of the music.')
                    ),
                Explainer.step(
                    description=_(
                        'We will also ask you how certain you are of your answer. Pay attention: a music fragment can occur several times.')
                    )
            ],
            button_label=_('Start'))
        )

        # 5. Start session
        start_session = StartSession.action()
        return combine_actions(
            explainer,
            consent,
            *practice_rounds,
            start_session
        )


    @staticmethod
    def next_round(session, series=None):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds
        # Close the session and return data for the final_score view
        if session.rounds_complete():
            # Finish session
            session.finish()
            session.save()

            percentage = (sum([r.score for r in session.result_set.all()]) / session.experiment.rounds) * 100
            score_message=_('Well done! You’ve answered {} percent correctly!').format(percentage)
            return final_action_with_optional_button(session, score_message, series)

        # Next round number, can be used to return different actions
        next_round_number = session.get_next_round()
        actions = []

        actions.append(BeatAlignment.next_trial_action(session, next_round_number))
        actions.append(Question.radios(
            key='certainty',
            question=_('How certain are you of your answer?'),
            choices=[_('I guessed'), _('I think I know'), _('I am sure')],
            view=Question.ID_RESULT_QUESTION,
            button_label=_('Next fragment'),
            skip_label=None
        ))
        return combine_actions(*actions)
    
    @staticmethod
    def next_practice_action(playlist, count):
        """Get action data for the next practice round"""
        section = playlist.section_set.filter(name__startswith='ex{}'.format(count)).first()
        if not section:
            return None
        
        if count==1:
            presentation_text = _(
                "In this example the beeps are ALIGNED TO THE BEAT of the music. The correct answer was ALIGNED TO THE BEAT.")
        else:
            presentation_text = _(
                "In this example the beeps are NOT ALIGNED TO THE BEAT of the music. The correct answer was NOT ALIGNED TO THE BEAT.")
        
        instructions = {
            'preload': '',
            'during_presentation': presentation_text
        }

        view = CompositeView(
            section=section,
            feedback_form=None,
            instructions=instructions,
            title=_('Example {}').format(count)
        )
        config = {
            'listen_first': True,
            'decision_time': section.duration + .5
        }
        return view.action(config)

    @staticmethod
    def next_trial_action(session, this_round):
        """Get next section for given session"""
        filter_by = {'tag_id': 0}
        section = session.section_from_unused_song(filter_by)
        condition = section.filename.split('_')[-1][:-4]
        expected_result = 'ON' if condition=='on' else 'OFF'
        result_pk = Base.prepare_result(session, section, expected_result)
        question = ChoiceQuestion(
            question=_("Are the beeps ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT?"),
            key='aligned',
            choices={
                'ON': _('ALIGNED TO THE BEAT'),
                'OFF': _('NOT ALIGNED TO THE BEAT')
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )   
        form = Form([question])
        instructions = {
            'preload': '',
            'during_presentation': ''
        }
        view = CompositeView(
            section=section,
            feedback_form=form.action(),
            instructions=instructions,
            title=_('Beat alignment')
        )
        config = {
            'listen_first': True,
            'decision_time': section.duration
        }
        action = view.action(config=config)
        return action
    
    @staticmethod
    def calculate_score(result, form_element):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == form_element['value']:
            return 1
        else:
            return 0
    
    @staticmethod
    def handle_result(session, section, data):
        return Base.handle_results(session, section, data)

















