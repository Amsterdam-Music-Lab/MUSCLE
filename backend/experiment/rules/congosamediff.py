from typing import Final
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.actions import Consent, ChoiceQuestion, Explainer, Final, Form, Playlist, Step, Trial
from experiment.actions.playback import Autoplay
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key
from experiment.rules.base import Base
from result.utils import prepare_result


class CongoSameDiff(Base):
    ''' An experiment type that could be used to test musical preferences '''
    ID = 'CONGOSAMEDIFF'
    contact_email = 'info@example.com'

    def __init__(self):
        pass

    def first_round(self, experiment):
        ''' Provide the first rounds of the experiment,
        before session creation
        The first_round must return at least one Info or Explainer action
        Consent and Playlist are often desired, but optional
        '''

        # 1. Playlist
        playlist = Playlist(experiment.playlists.all())

        # 2. Explainer
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
        question = ChoiceQuestion(
            question=_(
                "Is the third sound the SAME or DIFFERENT?"),
            view='BUTTON_ARRAY',
            # Definitely same, Probably same, Probably different, Definitely different, and I don’t know.
            choices={
                'DEFINITELY_SAME': _('DEFINITELY SAME'),
                'PROBABLY_SAME': _('PROBABLY SAME'),
                'PROBABLY_DIFFERENT': _('PROBABLY DIFFERENT'),
                'DEFINITELY_DIFFERENT': _('DEFINITELY DIFFERENT'),
                'I_DONT_KNOW': _('I DON’T KNOW')
            },
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
                'listen_first': True
            }
        )
        return view
    