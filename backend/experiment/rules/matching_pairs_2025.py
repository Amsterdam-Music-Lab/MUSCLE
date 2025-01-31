import random

from django.utils.translation import gettext_lazy as _
from django.db import models

from section.models import Playlist

from experiment.actions import Explainer, Final, Playlist as PlaylistAction, Trial
from experiment.actions.playback import MatchingPairs
from .matching_pairs import MatchingPairsGame


class MatchingPairs2025(MatchingPairsGame):
    """This is the working version of the Matching Pairs game for the 2025 Tunetwins experiment. The difference between this version and the original Matching Pairs game is that this version has some additional tutorial messages. These messages are intended to help the user understand the game. The tutorial messages are as follows:
    - no_match: This was not a match, so you get 0 points. Please try again to see if you can find a matching pair.
    - lucky_match: You got a matching pair, but you didn't hear both cards before. This is considered a lucky match. You get 10 points.
    - memory_match: You got a matching pair. You get 20 points.
    - misremembered: You thought you found a matching pair, but you didn't. This is considered a misremembered pair. You lose 10 points.

    The tutorial messages are displayed to the user in an overlay on the game screen.
    """

    ID = "MATCHING_PAIRS_2025"
    tutorial = {
        "no_match": _(
            "This was not a match, so you get 0 points. Please try again to see if you can find a matching pair."
        ),
        "lucky_match": _(
            "You got a matching pair, but you didn't hear both cards before. This is considered a lucky match. You get 10 points."
        ),
        "memory_match": _("You got a matching pair. You get 20 points."),
        "misremembered": _(
            "You thought you found a matching pair, but you didn't. This is considered a misremembered pair. You lose 10 points."
        ),
    }

    def next_round(self, session):
        if session.get_rounds_passed() < 1:
            intro_explainer = self.get_intro_explainer()
            playlist = PlaylistAction(session.block.playlists.all())
            actions = [intro_explainer, playlist]
            questions = self.get_open_questions(session)
            if questions:
                intro_questions = Explainer(
                    instruction=_(
                        "Before starting the game, we would like to ask you %i demographic questions."
                        % (len(questions))
                    ),
                    steps=[],
                )
                actions.append(intro_questions)
                actions.extend(questions)
            trial = self.get_matching_pairs_trial(session)
            actions.append(trial)
            return actions
        else:
            feedback_info = self.feedback_info()
            score = Final(
                session,
                title="Score",
                final_text=self._final_text(session),
                button={"text": "Play again", "link": self.get_play_again_url(session)},
                rank=self.rank(session, exclude_unfinished=False),
                feedback_info=feedback_info,
                percentile=session.percentile_rank(exclude_unfinished=False),
            )
            return [score]

    def get_matching_pairs_trial(self, session):
        player_sections = self._select_sections(session)
        random.seed(self.random_seed)
        random.shuffle(player_sections)

        playback = MatchingPairs(
            sections=player_sections,
            stop_audio_after=5,
            show_animation=self.show_animation,
            score_feedback_display=self.score_feedback_display,
            tutorial=self.tutorial,
        )
        trial = Trial(title="Tune twins", playback=playback, feedback_form=None, config={"show_continue_button": False})

        return trial

    def _select_sections(self, session):
        condition_type = self._select_least_played_condition_type(session)

        raise NotImplementedError

    def _select_least_played_condition_type(self, session) -> str:
        least_played_participant_condition_types = self._select_least_played_participant_condition_types(session)

        if len(least_played_participant_condition_types) == 1:
            return least_played_participant_condition_types[0]

        # If there are multiple condition types with the same lowest average play count per condition in the playlist for the current participant, select the one that has the lowest play count overall per condition in the playlist
        least_played_overall_condition_type = self._select_least_played_overall_condition_type(session)

        if len(least_played_overall_condition_type) == 1:
            return least_played_overall_condition_type[0]

        # If there are still multiple condition types with the same lowest average play count overall per condition in the playlist, select one at random
        random.seed(self.random_seed)

        return random.choice(least_played_overall_condition_type)

    def _select_least_played_participant_condition_types(self, session) -> list[str]:
        """Select the condition type with the lowest average play count per condition in the playlist for the current participant"""

        playlist = session.playlist
        participant_results = session.participant.result_set.filter(section__playlist=playlist)

        # Count the number of results per section and then group them by the section's tag
        tag_play_counts = (
            participant_results.values("section__tag")
            .annotate(play_count=models.Count("section"))
            .order_by("section__tag")
        )

        # Now, we need to get the average play count per condition type (tag) by dividing the tag play count by the number of conditions (group) in the playlist.
        condition_type_avg_play_counts = {}
        for tag_play_count in tag_play_counts:
            tag = tag_play_count["section__tag"]
            group_count = playlist.section_set.filter(tag=tag).values("group").distinct().count()
            avg_play_count = tag_play_count["play_count"] / group_count
            condition_type_avg_play_counts[tag] = avg_play_count

        min_avg_play_count = min(condition_type_avg_play_counts.values())

        # Get the condition types with the same lowest average play count
        least_played_participant_condition_types = [
            condition_type
            for condition_type, avg_play_count in condition_type_avg_play_counts.items()
            if avg_play_count == min_avg_play_count
        ]

        return least_played_participant_condition_types


        # As I don't have information about the number of plays, I'll pick a random playlist
        # TODO: Implement a way to get the least played playlist
        random_index = random.randint(0, playlist_count - 1)

        playlist = playlists[random_index]

        return playlist

    def _final_text(self, session):
        total_sessions = session.participant.session_set.count()
        total_score = session.participant.session_set.aggregate(total_score=models.Sum("final_score"))["total_score"]
        average_score = total_score / total_sessions if total_sessions > 0 else 0
        highest_score = session.participant.session_set.aggregate(highest_score=models.Max("final_score"))[
            "highest_score"
        ]
        percentile = session.percentile_rank(exclude_unfinished=False)
        percentile_rounded = round(percentile)

        final_text = """
        <p>{outperformed}</p>
        
        <table>
            <tr><td>{this_game}</td><td>{game_score}</td></tr>
            <tr><td>{personal_best}</td><td>{best_score}</td></tr>
            <tr><td>{average}</td><td>{avg_score}</td></tr>
        </table>
        """.format(
            outperformed=_("You outperformed {}% of the players!").format(percentile_rounded),
            this_game=_("This game"),
            game_score=session.final_score,
            personal_best=_("Personal Best"),
            best_score=highest_score,
            average=_("Average score"),
            avg_score=int(average_score),
        )

        return final_text
