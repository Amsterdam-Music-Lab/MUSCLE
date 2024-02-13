from typing import Final
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .experiment.rules import Base
from .experiment.actions import Consent, Explainer, Final, Playlist, Step
from .section.models import Playlist
from .experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from .experiment.questions.utils import question_by_key


class NewExperiment(Base):
    ID = 'NEW_EXPERIMENT'
    contact_email = 'info@example.com'

    def __init__(self):
        super().__init__(self.ID)
        
        # Add your questions here
        self.questions = [
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_generation'),
            question_by_key('dgf_musical_experience', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_country_of_origin'),
            question_by_key('dgf_education', drop_choices=['isced-2', 'isced-5'])
        ]

    def first_round(self, experiment):
        
        # 1. Informed consent from file or admin (admin has priority)        
        consent = Consent(
            experiment.consent, 
            title=_('Informed consent'), 
            confirm=_('I agree'), 
            deny=_('Stop'), 
            url='consent/consent_new_experiment.html'
            )        
        
        # 2. Choose playlist.
        playlist = Playlist(experiment.playlists.all())

        # 3. Explainer
        explainer = Explainer(
            instruction='',
            steps=[
                Step(description=_('New Experiment is ...')),
                Step(description=_('Next page of explanation')),
                Step(description=_('Another page of explanation')),
            ],
            step_numbers=True
        )
        
        return [
            consent,
            playlist,
            explainer
        ]
    
    def next_round(self, session):
        actions = self.get_questionnaire(session)

        if actions:
            return actions
        
        return [Final()]
    
    def feedback_info(self):
        info = super().feedback_info()
        info['header'] = _("Any remarks or questions (optional):")
        info['thank_you'] = _("Thank you for your feedback!")
        
        return info
    