from django.utils.translation import gettext as _

from .base import Base
from .views import Explainer, CompositeView, Final


class TestBattery(Base):
    experiment_slugs = ['anis', 'bat', 'ddi', 'ddit', 'hbat_bfit', 'hbat_bit', 'hbat_bst', 'rhdis']
    
    @classmethod
    def intro_explainer():
        return Explainer.action(
            instruction=_("You are about to take part in an experiment about rhythm perception."),
            steps=[
                Explainer.step(
                    description=_(
                        "We want to find out what the best way is to test whether someone has a good sense of rhythm!"),
                ),
                Explainer.step(
                    description=_(
                        "You will be doing many little tasks that have something to do with rhythm."),
                ),
                Explainer.step(
                    description=_(
                        "You will get a short explanation and a practice trial for each little task."),
                ),
                Explainer.step(
                    description=_(
                        "You can get reimbursed for completing the entire experiment! Either by earning 5 euros, or by getting study credit (for psychology students at UvA only). You will get instructions for how to get paid or how to get your credit at the end of the experiment."),
                )
            ],
            button_label=_("Continue")
        )
    
    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""
        listening_explainer = Explainer.action(
            instruction=_(
                'General listening instructions:'),
            steps=[
                Explainer.step(
                    description=_(
                        "To make sure that you can do the experiment as well as possible, please do it a quiet room with a stable internet connection."),
                    number=1
                ),
                Explainer.step(
                    description=_("Please use headphones, and turn off sound notifications from other devices and applications (e.g., e-mail, phone messages)."),
                    number=2
                )],
            button_label=_('Start!')
        )
        consent = Consent.action()
        start_session = StartSession.action()
        return combine_actions(
            cls.intro_explainer(),
            listening_explainer,
            consent,
            start_session
        )

def plan_tests(session, experiments):
    """ Given the session and a list of experiments, generate a random order of experiments 
    merge this into the session data.
    """
    session.merge_json_data({'experiments': experiments})
    session.save()
        