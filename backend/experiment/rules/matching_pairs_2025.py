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
        playlist = self._get_least_played_playlist(session)
        player_sections = playlist.section_set.all()
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

    def _get_least_played_playlist(self, session) -> Playlist:
        """Return playlist with least plays by participant and overall"""

        playlist_count = session.block.playlists.count()

        # If no playlist is found, raise an error
        if playlist_count == 0:
            raise ValueError("No playlist found for block {}".format(session.block))

        # If there's only one playlist, assume Original playlist
        if playlist_count == 1:
            playlist = session.block.playlists.first()
            return playlist  # Early return

        # If there's more than one playlist, pick the one least played by the participant and least played overall
        playlists = session.block.playlists.all()

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
