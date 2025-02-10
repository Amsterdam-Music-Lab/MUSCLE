import itertools
import re

from django.utils.translation import gettext_lazy as _
from experiment.actions.utils import final_action_with_optional_button
from section.models import Playlist, Section
from session.models import Session
from experiment.actions import ChoiceQuestion, Explainer, Form, Trial
from experiment.actions.playback import PlayButton
from .base import BaseRules
from result.utils import prepare_result


class CongoSameDiff(BaseRules):
    """ A micro-PROMS inspired experiment block that tests the participant's ability to distinguish between different sounds. """
    ID = 'CONGOSAMEDIFF'
    contact_email = 'aml.tunetwins@gmail.com'
    counted_result_keys = ['samediff_NORMAL']

    def next_round(self, session: Session):
        practice_done = session.result_set.filter(
            question_key='practice_done',
            given_response='YES'
        ).exists()

        if practice_done:
            round_number = session.get_rounds_passed(self.counted_result_keys)
            total_trials_count = self.get_total_trials_count(session)

            # if the participant has completed all trials, return the final round
            if round_number == total_trials_count:
                return self.get_final_round(session)

            # otherwise, return a normal trial
            # load the non-practice group variants for the group number
            real_trial_variants = session.playlist.section_set.exclude(
                tag__contains='practice'
            )

            # inventorize the groups, and the number of variants in each group
            groups = real_trial_variants.values_list('group', flat=True).order_by().distinct()
            variants = real_trial_variants.values_list('tag', flat=True).order_by().distinct()

            # get the participant's group variant based on the participant's id # else default to random number between 1 and variants_amount
            participant_id = session.participant.id
            group = groups[participant_id % len(groups)]
            variant_tag = self.get_participant_group_variant(
                participant_id,
                round_number,
                groups,
                variants
            )
            section = real_trial_variants.get(group=group, tag=variant_tag)

            return self.get_next_trial(
                session,
                section,
                round_number,
                total_trials_count,
                False
            )

        else:
            # practice is not done yet;
            # load the practice trials
            round_number = session.get_rounds_passed()
            practice_trials_subset = session.playlist.section_set.filter(
                tag__contains='practice'
            )

            # count of practice rounds (excluding the post-practice round)
            practice_trials_count = practice_trials_subset.count()
            practice_round_index = round_number % practice_trials_count
            section = practice_trials_subset.all()[practice_round_index]

            if round_number == 0:
                explainer = Explainer(
                    instruction='Welcome to this Musicality Battery block',
                    steps=[],
                )
                return [explainer, self.get_next_trial(
                    session,
                    section,
                    round_number,
                    practice_trials_count,
                    True
                )]
            # check if the practice was successful according to experimenter
            elif practice_round_index == 0:
                return self.get_practice_done_view(session)
            else:
                return self.get_next_trial(
                    session,
                    section,
                    round_number,
                    practice_trials_count,
                    True
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

        return trial

    def get_next_trial(
            self,
            session: Session,
            section: Section,
            trial_index: int,
            trials_count: int,
            is_practice=False
    ):
        practice_label = 'PRACTICE' if is_practice else 'NORMAL'
        section_name = section.song.name if section.song else 'no_name'
        section_tag = section.tag if section.tag else 'no_tag'
        section_group = section.group if section.group else 'no_group'

        # define a key, by which responses to this trial can be found in the database
        key = f'samediff_{practice_label}'

        # set artist field as expected_response in the results
        expected_response = section.filename

        question = ChoiceQuestion(
            explainer=f'{practice_label} ({trial_index}/{trials_count}) | {section_name} | {section_tag} | {section_group}',
            question=_(
                'Is the third sound the SAME or DIFFERENT as the first two sounds?'
            ),
            view='BUTTON_ARRAY',
            choices={
                'DEFINITELY_SAME': _('DEFINITELY SAME'),
                'PROBABLY_SAME': _('PROBABLY SAME'),
                'PROBABLY_DIFFERENT': _('PROBABLY DIFFERENT'),
                'DEFINITELY_DIFFERENT': _('DEFINITELY DIFFERENT'),
                'I_DONT_KNOW': _('I DON’T KNOW'),
            },
            key=key,
            result_id=prepare_result(
                key, session, section=section, expected_response=expected_response
            ),
            submits=True,
        )
        form = Form([question])
        playback = PlayButton([section], play_once=False)
        block_name = session.block.slug if session.block else "Musicality Battery Block"
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
        total_exp_variants = session.playlist.section_set.exclude(
            tag__contains='practice'
        )
        total_trials_count = total_exp_variants.values('group').distinct().count()
        return total_trials_count

    def validate_playlist(self, playlist: Playlist):

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

    def get_participant_group_variant(self, participant_id: int, round_number: int, groups: list[int], variants: list[int]) -> tuple[int, str]:
        ''' A participant is part of a group (1, 2, ...)'''
        ''' They will be presented with variants (A, B, C, D), registered as tags'''
        if participant_id < 0:
            raise ValueError(f"Participant id ({participant_id}) should be equal to or larger than 0")

        if round_number < 0:
            raise ValueError(f"Group number ({round_number}) should be equal to or larger than 0")

        if len(groups) < 1:
            raise ValueError(f"Groups ({groups}) should not be an empty list")

        if len(variants) < 1:
            raise ValueError(f"Variants ({variants}) should not be an empty list")

        variant_orders = list(itertools.permutations(variants))
        participant_index = participant_id % len(variant_orders)
        variant_index = round_number % len(variants)
        return variant_orders[participant_index][variant_index]
