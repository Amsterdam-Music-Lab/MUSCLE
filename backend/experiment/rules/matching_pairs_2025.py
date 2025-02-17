import random

from django.utils.translation import gettext_lazy as _
from django.db import models

from result.models import Result
from section.models import Section
from session.models import Session

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
            intro_explainer = self.get_intro_explainer()
            playlist = PlaylistAction(session.block.playlists.all())

            # TODO: Find a way to only show the intro explainer if the participant has not played this game before while avoiding the issue of an AudioContext not being available as the user hasn't interacted with the page yet
            # has_played_before = self._has_played_before(session)
            # actions = [intro_explainer, playlist] if not has_played_before else [playlist]
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

        # Finish session and show final view
        session.finish()
        session.save()

        return self._get_final_actions(session)

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
        random.seed(self.random_seed)
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
        condition_type, condition = self._select_least_played_condition_type_condition_pair(session)

        sections = self._select_least_played_sections(session, condition_type, condition)

        if not sections:
            raise ValueError(
                "No sections found for condition type {} and condition {}".format(condition_type, condition)
            )

        # if condition type not 'original', select the equivalent original sections
        if condition_type != "O":
            originals_sections = session.playlist.section_set.filter(tag__startswith="O")
            # Select equivalents by group number, e.g. a T2 with a group number of 1 will have an equivalent O2 with a group number of 1
            equivalents = originals_sections.filter(group__in=[section.group for section in sections])
            sections += equivalents
        else:
            sections += sections

        random.seed(self.random_seed)
        random.shuffle(sections)

        return sections

    def _select_least_played_condition_type_condition_pair(self, session: Session) -> tuple[str, str]:
        condition_type = self._select_least_played_condition_type(session)
        condition = self._select_least_played_condition(session, condition_type)

        return (condition_type, condition)

    def _select_least_played_condition_type(self, session: Session) -> str:
        least_played_participant_condition_types = self._select_least_played_session_condition_types(
            session, participant_specific=True
        )

        if len(least_played_participant_condition_types) == 1:
            return least_played_participant_condition_types[0]

        # If there are multiple condition types with the same lowest average play count per condition in the playlist for the current participant, select the one that has the lowest play count overall per condition in the playlist
        least_played_overall_condition_types = self._select_least_played_session_condition_types(
            session, participant_specific=False
        )

        if len(least_played_overall_condition_types) == 1:
            return least_played_overall_condition_types[0]

        # If there are still multiple condition types with the same lowest average play count overall per condition in the playlist, select one at random
        random.seed(self.random_seed)

        return random.choice(least_played_overall_condition_types)

    def _select_least_played_session_condition_types(self, session: Session, participant_specific=False) -> list[str]:
        playlist = session.playlist
        participant_sessions = (
            participant_specific and session.participant.session_set.all() or playlist.session_set.all()
        )
        all_tags = playlist.section_set.values_list("tag", flat=True).distinct()
        # Extract the first character as the 'condition_type'
        condition_types = {tag[0] for tag in all_tags}
        condition_type_counts = {ct: 0.0 for ct in condition_types}

        for psession in participant_sessions:
            played = psession.json_data.get("conditions", [])
            for ptype, _pcond in played:
                # Count how many distinct tags exist for this condition type
                total_for_ptype = sum(1 for t in all_tags if t[0] == ptype)
                if total_for_ptype:
                    condition_type_counts[ptype] += 1.0 / total_for_ptype

        min_avg = min(condition_type_counts.values())
        return [ct for ct, val in condition_type_counts.items() if val == min_avg]

    def _select_least_played_condition(self, session: Session, condition_type) -> str:
        least_played_participant_conditions = self._select_least_played_session_conditions(
            session, condition_type, participant_specific=True
        )

        if len(least_played_participant_conditions) == 1:
            return least_played_participant_conditions[0]

        least_played_overall_conditions = self._select_least_played_session_conditions(
            session, condition_type, participant_specific=False
        )

        if len(least_played_overall_conditions) == 1:
            return least_played_overall_conditions[0]

        random.seed(self.random_seed)

        return random.choice(least_played_overall_conditions)

    def _select_least_played_session_conditions(
        self, session: Session, condition_type, participant_specific=False
    ) -> list[str]:
        playlist = session.playlist
        participant_sessions = (
            participant_specific and session.participant.session_set.all() or playlist.session_set.all()
        )
        # All tags starting with condition_type
        relevant_tags = playlist.section_set.filter(tag__startswith=condition_type).values_list("tag", flat=True)
        # The second char is the condition number
        unique_conds = {t[1] for t in relevant_tags}
        cond_play_counts = {c: 0 for c in unique_conds}

        for psession in participant_sessions:
            played = psession.json_data.get("conditions", [])
            for ptype, pcond in played:
                if ptype != condition_type:
                    continue
                cond_play_counts[pcond] += 1

        min_count = min(cond_play_counts.values())
        return [c for c, val in cond_play_counts.items() if val == min_count]

    def _select_least_played_sections(self, session: Session, condition_type, condition) -> list[Section]:
        participant_result_sections = session.participant.result_set.filter(
            session__playlist=session.playlist
        ).values_list("section", flat=True)

        # Combine first and second char to form the tag
        combined_tag = f"{condition_type}{condition}"
        sections = session.playlist.section_set.filter(tag=combined_tag)

        # Count the number of times each section has been played by the participant
        section_play_counts = {section: 0 for section in sections}

        for participant_result_section in participant_result_sections:
            section_play_counts[participant_result_section] += 1

        # Return the num_pairs amount of sections that have been played the least amount of times
        least_played_sections = sorted(section_play_counts.keys(), key=lambda section: section_play_counts[section])[
            : self.num_pairs
        ]

        return least_played_sections

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
            outperformed=_("You outperformed {}% of the players!").format(percentile_rounded),
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
