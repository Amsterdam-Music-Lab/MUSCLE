from django.utils.translation import gettext_lazy as _
from django.conf import settings

from experiment.actions import Final, Trial
from experiment.actions.form import Form, ChoiceQuestion
from experiment.questions.utils import copy_shuffle, question_by_key
from experiment.questions.musicgens import MUSICGENS_17_W_VARIANTS
from .hooked import Hooked
from result.utils import prepare_result

class ThatsMySong(Hooked):

    ID = 'THATS_MY_SONG'
    consent_file = None
    relevant_keys = ['recognize', 'heard_before', 'playlist_decades']
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
    
    def first_round(self, experiment):
        actions = super().first_round(experiment)
        # remove consent
        del actions[1]
        return actions

    def next_round(self, session):	
        """Get action data for the next round"""
        json_data = session.load_json_data()
        round_number = self.get_current_round(session)
        
        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if round_number == session.experiment.rounds:

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            social_info = self.social_media_info(session.experiment, session.final_score)
            return [
                self.get_score(session, round_number),
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

        # Initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.

        # Collect actions.
        actions = []
        if round_number == 0:
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
        elif round_number == 1:
            decades = session.result_set.first().given_response.split(',')
            self.plan_sections(session, {'group__in': decades})
            actions.extend(self.next_song_sync_action(session))
        else:
            # Create a score action.
            actions.append(self.get_score(session, round_number - self.round_modifier))

            # Load the heard_before offset.
            plan = json_data.get('plan')
            heard_before_offset = len(plan['song_sync_sections'])

            # SongSync rounds. Skip questions until Round 5.
            if round_number in range(2, 5):
                actions.extend(self.next_song_sync_action(session))
            if round_number in range(5, heard_before_offset):
                question = self.get_single_question(session, randomize=True)
                if question:
                    actions.append(question)
                actions.extend(self.next_song_sync_action(session))

            # HeardBefore rounds
            if round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(self.heard_before_explainer())
                actions.append(
                    self.next_heard_before_action(session))
            if round_number > heard_before_offset:
                actions.append(
                    self.next_heard_before_action(session))
                question = self.get_single_question(session, randomize=True)
                if question:
                    actions.append(question)

        return actions