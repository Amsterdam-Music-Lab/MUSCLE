from django.db.models import Avg
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.actions import Explainer, Final, HTML, Redirect, Step, Trial
from experiment.actions.form import BooleanQuestion, ChoiceQuestion, Form, LikertQuestionIcon
from experiment.actions.playback import Autoplay
from experiment.actions.styles import ColorScheme

from result.utils import prepare_result
from result.models import Result

from section.models import Section
from session.models import Session

from .base import BaseRules
from .huang_2022 import get_test_playback


class MusicalPreferences(BaseRules):
    """This rules file presents repeated trials with a combined form:
    participants are asked to state how much they like the song, and whether they know the song
    after 21 and 42 rounds, participants see summaries of their choices,
    and at the final round, participants see other participants' preferred songs
    """

    ID = "MUSICAL_PREFERENCES"
    default_consent_file = "consent/consent_musical_preferences.html"
    preference_offset = 21  # after this many rounds rounds, show information with the participant's preferences
    knowledge_offset = 42  # after this many rounds, show additionally how many songs the participant knows
    contact_email = "musicexp_china@163.com"
    counted_result_keys = ["like_song"]

    know_score = {"yes": 2, "unsure": 1, "no": 0}

    def __init__(self):
        self.question_series = [
            {
                "name": "Question series Musical Preferences",
                "keys": [
                    "msi_38_listen_music",
                    "dgf_genre_preference_zh",
                    "dgf_gender_identity_zh",
                    "dgf_age",
                    "dgf_region_of_origin",
                    "dgf_region_of_residence",
                ],
                "randomize": False,
            },
        ]

    def get_intro_explainer(self):
        return Explainer(
            instruction=_("Welcome to the Musical Preferences experiment!"),
            steps=[Step(_("Please start by checking your connection quality."))],
            button_label=_("OK"),
        )

    def next_round(self, session: Session):
        round_number = session.get_rounds_passed(self.counted_result_keys)
        actions = []
        if round_number == 0:
            last_result = session.last_result()
            if last_result:
                if last_result.score == 1:
                    question_trials = self.get_open_questions(session)
                    if question_trials:
                        n_questions = len(question_trials)
                        explainer = Explainer(
                            instruction=_("Questionnaire"),
                            steps=[
                                Step(
                                    _(
                                        "To understand your musical preferences, we have {} questions for you before the experiment \
                                        begins. The first two questions are about your music listening experience, while the other \
                                        four questions are demographic questions. It will take 2-3 minutes."
                                    ).format(n_questions)
                                ),
                                Step(_("Have fun!")),
                            ],
                            button_label=_("Let's go!"),
                        )
                        return [explainer, *question_trials]
                    else:
                        explainer = Explainer(
                            instruction=_("How to play"),
                            steps=[
                                Step(_("You will hear 64 music clips and have to answer two questions for each clip.")),
                                Step(_("It will take 20-30 minutes to complete the whole experiment.")),
                                Step(_("Either wear headphones or use your device's speakers.")),
                                Step(_("Your final results will be displayed at the end.")),
                                Step(_("Have fun!")),
                            ],
                            button_label=_("Start"),
                        )
                        actions = [explainer]
                else:
                    if last_result.question_key == "audio_check1":
                        playback = get_test_playback()
                        html = HTML(body=render_to_string("html/huang_2022/audio_check.html"))
                        form = Form(
                            form=[
                                BooleanQuestion(
                                    key="audio_check2",
                                    choices={"no": _("Quit"), "yes": _("Next")},
                                    result_id=prepare_result(
                                        "audio_check2", session, scoring_rule="BOOLEAN"
                                    ),
                                    submits=True,
                                    style=[ColorScheme.BOOLEAN_NEGATIVE_FIRST],
                                )
                            ]
                        )
                        return Trial(
                            playback=playback,
                            html=html,
                            feedback_form=form,
                            config={"response_time": 15},
                            title=_("Tech check"),
                        )
                    else:
                        # participant had persistent audio problems, finish session and redirect
                        session.finish()
                        session.save()
                        return Redirect(settings.HOMEPAGE)
            else:
                playback = get_test_playback()
                html = HTML(body="<h4>{}</h4>".format(_("Do you hear the music?")))
                form = Form(
                    form=[
                        BooleanQuestion(
                            key="audio_check1",
                            choices={"no": _("No"), "yes": _("Yes")},
                            result_id=prepare_result(
                                "audio_check1", session, scoring_rule="BOOLEAN"
                            ),
                            submits=True,
                            style=[ColorScheme.BOOLEAN_NEGATIVE_FIRST],
                        )
                    ]
                )
                return [
                    self.get_intro_explainer(),
                    Trial(
                        playback=playback,
                        feedback_form=form,
                        html=html,
                        config={"response_time": 15},
                        title=_("Audio check"),
                    ),
                ]
        if round_number == self.preference_offset:
            like_results = session.result_set.filter(question_key="like_song")
            feedback = Trial(
                html=HTML(
                    body=render_to_string(
                        "html/musical_preferences/feedback.html",
                        {
                            "unlocked": _("Love unlocked"),
                            "n_songs": round_number,
                            "top_participant": self.get_preferred_songs(like_results, 3),
                        },
                    )
                )
            )
            actions = [feedback]
        elif round_number == self.knowledge_offset:
            like_results = session.result_set.filter(question_key="like_song")
            known_songs = session.result_set.filter(question_key="know_song", score=2).count()
            feedback = Trial(
                html=HTML(
                    body=render_to_string(
                        "html/musical_preferences/feedback.html",
                        {
                            "unlocked": _("Knowledge unlocked"),
                            "n_songs": round_number - 1,
                            "top_participant": self.get_preferred_songs(like_results, 3),
                            "n_known_songs": known_songs,
                        },
                    )
                )
            )
            actions = [feedback]
        elif round_number == session.block.rounds:
            like_results = session.result_set.filter(question_key="like_song")
            known_songs = session.result_set.filter(question_key="know_song", score=2).count()
            all_results = Result.objects.filter(question_key="like_song", section_id__isnull=False)
            top_participant = self.get_preferred_songs(like_results, 3)
            top_all = self.get_preferred_songs(all_results, 3)
            feedback = Trial(
                html=HTML(
                    body=render_to_string(
                        "html/musical_preferences/feedback.html",
                        {
                            "unlocked": _("Connection unlocked"),
                            "n_songs": round_number,
                            "top_participant": top_participant,
                            "n_known_songs": known_songs,
                            "top_all": top_all,
                        },
                    )
                )
            )
            session.finish()
            session.save()
            return [feedback, self.get_final_view(session, top_participant, known_songs, round_number, top_all)]
        section = session.playlist.get_section(song_ids=session.get_unused_song_ids())
        like_key = "like_song"
        likert = LikertQuestionIcon(
            question=_("2. How much do you like this song?"),
            key=like_key,
            result_id=prepare_result(like_key, session, section=section, scoring_rule="LIKERT"),
        )
        know_key = "know_song"
        know = ChoiceQuestion(
            question=_("1. Do you know this song?"),
            key=know_key,
            view="BUTTON_ARRAY",
            choices={"yes": "fa-check", "unsure": "fa-question", "no": "fa-xmark"},
            result_id=prepare_result(know_key, session, section=section),
            style=[ColorScheme.BOOLEAN],
        )
        playback = Autoplay([section], show_animation=True)
        form = Form([know, likert])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_("Song %(round)s/%(total)s") % {"round": round_number + 1, "total": session.block.rounds},
            config={
                "response_time": section.duration + 0.1,
            },
        )
        actions.append(view)
        return actions

    def calculate_score(self, result, data):
        if data.get("key") == "know_song":
            return self.know_score.get(data.get("value"))
        else:
            return super().calculate_score(result, data)

    def get_final_view(self, session, top_participant, known_songs, n_songs, top_all):
        # finalize block
        view = Final(
            session,
            title=_("End"),
            final_text=_(
                "Thank you for your participation and contribution to science!"
            ),
            feedback_info=self.feedback_info(),
        )
        return view

    def feedback_info(self):
        info = super().feedback_info()
        info["header"] = _("Any remarks or questions (optional):")
        return info

    def get_preferred_songs(self, result_set, n=5):
        top_results = result_set.annotate(avg_score=Avg("score")).order_by("score")[:n]
        out_list = []
        for result in top_results.all():
            section = Section.objects.get(pk=result.section.id)
            out_list.append(
                {"artist": section.artist_name(), "name": section.song_name()}
            )
        return out_list
