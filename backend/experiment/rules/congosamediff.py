
import re
import string
from django.utils.translation import gettext_lazy as _
from experiment.actions.utils import final_action_with_optional_button
from experiment.models import Block
from section.models import Playlist as PlaylistModel
from session.models import Session
from experiment.actions import ChoiceQuestion, Explainer, Form, Playlist, Trial
from experiment.actions.playback import PlayButton
from .base import Base
from result.utils import prepare_result


class CongoSameDiff(Base):
    """ A micro-PROMS inspired experiment block that tests the participant's ability to distinguish between different sounds. """
    ID = 'CONGOSAMEDIFF'
    contact_email = 'aml.tunetwins@gmail.com'

    def __init__(self):
        pass

    def first_round(self, block: Block):
        """ Provide the first rounds of the block,
        before session creation
        The first_round must return at least one Info or Explainer action
        Consent and Playlist are often desired, but optional
        """

        # Do a validity check on the block
        errors = self.validate_playlist(block.playlists.first())
        if errors:
            raise ValueError('The block playlist is not valid: \n- ' + '\n- '.join(errors))

        # 1. Playlist
        playlist = Playlist(block.playlists.all())

        # 2. Explainer
        explainer = Explainer(
            instruction='Welcome to this Musicality Battery block',
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

        # load the non-practice group variants for the group number
        real_trial_variants = session.playlist.section_set.exclude(
            tag__contains='practice'
        ).filter(
            group=group_number
        )

        # patterns amount is the number of groups times the number of variants in each group
        groups_amount = session.playlist.section_set.values('group').distinct().count()
        variants_amount = real_trial_variants.count()

        # get the participant's group variant based on the participant's id # else default to random number between 1 and variants_amount
        participant_id = session.participant.id
        participant_group_variant = self.get_participant_group_variant(
            participant_id,
            group_number,
            groups_amount,
            variants_amount
        )

        # get the index of the participant's group variant in the real_trial_variants
        # aka the index of the variant whose tag matches the participant's group variant
        real_trial_variants_list = list(real_trial_variants)
        pattern_group_variants_index = [
            i for i, variant in enumerate(real_trial_variants_list)
            if variant.tag == participant_group_variant
        ][0]

        # if the next_round_number is greater than the no. of practice trials,
        # return a non-practice trial
        return self.get_next_trial(
            session,
            real_trial_variants,
            pattern_group_variants_index + 1,
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
        section_artist = section.song.artist if section.song else 'NO_EXPECTED_RESPONSE'

        # define a key, by which responses to this trial can be found in the database
        key = f'samediff_trial_{section_group}_{section_name}'

        # set artist field as expected_response in the results
        expected_response = section_artist

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
            result_id=prepare_result(key, session, section=section, expected_response=expected_response),
            submits=True
        )
        form = Form([question])
        playback = PlayButton([section], play_once=False)
        block_name = session.block.name if session.block else 'Musicality Battery Block'
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_(block_name),
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

        return final_action_with_optional_button(
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

    def validate_playlist(self, playlist: PlaylistModel):

        errors = []

        errors += super().validate_playlist(playlist)  # Call the base class validate_playlist to perform common checks

        # All sections need to have a group value
        sections = playlist.section_set.all()
        for section in sections:
            file_name = section.song.name if section.song else 'No name'
            # every section.group should consist of a number
            regex_pattern = r'^\d+$'
            if not section.group or not re.search(regex_pattern, section.group):
                errors.append(f'Section {file_name} should have a group value containing only digits')
            # the section song name should not be empty
            if not section.song.name:
                errors.append(f'Section {file_name} should have a name that will be used for the result key')

        # It also needs at least one section with the tag 'practice'
        if not sections.filter(tag__contains='practice').exists():
            errors.append('At least one section should have the tag "practice"')

        # It should also contain at least one section without the tag 'practice'
        if not sections.exclude(tag__contains='practice').exists():
            errors.append('At least one section should not have the tag "practice"')

        # Every non-practice group should have the same number of variants
        # that should be labeled with a single uppercase letter
        groups = sections.values('group').distinct()
        variants = sections.exclude(tag__contains='practice').values('tag')
        unique_variants = set([variant['tag'] for variant in variants])
        variants_count = len(unique_variants)
        for group in groups:
            group_variants = sections.filter(group=group['group']).exclude(tag__contains='practice').values('tag').distinct()

            for variant in group_variants:
                if not re.search(r'^[A-Z]$', variant['tag']):
                    errors.append(f'Group {group["group"]} should have variants with a single uppercase letter (A-Z), but has {variant["tag"]}')

            if group_variants.count() != variants_count:
                group_variants_stringified = ', '.join([variant['tag'] for variant in group_variants])
                total_variants_stringified = ', '.join(unique_variants)
                errors.append(f'Group {group["group"]} should have the same number of variants as the total amount of variants ({variants_count}; {total_variants_stringified}) but has {group_variants.count()} ({group_variants_stringified})')

        return errors

    def get_participant_group_variant(self, participant_id: int, group_number: int, groups_amount: int, variants_amount: int) -> str:

        if participant_id <= 0:
            raise ValueError(f"Participant id ({participant_id}) should be larger than 0")

        if group_number <= 0:
            raise ValueError(f"Group number ({group_number}) should be larger than 0")

        if groups_amount <= 0:
            raise ValueError(f"Groups amount ({groups_amount}) should be larger than 0")

        if variants_amount <= 0:
            raise ValueError(f"Variants amount ({variants_amount}) should be larger than 0")

        # Generate variant labels (e.g., ['A', 'B', 'C'])
        variants = list(string.ascii_uppercase)[:variants_amount]

        total_patterns = len(variants)

        participant_index = participant_id - 1

        group_index = group_number - 1

        # Determine if the pattern should be reversed (every 4th, 5th, 6th participant)
        reversed_pattern = participant_index % (variants_amount * 2) >= variants_amount

        # Calculate the participant's group variant
        if reversed_pattern:
            variant_index = (participant_index - group_index) % total_patterns
        else:
            variant_index = (participant_index + group_index) % total_patterns

        return variants[variant_index]
