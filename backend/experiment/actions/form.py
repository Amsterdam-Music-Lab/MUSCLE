from typing import Any, Dict, List

from django.utils.translation import gettext_lazy as _

from .base_action import BaseAction

class Form(BaseAction):
    """The Form action is a view which brings together an array of questions with a submit and an optional skip button.

    Args:
        form (List[Question]): List of question components
        submit_label (str): Text for submit button
        skip_label (str): Text for skip button
        is_skippable (bool): Whether form can be skipped

    Example:
        ```python
        form = Form([
            TextQuestion(
                key="name",
                text="What's your name?",
                explainer="Please enter your full name.",
            ),
            BooleanQuestion(
                key="is_student",
                text="Are you a student?",
            ),
        ])
        ```
    """

    def __init__(
        self,
        form: List[Any],
        submit_label: str = _("Continue"),
        skip_label: str = _("Skip"),
        is_skippable: bool = False,
    ) -> None:
        self.form = form
        self.submit_label = submit_label
        self.skip_label = skip_label
        self.is_skippable = is_skippable

    def action(self) -> Dict[str, Any]:
        serialized_form = [question.action() for question in self.form]
        return {
            "form": serialized_form,
            "submit_label": self.submit_label,
            "skip_label": self.skip_label,
            "is_skippable": self.is_skippable,
        }
