from os.path import join
import random
import math

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
    decision_time = 2
    silence_time = 2

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
            if last_result and last_result.comment == 'recognized':
                section = last_result.section
                question = ChoiceQuestion(
                    question=_('Did the track come back in the right place?'),
                    key='sync',
                    choices={
                        'YES': _('YES'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY',
                    result_id=last_result.id,
                    submits=True
                )
                form = Form([question])
                silence_config = {
                    'decision_time': cls.silence_time,
                    'show_animation': False,
                    'auto_advance': True,
                    'mute': True
                }
                playback = Playback('AUTOPLAY', [section])
                silence_view = Trial(
                    playback=playback,
                    feedback_form=None,
                    title=_('Hooked on Music')
                )
                continuation_correctness = random.randint(0, 1) == 1
                last_result.expected_response = continuation_correctness
                last_result.save()
                continuation_offset = random.randint(100, 150) / 10 if not continuation_correctness else 0
                playhead = cls.decision_time + cls.silence_time + continuation_offset
                sync_config = {
                    'decision_time': cls.decision_time,
                    'show_animation': True,
                    'auto_advance': True,
                    'playhead': playhead
                }
                sync_view = Trial(
                    playback=playback,
                    feedback_form=form,
                    title=_('Hooked on Music')
                )
                return combine_actions(silence_view.action(), sync_view.action())
            else:    
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
                    'decision_time': cls.decision_time,
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
    
    @classmethod
    def calculate_score(cls, result, form_element, data):
        """Calculate score for given result data"""
        score = result.score

        # Calculate from the form_element
        if form_element.get('key') == 'recognize':
            value = form_element.get('value')
            if value == 'TIMEOUT':
                score = math.ceil(-cls.decision_time)
            elif value == 'NO':
                score = 0
            elif value == 'YES':
                score = math.ceil(
                    cls.decision_time - data.get('decision_time')
                )
                result.comment = 'recognized'
                
        else:
            result.comment = 'synced'
            if result.expected_response != form_element.value:
                score *= -1
        result.save()
        return score