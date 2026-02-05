from typing import List, TypedDict, Optional
from .base_action import BaseAction
from .button import Button, ButtonAction


class StepAction(TypedDict):
    number: Optional[int]
    description: str


class ExplainerAction(TypedDict):
    view: str
    instruction: str
    button: ButtonAction
    steps: List[StepAction]
    timer: Optional[int]


class Step(object):
    """
    A step in an explainer

    Args:
        description (str): Description of the step
        number (Optional[int]): Optional number of the step
    """

    def __init__(self, description: str, number: Optional[int] = None):
        self.description = description
        self.number = number

    def action(self, number=None) -> StepAction:
        """Create an explainer step, with description and optional number"""
        return {"number": self.number if self.number else number, "description": self.description}


class Explainer(BaseAction):
    """
    Provide data for a explainer that explains the experiment steps

    Relates to client component: Explainer.tsx

    Explainer view automatically proceeds to the following view after timer (in ms) expires. If timer=None, explainer view will proceed to the next view only after a click of a button. Intro explainers should always have timer=None (i.e. interaction with a browser is required), otherwise the browser will not autoplay the first segment.

    Args:
        instruction (str): Instruction for the explainer
        steps (List[Step]): List of steps to explain
        button (Optional[Button]): Configure button that proceeds to the next view
        timer (Optional[int]): Timer in ms
        step_numbers (Optional[bool]): Show step numbers
    """

    view = "EXPLAINER"

    def __init__(
        self,
        instruction: str,
        steps: List[Step],
        button: Button = Button("Let's go!", "colorPrimary"),
        timer: Optional[int] = None,
        step_numbers: Optional[bool] = False,
    ):
        self.instruction = instruction
        self.steps = steps
        self.button = button
        self.timer = timer
        self.step_numbers = step_numbers

    def action(self) -> ExplainerAction:
        if self.step_numbers:
            serialized_steps = [step.action(index + 1) for index, step in enumerate(self.steps)]
        else:
            serialized_steps = [step.action() for step in self.steps]
        return {
            "view": self.view,
            "instruction": self.instruction,
            "button": self.button.action(),
            "steps": serialized_steps,
            "timer": self.timer,
        }
