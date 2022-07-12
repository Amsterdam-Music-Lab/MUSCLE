from django.utils.translation import gettext as _
from django.template.loader import render_to_string

import random
from .base import Base
from .views import SongSync, Final, Score, Explainer, Step, Consent, StartSession, Playlist, Question, Trial
from .views.form import BooleanQuestion, ChoiceQuestion, Form
from .views.playback import Playback
from .util.questions import DEMOGRAPHICS, EXTRA_DEMOGRAPHICS, next_question, question_by_key
from .util.goldsmiths import MSI_FG_GENERAL, MSI_ALL
from .util.actions import combine_actions

class Huang2022(Base):
    """Rules for the Chinese version of the Hooked experiment."""

    ID = 'HUANG_2022'

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction=_(
                'In this test you will hear a series of tones for each trial.'),
            steps=[
                Step(_(
                    "Do you recognise the song? Try to sing along. The faster you recognise songs, the more points you can earn.")),
                Step(_(
                    "Do you really know the song? Keep singing or imagining the music while the sound is muted. The music is still playing: you just can’t hear it!")),
                Step(_(
                    "Was the music in the right place when the sound came back? Or did we jump to a different spot during the silence?"))
            ],
            button_label=_("Let's go!")).action(True)
        # read consent form from file
        rendered = render_to_string(
            'consent/consent_huang2021.html')
        consent = Consent.action(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))

        explainer_devices = Explainer(
            instruction=_("You can use your smartphone, computer or tablet to participate in this experiment. Please choose the best network in your area to participate in the experiment, such as wireless network (WIFI), mobile data network signal (4G or above) or wired network. If the network is poor, it may cause the music to fail to load or the experiment may fail to run properly. You can access the experiment page through the following channels:"),
            steps=[
                Step(_(
                        "Directly click the link on WeChat (smart phone or PC version, or WeChat Web)"),
                ),
                Step(_(
                        "If the link to load the experiment page through the WeChat app on your cell phone fails, you can copy and paste the link in the browser of your cell phone or computer to participate in the experiment. You can use any of the currently available browsers, such as Safari, Firefox, 360, Google Chrome, Quark, etc."),
                )
            ],
            button_label=_("Continue")
        ).action(True)
        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return [
            explainer,
            consent,
            explainer_devices,
            playlist,
            start_session
        ]

    @classmethod
    def plan_sections(cls, session):
        """Set the plan of tracks for a session.

           Assumes that all tags of 1 have a corresponding tag of 2
           with the same group_id, and vice-versa.
        """

        # Which songs are available?
        songs = list(session.playlist.song_ids())
        random.shuffle(songs)

        # How many sections do we need?
        # 2/3 of the rounds are SongSync, of which 1/4 old songs, 3/4 "free"
        # 1/3 of the rounds are "heard before", of which 1/2 old songs
        # e.g. 30 rounds -> 20 SongSync with 5 songs to be repeated later
        n_rounds = session.experiment.rounds
        n_old = round(0.17 * n_rounds)
        n_new = round(0.17 * n_rounds)
        n_free = n_rounds - 2 * n_old - n_new

        # Assign songs.
        old_songs = songs[:n_old]
        new_songs = songs[n_old:n_old+n_new]
        free_songs = songs[n_old+n_new:n_old+n_new+n_free]
        print(len(old_songs), len(new_songs), len(free_songs))

        # Assign sections.
        old_sections = [session.section_from_song(s) for s in old_songs]
        free_sections = [session.section_from_song(s) for s in free_songs]
        new_sections = [session.section_from_song(s) for s in new_songs]

        # Randomise.
        old_section_info = [{'novelty': 'old', 'id': s.id} for s in old_sections]
        song_sync_sections = old_section_info + [
            {'novelty': 'free', 'id': s.id} for s in free_sections]
        random.shuffle(song_sync_sections)
        heard_before_sections = old_section_info + [
            {'novelty': 'new', 'id': s.id} for s in new_sections]
        random.shuffle(heard_before_sections)
        plan = {
            'song_sync_sections': song_sync_sections,
            'heard_before_sections': heard_before_sections
        }

        print(plan)

        # Save, overwriting existing plan if one exists.
        session.merge_json_data({'plan': plan})
        # session.save() is required for persistence
        session.save()

    @classmethod
    def get_questions(cls, session):
        """Get a random question from each question list, in priority completion order.
        """

        # 1. Demographic questions (9 questions)
        questions = MSI_FG_GENERAL + MSI_ALL + [        
            question_by_key('msi_39_best_instrument'),
            genre_question(),
            question_by_key('dgf_generation'),
            question_by_key('dgf_education'),
            question_by_key(
                'dgf_highest_qualification_expectation', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_occupational_status', EXTRA_DEMOGRAPHICS),
            origin_question(),
            residence_question(),
            gender_question()
        ]
        return [
            Trial(
                title=_("Questionnaire"),
                feedback_form=Form([question], is_profile=True)).action() 
            for question in questions
        ]

    @staticmethod
    def next_round(session, request_session=None):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if session.rounds_complete():

            # Finish session.
            session.finish()
            session.save()
            final = Final(
                session=session,
                final_text=Huang2022.final_score_message(session),
                rank=Huang2022.rank(session),
                show_social=False,
                show_profile_link=True
            ).action()

            return final

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        next_round_number = session.get_next_round()

        # Collect actions.
        actions = []

        if next_round_number == 1:
            # Plan sections
            Huang2022.plan_sections(session)

            # Go to SongSync straight away.
            actions.append(Huang2022.next_song_sync_action(session))
        else:
            # Create a score action.
            config = {'show_section': True, 'show_total_score': True}
            score = Score(
                session,
                config=config,
                title=Huang2022.get_trial_title(session, next_round_number-1)
            )
            actions.append(score.action())

            # Load the heard_before offset.
            try:
                plan = session.load_json_data().get('plan')
                heard_before_offset = len(plan['song_sync_sections']) + 1
                question_offset = heard_before_offset + len(
                    plan['heard_before_sections']) - 1
            except KeyError as error:
                print('Missing plan key: %s' % str(error))
                return actions

            # SongSync rounds
            if next_round_number in range(2, heard_before_offset):
                actions.append(Huang2022.next_song_sync_action(session))
            # HeardBefore rounds
            elif next_round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(Huang2022.heard_before_explainer())
                actions.append(
                    Huang2022.next_heard_before_action(session))
            elif heard_before_offset < next_round_number < question_offset:
                actions.append(
                    Huang2022.next_heard_before_action(session))
            elif next_round_number == question_offset:
                actions.append(Explainer(
                    instruction=_("Please answer some questions on your musical and demographic background"),
                    steps=[],
                    button_label=_("Let's go!")).action()
                )
                actions.extend(Huang2022.get_questions(session))
        return combine_actions(*actions)

    @classmethod
    def next_song_sync_action(cls, session):
        """Get next song_sync section for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            sections = plan['song_sync_sections']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(sections):
            section = \
                session.section_from_any_song(
                    {'id': sections[next_round_number - 1].get('id')})
        if not section:
            print("Warning: no next_song_sync section found")
            section = session.section_from_any_song()
        result_pk = cls.prepare_result(session, section)
        song_sync = SongSync(
            section=section,
            result_id=result_pk
        )
        config = {'style': 'boolean-negative-first'}
        trial = Trial(
            song_sync=song_sync, title=cls.get_trial_title(session, next_round_number), config=config)
        return trial.action()

    @classmethod
    def heard_before_explainer(cls):
        """Explainer for heard-before rounds"""
        return Explainer(
            instruction=_("Bonus Rounds"),
            steps=[
                Step(_("Listen carefully to the music.")),
                Step(_("Did you hear the same song during previous rounds?")),
            ],
            button_label=_("Continue")).action(True)

    @classmethod
    def next_heard_before_action(cls, session):
        """Get next heard_before action for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            sections = plan['heard_before_sections']
            heard_before_offset = len(plan['song_sync_sections'])
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number - heard_before_offset  <= len(sections):
            this_section_info = sections[next_round_number - heard_before_offset - 1]
            section = session.section_from_any_song(
                    {'id': this_section_info.get('id')})
        else:
            return None
        if not section:
            print("Warning: no heard_before section found")
            section = session.section_from_any_song()
        playback = Playback([section])
        expected_result = this_section_info.get('novelty')
        # create Result object and save expected result to database
        result_pk = cls.prepare_result(session, section, expected_result)
        form = Form([BooleanQuestion(
            key='heard_before',
            choices={
                'old': _("YES"),
                'new': _("NO")
            },
            question=_("Did you hear this song in previous rounds?"),
            result_id=result_pk,
            submits=True)])
        config = {'style': 'boolean-negative-first'}
        trial = Trial(
            title=cls.get_trial_title(session, next_round_number),
            playback=playback,
            feedback_form=form,
            config=config,
        )
        return trial.action()
    
    @classmethod
    def get_trial_title(cls, session, next_round_number):
        return _("Round {} / {}".format(
            next_round_number, session.experiment.rounds-1))

    @classmethod
    def final_score_message(cls, session):
        """Create final score message for given session"""

        n_sync_guessed = 0
        sync_time = 0
        n_sync_correct = 0
        n_old_new_expected = 0
        n_old_new_correct = 0

        for result in session.result_set.all():
            json_data = result.load_json_data()
            if json_data.get('result') and json_data['result']['type'] == 'recognized':
                    n_sync_guessed += 1
                    sync_time += json_data['result']['recognition_time']
                    if result.score > 0:
                        n_sync_correct += 1
            else:
                if result.expected_response == 'old':
                    n_old_new_expected += 1
                    if result.score > 0:
                        n_old_new_correct += 1

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
        return " ".join([score_message, song_sync_message, heard_before_message])

    @staticmethod
    def calculate_score(result, data, form_element=None):
        # return 1 if correct, 0 if incorrect
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response:
            if expected_response == form_element['value']:
                return 1
            else:
                return 0
        else:
            # SongSync round
            return SongSync.calculate_score(data)
        
    
    @classmethod
    def handle_results(cls, session, data):
        try:
            form = data.pop('form')
            form_element = form[0]
            result_id = form_element['result_id']
        except:
            form_element = None
            result_id = data['result']['id']
        result = cls.get_result(session, result_id)
        score = cls.calculate_score(result, data, form_element)
        result.save_json_data(data)
        result.score = score
        result.save()
        return result


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
    return ChoiceQuestion(
        key='dgf_region_of_origin',
        view='DROPDOWN',
        question=_(
            "In which region did you spend the most formative years of your childhood and youth?"),
        choices=region_choices
    )


def residence_question():
    return ChoiceQuestion(
        view='DROPDOWN',
        key='dgf_region_of_residence',
        question=_("In which region do you currently reside?"),
        choices=region_choices
    )

def gender_question():
    return ChoiceQuestion(
        key='dgf_gender_identity',
        view='RADIOS',
        question="您目前对自己的性别认识?",
        choices={
            'male': "男",
            'Female': "女",
            'Others': "其他",
            'no_answer': "不想回答"
        },
        is_skippable=True
    )


def genre_question():
    return ChoiceQuestion(
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
