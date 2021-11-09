from django.utils.translation import gettext as _

from experiment.models import Section
from .views import CompositeView, Explainer, Final
from .views.form import ChoiceQuestion, Form

from .base import Base
from .h_bat import HBat

from .util.score import get_average_difference_level_based

class BST(HBat):
    """ Rules for the BST experiment, which follow closely
    the HBAT rules. """
    ID = 'BST'

    @classmethod
    def intro_explainer(cls):
        return Explainer.action(
            instruction=_(
                'In this test you will hear a number of rhythms which have a regular beat.'),
            steps=[
                Explainer.step(
                    description=_(
                        "It's your job to decide if the rhythm has a 2-QUARTER BEAT (a march) or a 3-QUARTER BEAT (a waltz)."),
                    number=1
                ),
                Explainer.step(
                    description=_("Every second tone in a 2-quarter beat is louder and every third tone in a 3-quarter beat is louder."),
                    number=2
                ),
                Explainer.step(
                    description=_(
                        'During the experiment it will become more difficult to hear the difference.'),
                    number=3
                ),
                Explainer.step(
                    description=_(
                        "Try to answer as accurately as possible, even if you're uncertain."),
                    number=4
                )],
            button_label='Ok'
        )

    @classmethod
    def next_trial_action(cls, session, trial_condition, level=1):
        """
        Get the next actions for the experiment
        trial_condition is either 1 or 0
        level can be 1 (? dB difference) or higher (smaller differences)
        """
        try:
            section = session.playlist.section_set.filter(group_id=level).get(tag_id=trial_condition)
        except Section.DoesNotExist:
            return None
        expected_result = 'in2' if trial_condition else 'in3'
        # create Result object and save expected result to database
        result_pk = Base.prepare_result(session, section, expected_result)
        instructions = {
            'preload': '',
            'during_presentation': ''
        }
        question = ChoiceQuestion(
            key='longer_or_equal',
            question=_(
                "Is the rhythm a 2-QUARTER BEAT or a 3-QUARTER BEAT?"),
            choices={
                'in2': _('2-QUARTER BEAT'),
                'in3': _('3-QUARTER BEAT')
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])
        view = CompositeView(
            section=section,
            feedback_form=form.action(),
            instructions=instructions,
            title=_('Meter detection')
        )
        config = {
            'listen_first': True,
            'decision_time': section.duration + .5
        }
        return view.action(config)

    @classmethod
    def response_explainer(cls, correct, in2, button_label=_('Next fragment')):
        if correct:
            if in2:
                instruction = _(
                    'The rhythm was a 2-QUARTER BEAT. Your answer was correct.')
            else:
                instruction = _(
                    'The rhythm was a 3-QUARTER BEAT. Your answer was correct.')
        else:
            if in2:
                instruction = _(
                    'The rhythm was a 2-QUARTER BEAT. Your answer was incorrect.')
            else:
                instruction = _(
                    'The rhythm was a 3-QUARTER BEAT. Your response was incorrect.')
        return Explainer.action(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )
    
    @classmethod
    def finalize_experiment(cls, session):
        """ if either the max_turnpoints have been reached,
        or if the section couldn't be found (outlier), stop the experiment
        """
        loudness_diff = get_average_difference_level_based(session, 6)
        score_message = _("Well done! You heard the difference \
            when the accented tone was only {} dB louder!").format(loudness_diff)
        session.finish()
        session.save()
        return Final.action(
            title=_('End'),
            session=session,
            score_message=score_message
        )