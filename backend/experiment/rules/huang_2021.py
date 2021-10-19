from django.utils.translation import gettext as _
from django.template.loader import render_to_string

import random
from .base import Base
from .views import SongSync, SongBool, FinalScore, Score, Explainer, Consent, StartSession, Playlist, Question
from .util.questions import DEMOGRAPHICS, EXTRA_DEMOGRAPHICS, next_question, question_by_key
from .util.goldsmiths import MSI_FG_GENERAL, MSI_ALL
from .util.actions import combine_actions


class Huang2021(Base):
    """Rules for the Chinese version of the Hooked experiment."""

    ID = 'HUANG_2021'

    @staticmethod
    def first_round(experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer.action(
            instruction=_("How to Play"),
            steps=[
                Explainer.step(
                    description=_(
                        "Do you recognise the song? Try to sing along. The faster you recognise songs, the more points you can earn."),
                    number=1
                ),
                Explainer.step(
                    description=_(
                        "Do you really know the song? Keep singing or imagining the music while the sound is muted. The music is still playing: you just can’t hear it!"),
                    number=2
                ),
                Explainer.step(
                    description=_(
                        "Was the music in the right place when the sound came back? Or did we jump to a different spot during the silence?"),
                    number=3
                )
            ],
            button_label=_("Let's go!")
        )

        # read consent form from file
        rendered = render_to_string(
            'consent_huang2021.html')
        consent = Consent.action(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))

        explainer_devices = Explainer.action(
            instruction=_("You can use your smartphone, computer or tablet to participate in this experiment. Please choose the best network in your area to participate in the experiment, such as wireless network (WIFI), mobile data network signal (4G or above) or wired network. If the network is poor, it may cause the music to fail to load or the experiment may fail to run properly. You can access the experiment page through the following channels:"),
            steps=[
                Explainer.step(
                    description=_(
                        "Directly click the link on WeChat (smart phone or PC version, or WeChat Web);"),
                    number=1
                ),
                Explainer.step(
                    description=_(
                        "If the link to load the experiment page through the WeChat app on your cell phone fails, you can copy and paste the link in the browser of your cell phone or computer to participate in the experiment. You can use any of the currently available browsers, such as Safari, Firefox, 360, Google Chrome, Quark, etc."),
                    number=2
                )
            ],
            button_label=_("Continue")
        )
        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return combine_actions(
            explainer,
            consent,
            explainer_devices,
            playlist,
            start_session
        )

    @staticmethod
    def plan_sections(session):
        """Set the plan of tracks for a session.

           Assumes that all tags of 1 have a corresponding tag of 2
           with the same group_id, and vice-versa.
        """

        # Which songs are available?
        old_new_song_set = set(session.playlist.song_ids())

        # How many sections do we need?
        n_old = round(0.17 * session.experiment.rounds)
        n_new = round(0.33 * session.experiment.rounds) - n_old
        n_free = session.experiment.rounds - 2 * n_old - n_new

        print(n_old, n_new, n_free)

        # Assign songs.
        old_songs = random.sample(old_new_song_set, k=n_old)
        print(len(old_songs), len(old_new_song_set))
        free_songs = random.sample(old_new_song_set - set(old_songs), k=n_free)
        print(len(free_songs))
        new_songs = \
            random.sample(old_new_song_set -
                          set(old_songs + free_songs), k=n_new)

        # Assign sections.
        old_sections = [session.section_from_song(s) for s in old_songs]
        free_sections = [session.section_from_song(s) for s in free_songs]
        new_sections = [session.section_from_song(s) for s in new_songs]

        # Get IDs.
        old_ids = [s.id for s in old_sections]
        free_ids = [s.id for s in free_sections]
        new_ids = [s.id for s in new_sections]

        # Randomise.
        permutation_1 = random.sample(range(n_free + n_old), n_free + n_old)
        permutation_2 = random.sample(range(n_old + n_new), n_old + n_new)
        plan = {
            'n_song_sync': n_free + n_old,
            'n_heard_before': n_old + n_new,
            'sections': (
                [(free_ids + old_ids)[i] for i in permutation_1]
                + [(old_ids + new_ids)[i] for i in permutation_2]
            ),
            'novelty': (
                [(['free'] * n_free + ['old'] * n_old)[i]
                 for i in permutation_1]
                + [(['old'] * n_old + ['new'] * n_new)[i]
                   for i in permutation_2]
            )
        }

        print(plan)

        # Save, overwriting existing plan if one exists.
        session.merge_json_data({'plan': plan})
        # session.save() is required for persistence
        session.save()

    @staticmethod
    def get_random_question(session):
        """Get a random question from each question list, in priority completion order.

        Participants will not continue to the next question set until they
        have completed their current one.
        """

        # Constantly re-randomising is mildly inefficient, but it's not
        # worth the trouble to save blocked, randomised question lists persistently.

        # 1. Demographic questions (9 questions)
        questions = [
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_generation'),
            question_by_key('dgf_education'),
            residence_question(),
            question_by_key('msi_39_best_instrument'),
            question_by_key(
                'dgf_highest_qualification_expectation', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_occupational_status', EXTRA_DEMOGRAPHICS),
            origin_question(),
            genre_question()


        ]
        question = next_question(
            session,
            random.sample(questions, len(questions)),
        )

        # 2. General music sophistication (18 questions)
        if question is None:
            question = \
                next_question(
                    session,
                    random.sample(MSI_FG_GENERAL, len(MSI_FG_GENERAL)),
                )

        # 3. Complete music sophistication (20 questions)
        if question is None:
            # next_question() will skip the FG questions from before
            question = \
                next_question(
                    session,
                    random.sample(MSI_ALL, len(MSI_ALL)),
                )

        return question

    @staticmethod
    def next_round(session):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if session.rounds_complete():

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            return combine_actions(
                Score.action(session),
                FinalScore.action(
                    session=session,
                    score_message=Huang2021.final_score_message(session),
                    rank=Huang2021.rank(session),
                    show_social=False
                )
            )

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        next_round_number = session.get_next_round()

        # Collect actions.
        actions = []

        if next_round_number == 1:
            # Plan sections
            Huang2021.plan_sections(session)

            # Go to SongSync straight away.
            actions.append(Huang2021.next_song_sync_action(session))
        else:
            # Create a score action.
            actions.append(Score.action(session))

            # Load the heard_before offset.
            try:
                heard_before_offset = \
                    session.load_json_data()['plan']['n_song_sync'] + 1
            except KeyError as error:
                print('Missing plan key: %s' % str(error))
                return combine_actions(*actions)

            # SongSync rounds. Skip questions until Round 5.
            if next_round_number in range(2, 5):
                actions.append(Huang2021.next_song_sync_action(session))
            if next_round_number in range(5, heard_before_offset):
                actions.append(Huang2021.get_random_question(session))
                actions.append(Huang2021.next_song_sync_action(session))

            # HeardBefore rounds
            if next_round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(Huang2021.heard_before_explainer())
                actions.append(
                    Huang2021.next_heard_before_action(session))
            if next_round_number > heard_before_offset:
                actions.append(Huang2021.get_random_question(session))
                actions.append(
                    Huang2021.next_heard_before_action(session))

        return combine_actions(*actions)

    @staticmethod
    def next_song_sync_action(session):
        """Get next song_sync section for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            sections = plan['sections']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(sections):
            section = \
                session.section_from_any_song(
                    {'id': sections[next_round_number - 1]})
        if not section:
            print("Warning: no next_song_sync section found")
            section = session.section_from_any_song()
        action = SongSync.action(
            session=session,
            section=section
        )

        return action

    @staticmethod
    def heard_before_explainer():
        """Explainer for heard-before rounds"""
        return Explainer.action(
            instruction=_("Bonus Rounds"),
            steps=[
                Explainer.step(
                    description=_("Listen carefully to the music."),
                    number=1
                ),
                Explainer.step(
                    description=_(
                        "Did you hear the same song during previous rounds?"),
                    number=2
                ),
            ],
            button_label=_("Continue"))

    @staticmethod
    def next_heard_before_action(session):
        """Get next heard_before action for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            sections = plan['sections']
            novelty = plan['novelty']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(sections):
            section = \
                session.section_from_any_song(
                    {'id': sections[next_round_number - 1]})
        if not section:
            print("Warning: no heard_before section found")
            section = session.section_from_any_song()

        return SongBool.action(
            instruction=_("Did you hear this song in previous rounds?"),
            session=session,
            section=section,
            expected_result=int(novelty[next_round_number - 1] == 'old')
        )

    @staticmethod
    def final_score_message(session):
        """Create final score message for given session"""

        n_sync_guessed = 0
        sync_time = 0
        n_sync_correct = 0
        n_old_new_expected = 0
        n_old_new_correct = 0

        for result in session.result_set.all():
            json_data = result.load_json_data()
            try:
                if json_data['view'] == 'SONG_SYNC':
                    if json_data['result']['type'] == 'recognized':
                        n_sync_guessed += 1
                        sync_time += json_data['result']['recognition_time']
                        if result.score > 0:
                            n_sync_correct += 1
                else:
                    if json_data['config']['expected_result'] == 1:
                        n_old_new_expected += 1
                        if result.score > 0:
                            n_old_new_correct += 1
            except KeyError as error:
                print('KeyError: %s' % str(error))
                continue

        score_message = _(
            "Well done!") if session.final_score > 0 else _("Too bad!")
        if n_sync_guessed == 0:
            song_sync_message = _("You did not recognise any songs at first.")
        else:
            song_sync_message = _("It took you %(n_seconds)d s to recognise a song on average, \
                and you correctly identified %(n_correct)d out of the %(n_total)d songs you thought you knew.") % {
                'n_seconds': round(sync_time / n_sync_guessed, 1),
                'n_correct': n_sync_correct,
                'n_total': n_sync_guessed
            }
        heard_before_message = _("During the bonus rounds, you remembered %(n_correct)d of the %(n_total)d songs that came back.") % {
            'n_correct': n_old_new_correct,
            'n_total': n_old_new_expected
        }
        return score_message + " " + song_sync_message + " " + heard_before_message


region_choices = {
    'BJ': '北京',
    'TJ': '天津',
    'HB': '河北',
    'SHX': '山西',
    'NMG': '内蒙古',
    'LN': '辽宁',
    'JL': '吉林',
    'HLJ': '黑龙江',
    'SH': '上海',
    'JS': '江苏',
    'ZJ': '浙江',
    'AH': '安徽',
    'FJ': '福建',
    'JX': '江西',
    'SD': '山东',
    'HEN': '河南',
    'HUB': '湖北',
    'HUN': '湖南',
    'GD': '广东',
    'GX': '广西',
    'HN': '海南',
    'CQ': '重庆',
    'SC': '四川',
    'GZ': '贵州',
    'YN': '云南',
    'XZ': '西藏',
    'SX': '陕西',
    'GS': '甘肃',
    'QH': '青海',
    'NX': '宁夏',
    'XJ': '新疆',
    'HK': '香港',
    'MC': '澳门',
    'TW': '台湾',
    'QT': '国外'
}


def origin_question():
    return Question.dropdown(
        key='dgf_region_of_origin',
        question=_(
            "In which region did you spend the most formative years of your childhood and youth?"),
        choices=region_choices
    )


def residence_question():
    return Question.dropdown(
        key='dgf_region_of_residence',
        question=_("In which region do you currently reside?"),
        choices=region_choices
    )


def genre_question():
    return Question.radios(
        key='dgf_genre_preference',
        question=_(
            "To which group of musical genres do you currently listen most?"),
        choices={
            'unpretentious': _("Pop/Country/Religious"),
            'Chinese artistic': _("Folk/Mountain songs"),
            'sophisticated': _("Western classical music/Jazz/Opera/Musical"),
            'classical': _("Chinese opera"),
            'intense': _("Rock/Punk/Metal"),
            'mellow': _("Dance/Electronic/New Age"),
            'contemporary': _("Hip-hop/R&B/Funk"),
        }
    )
