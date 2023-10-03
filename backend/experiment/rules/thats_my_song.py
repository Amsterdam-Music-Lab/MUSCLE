from django.utils.translation import gettext_lazy as _
from django.conf import settings

from experiment.actions import Final, Score, Trial
from experiment.actions.form import Form, ChoiceQuestion
from experiment.questions.utils import copy_shuffle, question_by_key
from experiment.questions.musicgens import MUSICGENS_17_W_VARIANTS
from .hooked import Hooked
from result.utils import prepare_result

class ThatsMySong(Hooked):

    ID = 'THATS_MY_SONG'
    consent_file = None
    round_modifier = 1

    def __init__(self):
        self.questions = [
            question_by_key('dgf_generation'),
            question_by_key('dgf_gender_identity'),
            *copy_shuffle(MUSICGENS_17_W_VARIANTS)
        ]

    def feedback_info(self):
        return None

    def get_info_playlist(self, filename):
        """ function used by `manage.py compileplaylist` to compile a csv with metadata """
        parts = filename.split(' - ')
        time_info = int(parts[0])
        if time_info < 1970:
            decade = '1960s'
        elif time_info < 1980:
            decade = '1970s'
        elif time_info < 1990:
            decade = '1980s'
        elif time_info < 2000:
            decade = '1990s'
        else:
            decade = '2000s'
        try:
            int(parts[-1])
            form = parts[-2]
        except:
            form = parts[-1]
        return {
            'artist': parts[1],
            'song': parts[2],
            'tag': form,
            'group': decade
        }

    def next_round(self, session):	
        """Get action data for the next round"""
        json_data = session.load_json_data()

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if session.rounds_passed() == session.experiment.rounds + 1:

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            next_round_number = session.get_next_round()
            config = {'show_section': True, 'show_total_score': True}
            social_info = self.social_media_info(session.experiment, session.final_score)
            title = self.get_trial_title(session, next_round_number - 1 - self.round_modifier)
            return [
                Score(session,
                    config=config,
                    title=title
                ),
                Final(
                    session=session,
                    final_text=self.final_score_message(session) + " For more information about this experiment, visit the Vanderbilt University Medical Center Music Cognition Lab.",
                    rank=self.rank(session),
                    social=social_info,
                    show_profile_link=True,
                    button={'text': _('Play again'), 'link': '{}/{}{}'.format(settings.CORS_ORIGIN_WHITELIST[0], session.experiment.slug,
                        '?participant_id='+session.participant.participant_id_url if session.participant.participant_id_url else '')},
                    logo={'image': '/images/vumc_mcl_logo.png', 'link':'https://www.vumc.org/music-cognition-lab/welcome'}
                )
            ]

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        next_round_number = session.get_next_round()

        # Collect actions.
        actions = []
        if next_round_number == 1:
            # get list of trials for demographic questions (first 2 questions)
            questions = self.get_questionnaire(session, cutoff_index=2)
            if questions:
                for q in questions:
                    actions.append(q)

            question = ChoiceQuestion(
                key='playlist_decades',
                view='CHECKBOXES',
                question=_("Choose two or more decades of music"),
                choices={
                    '1960s': '1960s',
                    '1970s': '1970s',
                    '1980s': '1980s',
                    '1990s': '1990s',
                    '2000s': '2000s'
                },
                min_values = 2,
                result_id=prepare_result('playlist_decades', session=session)
            )
            actions.append(
                Trial(
                title=_("Playlist selection"),
                feedback_form=Form([question]))
            )

        # Go to SongSync
        elif next_round_number == 2:
            decades = session.result_set.first().given_response.split(',')
            self.plan_sections(session, {'group__in': decades})
            actions.extend(self.next_song_sync_action(session))
        else:
            # Create a score action.
            config = {'show_section': True, 'show_total_score': True}
            title = self.get_trial_title(session, next_round_number - 1 - self.round_modifier)
            actions.append(Score(session,
                config=config,
                title=title
            ))

            # Load the heard_before offset.
            plan = json_data.get('plan')
            heard_before_offset = len(plan['song_sync_sections']) + 2

            # SongSync rounds. Skip questions until Round 5.
            if next_round_number in range(3, 6):
                actions.extend(self.next_song_sync_action(session))
            if next_round_number in range(6, heard_before_offset):
                question = self.get_single_question(session, randomize=True)
                if question:
                    actions.append(question)
                actions.extend(self.next_song_sync_action(session))

            # HeardBefore rounds
            if next_round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(self.heard_before_explainer())
                actions.append(
                    self.next_heard_before_action(session))
            if next_round_number > heard_before_offset:
                question = self.get_single_question(session, randomize=True)
                if question:
                    actions.append(question)
                actions.append(
                    self.next_heard_before_action(session))

        return actions