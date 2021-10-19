import math
from django.utils.translation import gettext as _


class TwoAlternativeForced:  # pylint: disable=too-few-public-methods
    """
    Provide data for a TwoAlternativeForced view that (auto)plays a section, shows a question and has two customizable buttons

    Relates to client component: TwoAlternativeForced.js    
    """

    ID = 'TWO_ALTERNATIVE_FORCED'

    @staticmethod
    def calculate_score(session, data):
        """Calculate score for given result data"""
        score = 0

        # Calculate from the data object
        # If requested keys don't exist, return None
        try:

            config = data['config']
            result = data['result']
            time = result['decision_time']

            # Calculate scores based on result type
            if result['type'] == 'time_passed':
                score = math.ceil(-time)

            else:
                if result['given_result'] == config['expected_result']:
                    # correct
                    score = math.ceil(
                        config['decision_time'] - result['decision_time']
                    )
                else:
                    # wrong
                    score = math.floor(-time)

        except KeyError as error:
            print('KeyError: %s' % str(error))
            return None

        return score

    @staticmethod
    def action(session, introduction, instruction, section, auto_play, expected_result,
               button1_label, button1_color, button2_label, button2_color,
               ready_message="Get ready!", ready_time=3, decision_time=5, auto_advance=True,
               listen_first=False, time_pass_break=False, title=None):
        """
        Get data for two_alternative_forced action

        session: current session
        introduction: introduction (above circle)
        instruction: instruction (under circle)
        section: section to play
        auto_play: Should the song auto play when question starts?
        expected_result: correct answer (correspondents to button nr 1 or 2)

        button1_label: Button1 label e.g. "Jazz"
        button1_color: Button1 color e.g. "teal"*
        button2_label: Button2 label e.g. "Rock"
        button2_color: Button2 color e.g. "red"*
        * Available colors: red, teal, yellow, pink, gray, blue, indigo

        ready_message: Message shown during preload countdown
        ready_time: Time to ready up before questions starts; make 0 to eliminate preload.
                    in that case only a spinner will be shown in case preloading the audio takes
                    too much time (e.g. slow connections)
        decision_time: Time the user has to make a decision
        auto_advance: Advance when decision time has passed
                    - True: user should answer within the decision_time
                    - False: user has unlimited time answer; music will be stopped after decision_time

        listen_first: Force user to listen to the section for the duration of decision_time
                    - The buttons will be enabled after the decision_time has passed
                    - auto_advance should be False (or will be made in code below)
                    - One can reduce the decision_time in the result with the original decision_time to get the user response time

        time_pass_break: When time has passed, submit the result immediately; skipping any subsequent actions (e.g. a certainty question)
                    - Can not be combined with listen_first (True)
                    - Can not be combined with auto_advance (False)
        title: override title string

        """

        # Force auto_advance to be False when listen_full_section is true
        if listen_first:
            auto_advance = False

        # Validate time_pass_break settings
        if time_pass_break:
            if listen_first:
                print(
                    "Warning: Do not combine listen_first (True) and time_pass_break (True)")
                time_pass_break = False
            if not auto_advance:
                print(
                    "Warning: Do not combine auto_advance (False) and time_pass_break (True)")
                time_pass_break = False
        if not title:
            title = _('Round {} / {}').format(session.get_next_round(), session.experiment.rounds)
        # Create action
        action = {
            'view': TwoAlternativeForced.ID,
            'title': title,
            'auto_play': auto_play,
            'auto_advance': auto_advance,
            'ready_message': ready_message,
            'instruction': instruction,
            'listen_first': listen_first,
            'time_pass_break': time_pass_break,
            'introduction': introduction,
            'button1_label': button1_label,
            'button1_color': button1_color,
            'button2_label': button2_label,
            'button2_color': button2_color,
        }

        # Section
        action['section'] = {
            'id': section.id,
            'artist': section.artist,
            'song': section.name,
            'url': section.absolute_url(),
        }

        # Config
        action['config'] = {
            'ready_time': ready_time,
            'decision_time': decision_time,
            'expected_result': expected_result,
        }

        return action
