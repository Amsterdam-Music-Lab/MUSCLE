
from django.utils.translation import gettext_lazy as _
from experiment.actions.final import Final
from experiment.models import Experiment
from session.models import Session
from experiment.actions import ChoiceQuestion, Explainer, Form, Playlist, Trial
from experiment.actions.playback import Autoplay
from .base import Base
from result.utils import prepare_result


class CongoSameDiff(Base):
    ''' A micro-PROMS inspired experiment that tests the participant's ability to distinguish between different sounds. '''
    ID = 'CONGOSAMEDIFF'
    contact_email = 'aml.tunetwins@gmail.com'

    def __init__(self):
        pass

    def first_round(self, experiment: Experiment):
        ''' Provide the first rounds of the experiment,
        before session creation
        The first_round must return at least one Info or Explainer action
        Consent and Playlist are often desired, but optional
        '''

        # 1. Playlist
        playlist = Playlist(experiment.playlists.all())

        # 2. Explainer
        explainer = Explainer(
            instruction='Welcome to this Same Diff experiment',
            steps=[],
            step_numbers=True
        )

        return [
            playlist,
            explainer
        ]

    def next_round(self, session: Session):

        next_round_number = session.get_next_round()

        # total number of trials
        total_trials_count = session.playlist.section_set.count()

        # if the next_round_number is greater than the total number of trials,
        # return a final action
        if next_round_number > total_trials_count:
            return self.get_final_round(session)

        # count of practice rounds
        practice_trials_count = session.playlist.section_set.filter(
            tag__contains='practice'
        ).count()

        # if the next_round_number is less than the number of practice trials,
        # return a practice trial
        if next_round_number <= practice_trials_count:
            subset = session.playlist.section_set.filter(
                tag__contains='practice')
            
            return self.get_next_trial(
                session,
                subset,
                next_round_number,
                True
            )
        
        subset = session.playlist.section_set.exclude(
            tag__contains='practice')

        # if the next_round_number is greater than the no. of practice trials,
        # return a non-practice trial
        return self.get_next_trial(
            session,
            subset,
            next_round_number - practice_trials_count,
            False
        )

    def get_next_trial(
            self,
            session: Session,
            subset: Playlist,
            trial_index: int,
            is_practice=False
    ):
        # define a key, by which responses to this trial can be found in the database
        key = 'samediff_trial'
        # get a section based on the practice tag and the trial_index
        section = subset.all()[trial_index - 1]
        subset_count = subset.count()

        practice_label = 'PRACTICE' if is_practice else 'NORMAL'
        section_name = section.song.name
        section_tag = section.tag
        section_group = section.group

        question = ChoiceQuestion(
            explainer=f'{practice_label} ({trial_index}/{subset_count}) | {section_name} | {section_tag} | {section_group}',
            question=_('Is the third sound the SAME or DIFFERENT as the first two sounds?'),
            view='BUTTON_ARRAY',
            choices={
                'DEFINITELY_SAME': _('DEFINITELY SAME'),
                'PROBABLY_SAME': _('PROBABLY SAME'),
                'PROBABLY_DIFFERENT': _('PROBABLY DIFFERENT'),
                'DEFINITELY_DIFFERENT': _('DEFINITELY DIFFERENT'),
                'I_DONT_KNOW': _('I DON’T KNOW'),
            },
            style={},
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
    
    def get_final_round(self, session: Session):
        # Finish session
        session.finish()
        session.save()

        return Final(
            title=_('End'),
            session=session,
            final_text=_('Thank you for participating!'),
        )

