import random
import json

from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.actions import Explainer, Final, Playlist, Step, Trial
from experiment.actions.playback import MatchingPairs
from result.utils import prepare_result

from section.models import Section


class MatchingPairsGame(Base):
    ID = "MATCHING_PAIRS"
    default_consent_file = "consent/consent_matching_pairs.html"
    num_pairs = 8
    show_animation = True
    score_feedback_display = "large-top"
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
    contact_email = "aml.tunetwins@gmail.com"
    random_seed = None

    def __init__(self):
        self.question_series = [
            {
                "name": "Demographics",
                "keys": [
                    "dgf_gender_identity",
                    "dgf_generation",
                    "dgf_musical_experience",
                    "dgf_country_of_origin",
                    "dgf_education_matching_pairs",
                ],
                "randomize": False,
            },
        ]

    def get_intro_explainer(self):
        return Explainer(
            instruction="",
            steps=[
                Step(
                    description=_(
                        'TuneTwins is a musical version of "Memory". It consists of 16 musical fragments. Your task is to listen and find the 8 matching pairs.'
                    )
                ),
                Step(
                    description=_(
                        "Some versions of the game are easy and you will have to listen for identical pairs. Some versions are more difficult and you will have to listen for similar pairs, one of which is distorted."
                    )
                ),
                Step(description=_("Click on another card to stop the current card from playing.")),
                Step(description=_("Finding a match removes the pair from the board.")),
                Step(description=_("Listen carefully to avoid mistakes and earn more points.")),
            ],
            step_numbers=True,
        )

    def next_round(self, session):
        if session.get_rounds_passed() < 1:
            intro_explainer = self.get_intro_explainer()
            playlist = Playlist(session.block.playlists.all())
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
            # final score saves the result from the cleared board into account
            score = Final(
                session,
                title="Score",
                final_text="Can you score higher than your friends and family? Share and let them try!",
                button={"text": "Play again", "link": self.get_play_again_url(session)},
                rank=self.rank(session, exclude_unfinished=False),
                feedback_info=self.feedback_info(),
            )
            return [score]

    def select_sections(self, session):
        json_data = session.json_data
        pairs = json_data.get("pairs", [])
        if len(pairs) < self.num_pairs:
            pairs = list(session.playlist.section_set.order_by().distinct("group").values_list("group", flat=True))
            random.seed(self.random_seed)
            random.shuffle(pairs)
        selected_pairs = pairs[: self.num_pairs]
        session.save_json_data({"pairs": pairs[self.num_pairs :]})
        originals = session.playlist.section_set.filter(group__in=selected_pairs, tag="Original")
        degradations = json_data.get("degradations")
        if not degradations:
            degradations = ["Original", "1stDegradation", "2ndDegradation"]
            random.seed(self.random_seed)
            random.shuffle(degradations)
        degradation_type = degradations.pop()
        session.save_json_data({"degradations": degradations})
        if degradation_type == "Original":
            player_sections = player_sections = list(originals) * 2
        else:
            degradations = session.playlist.section_set.filter(group__in=selected_pairs, tag=degradation_type)
            player_sections = list(originals) + list(degradations)
        return player_sections

    def get_matching_pairs_trial(self, session):
        player_sections = self.select_sections(session)
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

    def calculate_score(self, result, data):
        """not used in this experiment"""
        pass

    def calculate_intermediate_score(self, session, result):
        """will be called every time two cards have been turned"""
        result_data = json.loads(result)
        first_card = result_data["first_card"]
        first_section = Section.objects.get(pk=first_card["id"])
        first_card["filename"] = str(first_section.filename)
        second_card = result_data["second_card"]
        second_section = Section.objects.get(pk=second_card["id"])
        second_card["filename"] = str(second_section.filename)
        if first_section.group == second_section.group:
            if "seen" in second_card:
                score = 20
                given_response = "match"
            else:
                score = 10
                given_response = "lucky match"
        else:
            if "seen" in second_card:
                score = -10
                given_response = "misremembered"
            else:
                score = 0
                given_response = "no match"
        prepare_result("move", session, json_data=result_data, score=score, given_response=given_response)
        return score
