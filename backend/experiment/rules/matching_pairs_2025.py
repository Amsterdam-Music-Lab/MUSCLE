from os.path import split
import random

from django.utils.translation import gettext_lazy as _
from django.db import models

from result.models import Result
from section.models import Section, Song
from session.models import Session

from experiment.actions import Explainer, Final, Trial
from experiment.actions.playback import MatchingPairs
from .matching_pairs import MatchingPairsGame

POSSIBLE_CONDITIONS = [
    ["O", "0"],
    ["TD", "1"],
    ["TD", "2"],
    ["TD", "3"],
    ["TD", "4"],
    ["TD", "5"],
    ["SD", "1"],
    ["SD", "2"],
    ["SD", "3"],
    ["SD", "4"],
    ["SD", "5"],
]

class MatchingPairs2025(MatchingPairsGame):
    """This is the working version of the Matching Pairs game for the 2025 Tunetwins experiment.
    The difference between this version and the original Matching Pairs game is that this version has some additional tutorial messages.
    These messages are intended to help the user understand the game.
    The tutorial messages are displayed to the user in an overlay on the game screen.
    There is also additional logic to balance condition types (degradations vs. original) and difficulty levels.
    """

    ID = "MATCHING_PAIRS_2025"
    num_pairs = 8
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

    def next_round(self, session: Session):
        if session.get_rounds_passed() < 1:
            actions = (
                [self.get_intro_explainer()]
                if not self._has_played_before(session)
                else []
            )

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
            if not actions:
                actions.append(self.get_short_explainer())
            trial = self.get_matching_pairs_trial(session)
            actions.append(trial)
            return actions

        # Finish session and show final view
        session.finish()
        session.save()

        return self._get_final_actions(session)

    def get_short_explainer(self):
        return Explainer("Click to start!", steps=[])

    def _get_final_actions(self, session: Session):
        accumulated_score = session.participant.session_set.aggregate(total_score=models.Sum("final_score"))[
            "total_score"
        ]
        score = Final(
            session,
            title="Score",
            total_score=accumulated_score,
            final_text=self._final_text(session),
            button={"text": "Next game", "link": self.get_experiment_url(session)},
            rank=self.rank(session, exclude_unfinished=False),
            percentile=session.percentile_rank(exclude_unfinished=False),
        )

        return [score]

    def get_matching_pairs_trial(self, session: Session):
        player_sections = self._select_sections(session)
        random.shuffle(player_sections)

        # Only show tutorial if participant has never played this game before
        has_played_before = self._has_played_before(session)
        tutorial = self.tutorial if not has_played_before else None

        playback = MatchingPairs(
            sections=player_sections,
            stop_audio_after=5,
            show_animation=self.show_animation,
            score_feedback_display=self.score_feedback_display,
            tutorial=tutorial,
        )
        trial = Trial(title="Tune twins", playback=playback, feedback_form=None, config={"show_continue_button": False})

        return trial

    def _has_played_before(self, session: Session) -> bool:
        experiment = session.block.phase.experiment
        previous_games = Session.objects.filter(
            block__phase__experiment=experiment, participant=session.participant, block__rules=self.ID
        )
        previous_games_results = Result.objects.filter(session__in=previous_games)

        return previous_games_results.exists()

    def _select_sections(self, session: Session) -> list[Section]:
        condition, difficulty = self._select_least_played_condition_difficulty_pair(
            session
        )

        songs = self._select_least_played_songs(session)

        sections = list(
            session.playlist.section_set.filter(
                song__pk__in=songs, group=condition, tag=difficulty
            )
        )
        if not len(sections) == self.num_pairs:
            raise ValueError(
                "Not enough sections found for condition {} and difficulty {}".format(
                    condition, difficulty
                )
            )

        # if condition type not 'original', select the equivalent original sections
        if condition != "O":
            equivalents = list(
                session.playlist.section_set.filter(group="O", song__in=songs)
            )
            sections += equivalents
        else:
            sections += sections

        random.shuffle(sections)

        return sections

    def evaluate_sections_equal(
        self, first_section: Section, second_section: Section
    ) -> bool:
        return first_section.song == second_section.song

    def _select_least_played_condition_difficulty_pair(
        self, session: Session
    ) -> tuple[str, str]:
        condition_results = session.participant.result_set.filter(
            question_key__startswith='condition'
        )
        if len(condition_results) == 11:
            # all conditions have been played, return the least played
            least_played = condition_results.order_by('score').first()
            least_played.score += 1
            least_played.save()
            cond, difficulty = least_played.question_key.split('_')[1:]
            return cond, difficulty
        elif len(condition_results) == 0:
            cond, difficulty = random.choice(POSSIBLE_CONDITIONS)
        else:
            played_conditions = [
                cond.split('_')[1:]
                for cond in condition_results.values_list('question_key', flat=True)
            ]
            unplayed_conditions = [
                cond for cond in POSSIBLE_CONDITIONS if cond not in played_conditions
            ]
            cond, difficulty = random.choice(unplayed_conditions)
        question_key = f"condition_{cond}_{difficulty}"
        Result.objects.create(
            participant=session.participant, question_key=question_key, score=1
        )
        return cond, difficulty

    def _select_least_played_songs(self, session: Session) -> list[int]:
        songs = list(
            session.playlist.section_set.values_list('song', flat=True).distinct().all()
        )
        random.shuffle(songs)
        participant_results = session.participant.result_set.filter(
            question_key__startswith='song'
        ).order_by('score')
        if not participant_results.count():
            selected_songs = songs[: self.num_pairs]
        else:
            participant_songs = [
                int(result.question_key.split('_')[1]) for result in participant_results
            ]
            unplayed_songs = [song for song in songs if song not in participant_songs]
            if len(unplayed_songs) >= self.num_pairs:
                selected_songs = unplayed_songs[: self.num_pairs]
            else:
                selected_songs = [
                    *unplayed_songs,
                    *participant_songs,
                ][: self.num_pairs]
        for song in selected_songs:
            result, created = Result.objects.get_or_create(
                participant=session.participant, question_key=f"song_{song}"
            )
            if created:
                result.score = 1
            else:
                result.score += 1
            result.save()
        return selected_songs

    def _final_text(self, session: Session):
        total_sessions = session.participant.session_set.count()
        total_score = session.participant.session_set.aggregate(total_score=models.Sum("final_score"))["total_score"]
        average_score = total_score / total_sessions if total_sessions > 0 else 0
        highest_score = session.participant.session_set.aggregate(highest_score=models.Max("final_score"))[
            "highest_score"
        ]
        game_score = int(session.total_score())
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
            outperformed=_("You outperformed {}% of the players!").format(
                percentile_rounded
            ),
            this_game=_("This game"),
            game_score=game_score,
            personal_best=_("Personal Best"),
            # personal best might not be updated yet in the database
            best_score=max(int(highest_score), game_score),
            average=_("Average score"),
            avg_score=int(average_score),
        )

        return final_text

    def _get_percentile_rank(self):
        # Custom percentile rank calculation
        raise NotImplementedError

    def get_info_playlist(self, section_path: str):
        path, filename = split(section_path)
        filename_components = filename.split('_')
        output = {'artist': filename_components[1], 'song': filename_components[2]}
        head, tail = split(path)
        if tail == 'O':
            output.update({'group': 'O', 'tag': 0})
        else:
            top_directory = split(head)[1]
            output.update({'group': top_directory, 'tag': tail[1]})
        return output
