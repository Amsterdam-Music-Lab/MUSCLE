import math
from django.utils.translation import gettext as _

class TwoSong:  # pylint: disable=too-few-public-methods
    """
    Provide data for a TwoSong view that has two playable sections, a question and has two customizable buttons

    Relates to client component: TwoSong.js   
    """

    ID = 'TWO_SONG'

    @staticmethod
    def calculate_score(session, data):
        """Calculate score for given result data"""
        score = 0

        # Calculate from the data object
        # If requested keys don't exist, return None
        try:

            config = data['config']
            result = data['result']

            # Calculate scores based on result type
            if result['given_result'] == config['expected_result']:
                # correct
                score = 1
            else:
                # wrong
                score = -1

        except KeyError as error:
            print('KeyError: %s' % str(error))
            return None

        return score

    @staticmethod
    def action(session, introduction, instruction, section2, section1, expected_result=0,
               button1_label="Fragment A", button1_color="blue", button2_label="Fragment B", button2_color="teal",
               section1_color="blue", section1_label="A", section2_color="teal", section2_label="B",
               ready_message="", ready_time=0.5, listen_first=True):
        """
        Get data for two_song action

        session: current session
        introduction: introduction (above players)
        instruction: instruction (under players)
        expected_result: correct answer (correspondents to button nr 1 or 2) 
                        - 0 in case there is no correct answer, e.g. preference question

        section1: first secion
        section1_color: Section1 player color e.g. "teal" *
        section1_label: Section1 label, e.g. "A"
        section2: second section
        section2_color: Section2 player color e.g. "blue" *
        section2_label: Section2 label, e.g. "B"

        button1_label: Button1 label e.g. "Fragment A"
        button1_color: Button1 color e.g. "teal"*
        button2_label: Button2 label e.g. "Fragment B"
        button2_color: Button2 color e.g. "red"*

        * Available colors: red, teal, yellow, pink, gray, blue, indigo

        ready_message: Message shown during preload countdown
        ready_time: Time to ready up before questions starts; make 0 to eliminate preload.
                    in that case only a spinner will be shown in case preloading the audio takes
                    too much time (e.g. slow connections)

        listen_first: Force user play both sections, to enable the two buttons
        """

        # Create action
        action = {
            'view': TwoSong.ID,
            'title': _('Round {} / {}').format(get_next_round(), session.experiment.rounds),
            'ready_message': ready_message,
            'instruction': instruction,
            'introduction': introduction,

            'section1_color': section1_color,
            'section1_label': section1_label,
            'section2_color': section2_color,
            'section2_label': section2_label,

            'button1_label': button1_label,
            'button1_color': button1_color,
            'button2_label': button2_label,
            'button2_color': button2_color,
            'listen_first': listen_first,
        }

        # Section
        action['section1'] = {
            'id': section1.id,
            'artist': section1.artist,
            'song': section1.name,
            'url': section1.absolute_url(),
        }
        action['section2'] = {
            'id': section2.id,
            'artist': section2.artist,
            'song': section2.name,
            'url': section2.absolute_url(),
        }

        # Config
        action['config'] = {
            'ready_time': ready_time,
            'expected_result': expected_result,
        }

        return action
