from .base_action import BaseAction

class Explainer(BaseAction):
    """
    Provide data for a explainer that explains the experiment steps

    Relates to client component: Explainer.js

    Explainer view automatically proceeds to the following view after timer (in ms) expires. If timer=None, explainer view will proceed to the next view only after a click of a button. Intro explainers should always have timer=None (i.e. interaction with a browser is required), otherwise the browser will not autoplay the first segment.
    """

    ID = "EXPLAINER"

    def __init__(self, instruction, steps, button_label="Let's go!", timer=None, step_numbers=False):
        self.instruction = instruction
        self.steps = steps
        self.button_label = button_label
        self.timer = timer
        self.step_numbers = step_numbers

    def action(self):
        """Get data for explainer action"""
        if self.step_numbers:
            serialized_steps = [step.action(index+1) for index, step in enumerate(self.steps)]
        else:
            serialized_steps = [step.action() for step in self.steps]
        return {
            'view': self.ID,
            'instruction': self.instruction,
            'button_label': self.button_label,
            'steps': serialized_steps,
            'timer': self.timer,
        }


class Step(object):

    def __init__(self, description, number=None):
        self.description = description
        self.number = number

    def action(self, number=None):
        """Create an explainer step, with description and optional number"""
        return {
            'number': self.number if self.number else number,
            'description': self.description
        }
