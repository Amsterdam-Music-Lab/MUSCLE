from typing import Final
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.actions import Consent, BooleanQuestion, Explainer, Final, Form, Playlist, Step, Trial
from experiment.actions.playback import Autoplay
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key
from experiment.rules.base import Base
from result.utils import prepare_result


class NewExperiment(Base):
    ''' An experiment type that could be used to test musical preferences '''
    ID = 'NEW_EXPERIMENT'
    contact_email = 'info@example.com'

    def __init__(self):

        # Add your questions here
        self.questions = [
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_generation'),
            question_by_key('dgf_musical_experience', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_country_of_origin'),
            question_by_key('dgf_education', drop_choices=[
                            'isced-2', 'isced-5'])
        ]

    def first_round(self, experiment):
        ''' Provide the first rounds of the experiment, 
        before session creation
        The first_round must return at least one Info or Explainer action
        Consent and Playlist are often desired, but optional
        '''
        # 1. Informed consent (optional)
        rendered = render_to_string('consent/consent.html')
        consent = Consent(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))
        
        # 2. Choose playlist (optional, only relevant if there are multiple playlists the participant can choose from)
        playlist = Playlist(experiment.playlists.all())

        # 3. Explainer
        explainer = Explainer(
            instruction='Welcome to this new experiment',
            steps=[
                Step(description=_('Please read the instructions carefully')),
                Step(description=_('Next step of explanation')),
                Step(description=_('Another step of explanation')),
            ],
            step_numbers=True
        )
        
        return [
            consent,
            playlist,
            explainer
        ]
    
    def next_round(self, session):
        # ask any questions defined in the admin interface
        actions = self.get_questionnaire(session)
        if actions:
            return actions

        elif session.rounds_complete():
            # we have as many results as rounds in this experiment
            # finish session and show Final view
            session.finish()
            session.save()
            return [
                Final(
                    session,
                    final_text=_('Thank you for participating!'),
                    feedback_info=self.feedback_info()  # show feedback bar, this line can be removed
                )
            ]
        else:
            return self.get_trial(session)

    def get_trial(self, session):
        # define a key, by which responses to this trial can be found in the database
        key = 'test_trial'
        # get a random section
        section = session.section_from_any_song()
        question = BooleanQuestion(
            question=_(
                "Do you like this song?"),
            key=key,
            result_id=prepare_result(key, session, section=section),
            submits=True
        )
        form = Form([question])
        playback = Autoplay([section])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Test experiment'),
            config={
                'response_time': section.duration,
                # listen_first: whether response buttons will be greyed out during `response_time`
                'listen_first': True
            }
        )
        return view
    