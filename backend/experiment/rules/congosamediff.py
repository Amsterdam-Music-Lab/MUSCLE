
import random
import re
from django.utils.translation import gettext_lazy as _
from experiment.actions.final import Final
from experiment.models import Experiment
from section.models import Playlist as PlaylistModel
from session.models import Session
from experiment.actions import ChoiceQuestion, Explainer, Form, Playlist, Trial
from experiment.actions.playback import PlayButton
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

        # Do a validity check on the experiment
        # All sections need to have a group value
        sections = experiment.playlists.first().section_set.all()
        for section in sections:
            file_name = section.song.name if section.song else 'No name'
            # every section.group should consist of a number
            regex_pattern = r'^\d+$'
            if not section.group or not re.search(regex_pattern, section.group):
                raise ValueError(f'Section {file_name} should have a group value containing only digits')
            # the section song name should not be empty
            if not section.song.name:
                raise ValueError(f'Section {file_name} should have a name that will be used for the result key')

        # It also needs at least one section with the tag 'practice'
        if not sections.filter(tag__contains='practice').exists():
            raise ValueError('At least one section should have the tag "practice"')

        # It should also contain at least one section without the tag 'practice'
        if not sections.exclude(tag__contains='practice').exists():
            raise ValueError('At least one section should not have the tag "practice"')

        # 1. Playlist
        playlist = Playlist(experiment.playlists.all())

        # 2. Explainer
        explainer = Explainer(
            instruction='Welcome to this Same Diff experiment',
            steps=[],
        )

        return [
            playlist,
            explainer
        ]

    def next_round(self, session: Session):

        next_round_number = session.get_current_round()

        # practice trials + post-practice question + non-practice trials
        total_trials_count = self.get_total_trials_count(session)

        practice_done = session.result_set.filter(
            question_key='practice_done',
            given_response='YES'
        ).exists()

        # if the participant has completed all trials, return the final round
        if next_round_number > total_trials_count:
            return self.get_final_round(session)

        # load the practice trials
        practice_trials_subset = session.playlist.section_set.filter(
            tag__contains='practice'
        )

        # count of practice rounds (excluding the post-practice round)
        practice_trials_count = practice_trials_subset.count()

        # if the user hasn't completed the practice trials
        # return the next practice trial
        if next_round_number <= practice_trials_count:
            return self.get_next_trial(
                session,
                practice_trials_subset,
                next_round_number,
                True
            )

        # if the participant has not completed the practice trials correctly
        # reset the rounds and return the first practice trial
        if next_round_number > practice_trials_count + 1 and not practice_done:
            session.reset_rounds()

            return self.get_next_trial(
                session,
                practice_trials_subset,
                1,  # first practice trial
                True
            )

        # if the participant has completed the practice trials
        # ask if the participant has completed the practice trials correctly
        # yes will move the participant to the non-practice trials
        # no will reset the rounds and return the first practice trial
        if next_round_number == practice_trials_count + 1 and not practice_done:
            return self.get_practice_done_view(session)

        # group number of the trial to be played
        group_number = next_round_number - practice_trials_count - 1

        # load the non-practice trial variants for the group number
        real_trial_variants = session.playlist.section_set.exclude(
            tag__contains='practice'
        ).filter(
            group=group_number
        )

        # pick a variant from the variants randomly (#919)
        variants_count = real_trial_variants.count()
        random_variants_index = random.randint(0, variants_count - 1)

        # if the next_round_number is greater than the no. of practice trials,
        # return a non-practice trial
        return self.get_next_trial(
            session,
            real_trial_variants,
            random_variants_index + 1,
            False
        )

    def get_practice_done_view(self, session: Session):

        key = 'practice_done'
        result_pk = prepare_result(key, session, expected_response=key)

        question = ChoiceQuestion(
            question="Did the participant complete the practice round correctly?",
            key=key,
            choices={
                "YES": "Yes, continue",
                "NO": "No, restart the practice trials",
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True,
        )

        form = Form([question])

        trial = Trial(
            feedback_form=form,
            title='Practice Done',
        )

        return [trial]

    def get_next_trial(
            self,
            session: Session,
            subset: PlaylistModel,
            trial_index: int,
            is_practice=False
    ):
        # get a section based on the practice tag and the trial_index
        section = subset.all()[trial_index - 1]
        subset_count = subset.count()

        practice_label = 'PRACTICE' if is_practice else 'NORMAL'
        section_name = section.song.name if section.song else 'no_name'
        section_tag = section.tag if section.tag else 'no_tag'
        section_group = section.group if section.group else 'no_group'

        # define a key, by which responses to this trial can be found in the database
        key = f'samediff_trial_{section_group}_{section_name}'

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
        playback = PlayButton([section], play_once=False)
        experiment_name = session.experiment.name if session.experiment else 'SameDiff Experiment'
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_(experiment_name),
            config={
                'response_time': section.duration,
                'listen_first': False,
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

    def get_total_trials_count(self, session: Session):
        practice_trials_subset = session.playlist.section_set.filter(
            tag__contains='practice'
        )
        practice_trials_count = practice_trials_subset.count()
        total_exp_variants = session.playlist.section_set.exclude(
            tag__contains='practice'
        )
        total_unique_exp_trials_count = total_exp_variants.values('group').distinct().count()
        total_trials_count = practice_trials_count + total_unique_exp_trials_count + 1
        return total_trials_count
