from typing import Any, Dict, List, Optional

from django.utils.translation import gettext_lazy as _

from .base_action import BaseAction
from .button import Button

class Form(BaseAction):
    """The Form action is a view which brings together an array of questions with a submit and an optional skip button.

    Args:
        form (List[Question]): List of question components
        submit_button (Button): Button object specifying label and color of submit button
        skip_button (Button): Button object specifying label and color of skip button

    Example:
        ```python
        form = Form([
            TextQuestion(
                key="name",
                text="What's your name?",
                explainer="Please enter your full name.",
            ),
            ButtonArrayQuestion(
                key="is_student",
                text="Are you a student?",
                choices={'YES': _('YES'), 'NO': _('NO')},
            ),
        ])
        ```
    """

    def __init__(
        self,
        form: List[Any],
        submit_button: Optional[Button] = Button(_("Submit"), 'colorPrimary'),
        skip_button: Optional[Button] = Button(_("Skip"), 'colorGrey'),
    ) -> None:
        self.form = form
        self.submit_button = submit_button
        self.skip_button = skip_button

    def action(self) -> Dict[str, Any]:
        serialized_form = [question.action() for question in self.form]
        return {
            "form": serialized_form,
            "submitButton": self.submit_button.action() if self.submit_button else None,
            "skipButton": self.skip_button.action() if self.skip_button else None,
        }
