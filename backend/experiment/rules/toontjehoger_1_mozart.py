import logging
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from random import randint
from experiment.models import Section
from .views import Trial, Explainer, Step, Score, Final, StartSession, Playlist, Info, HTML
from .views.form import ButtonArrayQuestion, Form
from .views.playback import Playback
from .base import Base
from os.path import join
from .util.actions import combine_actions

logger = logging.getLogger(__name__)


class ToontjeHoger1Mozart(Base):
    ID = 'TOONTJE_HOGER_1_MOZART'
    TITLE = _("Toontje Hoger")
    SCORE_CORRECT = 50
    SCORE_WRONG = 0
    LISTEN_DURATION = 5  # 20

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Uitleg",
            steps=[
                Step(_("Je krijgt zo eerst een muziekfragment van 20 seconden te horen.")),
                Step(
                    _("Hierna verschijnt een kort spelletje.")),
            ],
            button_label=_("Start")
        ).action(step_numbers=True)

        # 2. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 3. Start session.
        start_session = StartSession.action()

        return [
            explainer,
            playlist,
            start_session
        ]

    @classmethod
    def next_round(cls, session, request_session=None):
        """Get action data for the next round"""
        rounds_passed = session.rounds_passed()

        # Round 1
        if rounds_passed == 0:
            round = cls.get_image_trial(session,
                                        section_group='1',
                                        image_url="/images/experiments/toontjehoger/mozart-effect1.webp",
                                        question='Welke vorm ontstaat er na het afknippen van de hoekjes?',
                                        expected_response='B'
                                        )
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return round

        # Round 2
        if rounds_passed == 1:
            score = cls.get_score(session)
            round = cls.get_image_trial(session,
                                        section_group='2',
                                        image_url="/images/experiments/toontjehoger/mozart-effect2.webp",
                                        question='Welke vorm ontstaat er na het afknippen van het hoekje?',
                                        expected_response='B'
                                        )
            return combine_actions(*score, *round)

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_score(cls, session):
        # Feedback message
        last_result = session.last_result()
        feedback = "Goed gedaan! Het juiste antwoord was inderdaad {}.".format(
            last_result.expected_response) if last_result.score else "Helaas, antwoord {} is niet goed! Volgende keer beter".format(last_result.given_response)

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback).action()
        return [score]

    @classmethod
    def get_image_trial(cls, session, section_group, image_url, question, expected_response):
        # Config
        # -----------------
        section = session.section_from_unused_song(
            filter_by={'group': section_group})
        if section == None:
            raise Exception("Error: could not find section for round 1")

        result_pk = cls.prepare_result(
            session, section=section, expected_response=expected_response)

        # Step 1
        # --------------------

        # Listen
        play_config = {'show_animation': True}
        playback = Playback([section],
                            player_type=Playback.TYPE_AUTOPLAY,
                            play_config=play_config
                            )

        listen_config = {
            'auto_advance': True,
            'show_continue_button': False,
            'decision_time': cls.LISTEN_DURATION
        }

        listen = Trial(
            config=listen_config,
            playback=playback,
            title=cls.TITLE,
        ).action()

        # Step 2
        # --------------------

        # Question
        question = ButtonArrayQuestion(
            question=question,
            key='expected_shape',
            choices={
                'A': 'A',
                'B': 'B',
                'C': 'C',
                'D': 'D',
                'E': 'E',
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        image_trial = HTML(
            html='<img src="{}" style="height:calc(100% - 260px);max-height:326px;max-width: 100%;"/>'.format(
                image_url),
            form=form,
            title=cls.TITLE,
            result_id=result_pk
        ).action()

        return [listen, image_trial]

    @classmethod
    def calculate_score(cls, result, form_element, data):
        score = cls.SCORE_CORRECT if result.expected_response == result.given_response else cls.SCORE_WRONG
        return score

    @classmethod
    def get_final_round(cls, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = cls.get_score(session)

        # Final
        final_text = _("Je hebt het uitstekend gedaan!") if session.final_score >= 2 * \
            cls.SCORE_CORRECT else _("Er is ruimte voor verbetering. Wellicht nog een poging wagen?")
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
            button={'text': 'Volgende'}
        ).action()

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment1.html'))
        info = Info(
            body=body,
            heading=_("Het Mozart effect"),
            button_label=_("Terug naar ToontjeHoger"),
            button_link="https://www.amsterdammusiclab.nl"
        ).action()

        return [*score, final, info]
