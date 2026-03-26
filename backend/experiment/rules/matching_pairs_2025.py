from os.path import split
import random

from django.db.models import Avg
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from result.models import Result
from section.models import Section
from session.models import Session

from experiment.actions import Explainer, Final, Step, Trial
from experiment.actions.playback import MatchingPairs
from experiment.actions.types import FeedbackInfo
from .matching_pairs import MatchingPairsGame


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
    cutoff = 30
    progress_info = [
        _("Great job finishing Game 1 - your first star is within reach!"),
        _("Just 1 more game to earn your first star!"),
        _("First star unlocked - keep going for the second!"),
        _("Keep up the momentum! - your next star is coming up!"),
        _("Just 1 more game to earn your second star!"),
        _("Second star unlocked - you’re halfway there!"),
        _("Keep it up - your third star is waiting!"),
        _("Game 8 complete - the third star is almost yours!"),
        _("Third star unlocked  - final sprint!"),
        _("Just 2 games left to complete the challenge!"),
        _("Just 1 game to unlock your title!"),
        _("All stars collected — Congratulations, you cleared all levels!"),
    ]

    def feedback_info(self) -> FeedbackInfo:
        feedback_body = render_to_string(
            "feedback/user_feedback.html", {"email": self.contact_email}
        )
        return {
            # Header above the feedback form
            "header": _("Do you have any remarks or questions?"),
            # Button text
            "button": _("Submit"),
            # Body of the feedback form, can be HTML. Shown under the button
            "contact_body": feedback_body,
            # Thank you message after submitting feedback
            "thank_you": _("We appreciate your feedback!"),
            # Show a floating button on the right side of the screen to open the feedback form
            "show_float_button": True,
        }

    def next_round(self, session: Session):
        if session.get_rounds_passed() < 1:
            actions = []

            questions = self.get_profile_question_trials(session, None)
            if questions:
                intro_questions = Explainer(
                    instruction=_(
                        "Before starting the game, we would like to ask you %(n_questions)i demographic questions."
                    )
                    % {'n_questions': len(questions)},
                    steps=[],
                )
                actions.append(intro_questions)
                actions.extend(questions)
            if not self._has_played_before(session):
                actions.append(self.get_intro_explainer())
            if not actions:
                actions.append(
                    self.get_short_explainer()
                )  # short explainer necessary because preload won't start otherwise
            trial = self.get_matching_pairs_trial(session)
            actions.append(trial)
            return actions

        # Finish session and show final view
        session.finish()
        session.save()

        return self._get_final_actions(session)

    def get_short_explainer(self):
        return Explainer(_("Click to start!"), steps=[])

    def _get_final_actions(self, session: Session):
        played_sessions = session.participant.session_set.filter(
            finished_at__isnull=False,
            block__in=session.block.phase.blocks.all(),
        )
        n_sessions = played_sessions.count()
        if n_sessions % 12 == 0:
            # final board, percentile is based on participant's accumulative score
            percentile = session.participant.percentile_rank_accumulative_score()
            display_percentile = max(self.cutoff, percentile)
            mean = played_sessions.aggregate(Avg("final_score"))["final_score__avg"]
            extra_info = _(
                "Your music memory mean score is %(mean)d. The average score was 32.63 for Dutch participants and 37.20 for U.S. participants. Your score was higher than %(percentile)d%% of participants."
            ) % {"percentile": display_percentile, "mean": mean}
            if percentile > 75:
                title = {
                    "header": _("Exceptional"),
                    "body": _("Sharp Recognition"),
                }
                final_text = _("You have excellent music perception ability.")
            elif percentile > 50:
                title = {"header": _("Advanced"), "body": _("Clear Recognition")}
                final_text = _("Your performance in music perception is above average.")
            elif percentile >= 40:
                title = {"header": _("Average"), "body": _("Stable Performance")}
                final_text = _("Your perception ability is around the average level.")
            else:
                title = {"header": _("Developing"), "body": _("Ongoing Exploration")}
                final_text = _(
                    "Your music perception ability still has room for further development."
                )
        else:
            percentile = session.percentile_rank()
            display_percentile = max(percentile, self.cutoff)
            final_text = _(
                "Congrats! You did better than %(percentile)d%% of players at this level"
            ) % {"percentile": display_percentile}
            extra_info = None
            title = {}
        score = Final(
            session,
            title=title,
            total_score=session.final_score,
            final_text=final_text,
            extra_info=extra_info,
            progress_text=self.progress_info[(n_sessions - 1) % 12],
            button={"text": "Keep playing!", "link": self.get_experiment_url(session)},
            percentile=percentile,
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
        cond, diff = self._select_least_played_condition_difficulty_pair(session)

        songs = self._select_least_played_songs(session)

        sections = list(
            session.playlist.section_set.filter(
                song__pk__in=songs, group=cond, tag=diff
            )
        )
        if not len(sections) == self.num_pairs:
            raise ValueError(
                "Not enough sections found for condition {} and difficulty {}".format(
                    cond, diff
                )
            )

        # if condition type not 'original', select the equivalent original sections
        if cond != "O":
            equivalents = list(
                session.playlist.section_set.filter(group="O", song__in=songs)
            )
            sections += equivalents
        else:
            sections += sections

        random.shuffle(sections)

        return sections

    def _get_possible_conditions(self, session):
        conditions = list(set(session.playlist.section_set.values_list('group', 'tag')))
        return conditions

    def get_intro_explainer(self):
        return Explainer(
            instruction="",
            steps=[
                Step(
                    description=_(
                        'You get a board with 16 musical cards. **Pick a card,** and listen to it carefully...'
                    )
                ),
                Step(
                    description=_("Then try to **find a second card that matches it.**")
                ),
                Step(
                    description=_(
                        "**Find the 8 matching pairs** to clear the board and score points:"
                    )
                ),
                Step(
                    description=_(
                        "**+20 points:** Matched first card with one you’ve heard before — memory wins!"
                    )
                ),
                Step(
                    description=_(
                        "**-10 points:** Chose a wrong second card that’s heard before? Oops — penalty..."
                    )
                ),
                Step(
                    description=_(
                        "Some cards sound **distorted** on purpose. Stay sharp!"
                    )
                ),
            ],
            step_numbers=True,
        )

    def evaluate_sections_equal(
        self, first_section: Section, second_section: Section
    ) -> bool:
        return first_section.song == second_section.song

    def _select_least_played_condition_difficulty_pair(
        self, session: Session
    ) -> tuple[str, str]:
        possible_conditions = self._get_possible_conditions(session)
        condition_results = session.participant.result_set.filter(
            question_key='condition'
        ).order_by('score')
        if len(condition_results) == 11:
            # all conditions have been played, return the least played
            least_played = condition_results.first()
            least_played.score += 1
            least_played.save()
            cond, difficulty = least_played.given_response.split('_')
            session.save_json_data({'condition': cond, 'difficulty': difficulty})
            return cond, difficulty
        elif len(condition_results) == 0:
            cond, difficulty = random.choice(possible_conditions)
        else:
            played_conditions = [
                tuple(cond.split('_'))
                for cond in condition_results.values_list('given_response', flat=True)
            ]
            unplayed_conditions = [
                cond for cond in possible_conditions if cond not in played_conditions
            ]
            cond, difficulty = random.choice(unplayed_conditions)
        condition = f"{cond}_{difficulty}"
        Result.objects.create(
            participant=session.participant,
            question_key="condition",
            given_response=condition,
            score=1,
        )
        session.save_json_data({'condition': cond, 'difficulty': difficulty})
        return cond, difficulty

    def _select_least_played_songs(self, session: Session) -> list[int]:
        songs = list(
            session.playlist.section_set.values_list('song', flat=True).distinct().all()
        )
        random.shuffle(songs)
        participant_results = session.participant.result_set.filter(
            question_key='song', given_response__in=songs
        ).order_by('score')
        if not participant_results.count():
            selected_songs = songs[: self.num_pairs]
        else:
            participant_songs = [
                int(result.given_response) for result in participant_results
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
                participant=session.participant,
                question_key="song",
                given_response=song,
            )
            if created:
                result.score = 1
            else:
                result.score += 1
            result.save()
        return selected_songs

    def _get_percentile_rank(self, session):
        """
        Returns:
            Percentile rank of all sessions with same difficulty, based on `final_score`
        """
        blocks = session.block.phase.experiment.associated_blocks()
        condition = session.json_data.get('condition')
        difficulty = session.json_data.get('difficulty')
        filter_conditions = {
            'block__in': blocks,
            'json_data__contains': {
                'condition': condition,
                'difficulty': difficulty,
            },
        }
        return session.percentile_rank(filter_conditions)

    def get_info_playlist(self, section_path: str):
        path, filename = split(section_path)
        filename_components = filename.split('_')
        output = {'artist': filename_components[1], 'song': filename_components[2]}
        head, tail = split(path)
        if tail == 'O':
            output.update({'group': 'O', 'tag': 0})
        else:
            top_directory = split(head)[1]
            # stage 1
            # output.update({'group': top_directory, 'tag': tail[1]})
            # stage 2
            output.update({'group': top_directory, 'tag': tail})
        return output
