from os.path import join

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .views.form import ChoiceQuestion, Form
from .views import Trial, Consent, Final, Explainer, StartSession, Step, Playlist
from .views.playback import Playback
from .base import Base
from .util.actions import combine_actions


class Hooked(Base):
    """ Inherit from these rules to set up a variant
    of the Hooked on Music game
    """
    ID = 'HOOKED'

    experiment_name = 'Hooked on Music'
    researcher = 'Dr John Ashley Burgoyne'
    researcher_contact = 'John Ashley Burgoyne (phone number: +31 20 525 7034; \
        e-mail: j.a.burgoyne@uva.nl; Science Park 107, 1098 GE Amsterdam)'

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="How to Play",
            steps=[
                Step(_("Do you recognise the song? Try to sing along. The faster you recognise songs, the more points you can earn.",)),
                Step(_("Do you really know the song? Keep singing or imagining the music while the sound is muted. The music is still playing: you just can’t hear it!")),
                Step(_("Was the music in the right place when the sound came back? Or did we jump to a different spot during the silence?"))
            ],   
        ).action(step_numbers=True)

        # 2. Get informed consent.
        context = {
            'experiment_name': cls.experiment_name,
            'researcher': cls.researcher,
            'resarcher_contact': cls.researcher_contact
        }
        consent_text = render_to_string(join('consent', 
            'consent_hooked.html'), context=context)
        consent = Consent.action(consent_text)
        
        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return combine_actions(
            explainer,
            consent,
            playlist,
            start_session
        )
    
    @classmethod
    def next_round(cls, session):
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
                Final.action(
                    session=session,
                    final_text=cls.final_score_message(session),
                    rank=cls.rank(session)
                )
            )
        
        else:
            last_result = session.result_set.order_by('-created_at').first()
            section = session.section_from_unused_song()
            result_pk = Base.prepare_result(session, section)
            question = ChoiceQuestion(
                question=_('Do you recognise this song?'),
                key='recognize',
                choices={
                    'YES': _('YES'),
                    'NO': _('NO')
                },
                view='BUTTON_ARRAY',
                result_id=result_pk,
                submits=True
            )
            form = Form([question])
            play_config = {
                'decision_time': 2,
                'show_animation': True,
                'auto_advance': True
            }
            playback = Playback('AUTOPLAY', [section], config=play_config)
            view = Trial(
                playback=playback,
                feedback_form=form,
                title=_('Hooked on Music')
            )
            return view.action()
    
    def calculate_score(result, form_element):
        """Calculate score for given result data"""
        score = 0

        # Calculate from the data object
        # If requested keys don't exist, return None
        try:

            config = data['config']
            result = data['result']

            # Calculate scores based on result type
            if result['type'] == 'time_passed':
                score = math.ceil(-result['recognition_time'])

            elif result['type'] == 'not_recognized':
                score = 0

            elif result['type'] == 'recognized':
                # Get score
                score = math.ceil(
                    config['recognition_time'] - result['recognition_time']
                )

                if config['continuation_correctness'] != result['continuation_correctness']:
                    score *= -1

        except KeyError as error:
            print('KeyError: %s' % str(error))
            return None

        return score