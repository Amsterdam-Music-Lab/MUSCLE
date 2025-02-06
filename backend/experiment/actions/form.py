from typing import Dict, List, Optional, Any, Literal
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .styles import ButtonStyle, ColorScheme
from .base_action import BaseAction


QuestionView = Literal[
    "AUTOCOMPLETE", "BUTTON_ARRAY", "CHECKBOXES", "DROPDOWN", "RADIOS", "RANGE", "TEXT_RANGE", "ICON_RANGE", "STRING"
]


class Question(BaseAction):
    """The Question action is a component that represents a single question in a form.

    Args:
        key (str): Unique identifier for the question in results table
        result_id (Optional[int]): Optional result ID for testing purposes
        view (QuestionView): Widget type to use in frontend (default: 'STRING')
        explainer (str): Additional instructions for the question
        question (str): The actual question text
        is_skippable (bool): Whether question can be skipped
        submits (bool): Whether answering submits the form
        style Optional[list[str]]: CSS class name(s) set in the frontend for styling

    Example:
        ```python
        question = Question(
            key="name",
            question="What's your name?",
            explainer="Please enter your full name.",
            is_skippable=True,
            submits=True,
            style=[ColorScheme.BOOLEAN],
            view="STRING",
        )
        ```

    Note:
        - You can use any of the child classes to create a specific question type (e.g. TextQuestion, BooleanQuestion). \n
        - The `key` should be unique within the form. \n
    """

    def __init__(
        self,
        key: str,
        result_id: Optional[int] = None,
        view: QuestionView = "STRING",
        explainer: str = "",
        question: str = "",
        is_skippable: bool = False,
        submits: bool = False,
        style: list[str] = [ColorScheme.NEUTRAL.value],
    ) -> None:
        self.key = key
        self.view = view
        self.explainer = explainer
        self.question = question
        self.result_id = result_id
        self.is_skippable = is_skippable
        self.submits = submits
        self.style = self._apply_style(style)

    def action(self) -> Dict[str, Any]:
        if settings.TESTING and self.result_id:
            from result.models import Result

            result = Result.objects.get(pk=self.result_id)
            if result and result.expected_response:
                self.expected_response = result.expected_response
        return super().action()


class NumberQuestion(Question):
    """A question that accepts numeric input.

    Args:
        input_type (str): Type of number input (default: 'number')
        min_value (int): Minimum allowed value
        max_value (int): Maximum allowed value
        **kwargs: Additional Question arguments
    """

    def __init__(self, input_type: str = "number", min_value: int = 0, max_value: int = 120, **kwargs) -> None:
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.input_type = input_type
        self.view = "STRING"


class TextQuestion(Question):
    """A question that accepts text input.

    Args:
        input_type (str): Type of text input (default: 'text')
        max_length (int): Maximum character length
        **kwargs: Additional Question arguments
    """

    def __init__(self, input_type: str = "text", max_length: int = 64, **kwargs) -> None:
        super().__init__(**kwargs)
        self.max_length = max_length  # the maximum length of the question's answer in characters
        self.input_type = input_type
        self.view = "STRING"


class BooleanQuestion(Question):
    """A yes/no question component.

    Args:
        choices (Optional[Dict[str, str]]): Custom yes/no labels
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = BooleanQuestion(
            key="is_student",
            question="Are you a student?",
            choices={
                "no": "Nope", # Use _("No") for translation (default)
                "yes": "Yep"
            },
        )
        ```
    """

    def __init__(self, choices: Optional[Dict[str, str]] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices or {"no": _("No"), "yes": _("Yes")}
        self.view = "BUTTON_ARRAY"
        style = kwargs.get('style') or [
            ColorScheme.BOOLEAN_NEGATIVE_FIRST,
            ButtonStyle.LARGE_GAP,
        ]
        self.style = self._apply_style(style)


class ChoiceQuestion(Question):
    """A question with (multiple) choice options.

    Args:
        choices (Dict[str, str]): Available options
        min_values (int): Minimum number of selections required
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = ChoiceQuestion(
            key="color",
            question="What's your favorite color?",
            choices={
                "red": "Red", # or _("Red") for translation
                "green": "Green",
                "blue": "Blue",
            },
            min_values=1,
        )
        ```

    Note:
        - To have multiple choices (participant can select more than one answer), set `view` to 'CHECKBOXES'
    """

    def __init__(self, choices: Dict[str, str], min_values: int = 1, **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices
        # minimal number of values to be selected, 1 or more
        # TODO: enforce (raise ValueError), or math.floor it
        self.min_values = min_values


class DropdownQuestion(Question):
    """A question with a dropdown menu.

    Args:
        choices (Dict[str, str]): Available options
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = DropdownQuestion(
            key="color",
            question="What's your favorite color?",
            choices={
                "red": "Red", # or _("Red") for translation
                "green": "Green",
                "blue": "Blue",
            },
        )
        ```
    """

    def __init__(self, choices: Dict[str, str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices
        self.view = "DROPDOWN"


class AutoCompleteQuestion(Question):
    """A question with an autocomplete input.

    Args:
        choices (Dict[str, str]): Available options
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = AutoCompleteQuestion(
            key="color",
            question="What's your favorite color?",
            choices={
                "red": "Red", # or _("Red") for translation
                "green": "Green",
                "blue": "Blue",
            },
        )
        ```
    """

    def __init__(self, choices: Dict[str, str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices
        self.view = "AUTOCOMPLETE"


class RadiosQuestion(Question):
    """A question with radio buttons.

    Args:
        choices (Dict[str, str]): Available options
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = RadiosQuestion(
            key="color",
            question="What's your favorite color?",
            choices={
                "red": "Red", # or _("Red") for translation
                "green": "Green",
                "blue": "Blue",
            },
        )
        ```
    """

    def __init__(self, choices: Dict[str, str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices
        self.view = "RADIOS"


class ButtonArrayQuestion(Question):
    """A question with a button array.

    Args:
        choices (Dict[str, str]): Available options
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = ButtonArrayQuestion(
            key="color",
            question="What's your favorite color?",
            choices={
                "red": "Red", # or _("Red") for translation
                "green": "Green",
                "blue": "Blue",
            },
        )
        ```
    """

    def __init__(self, choices: Dict[str, str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices
        self.view = "BUTTON_ARRAY"


class RangeQuestion(Question):
    """A question with a range slider.

    Args:
        min_value (int): Minimum value
        max_value (int): Maximum value
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = RangeQuestion(
            key="age",
            question="How old are you?",
            min_value=18,
            max_value=120,
        )
        ```
    """

    def __init__(self, min_value: int, max_value: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value


LikertView = Literal["TEXT_RANGE", "ICON_RANGE"]


class LikertQuestion(Question):
    """A question with a Likert scale.

    Args:
        scale_steps (int): Number of scale steps (default: 7)
        explainer (str): Additional instructions for the question
        likert_view (LikertView): Likert scale view (default: 'TEXT_RANGE')
        choices (Dict[int, str]): Custom Likert scale labels
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = LikertQuestion(
            key="satisfaction",
            question="How satisfied are you with the service?",
            explainer="Please rate your satisfaction.",
            scale_steps=5,
            likert_view="TEXT_RANGE",
        )
        ```
    """

    def __init__(
        self,
        scale_steps: int = 7,
        explainer: str = _("How much do you agree or disagree?"),
        likert_view: LikertView = "TEXT_RANGE",
        choices: Dict[int, str] = {},
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.view = likert_view
        self.scoring_rule = "LIKERT"
        self.scale_steps = scale_steps
        self.explainer = explainer

        if choices:
            self.choices = choices
            self.scale_steps = len(self.choices)
        else:
            if scale_steps == 7:
                self.choices = {
                    1: _("Completely Disagree"),
                    2: _("Strongly Disagree"),
                    3: _("Disagree"),
                    4: _("Neither Agree nor Disagree"),  # Undecided
                    5: _("Agree"),
                    6: _("Strongly Agree"),
                    7: _("Completely Agree"),
                }
            elif scale_steps == 5:
                self.choices = {
                    1: _("Strongly Disagree"),
                    2: _("Disagree"),
                    3: _("Neither Agree nor Disagree"),  # Undecided
                    4: _("Agree"),
                    5: _("Strongly Agree"),
                }


class LikertQuestionIcon(Question):
    """A question with a Likert scale using icons.

    Args:
        scale_steps (int): Number of scale steps (default: 7)
        likert_view (LikertView): Likert scale view (default: 'ICON_RANGE')
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = LikertQuestionIcon(
            key="satisfaction",
            question="How satisfied are you with the service?",
            scale_steps=5,
            likert_view="ICON_RANGE",
        )
        ```
    """

    def __init__(self, scale_steps: int = 7, likert_view: LikertView = "ICON_RANGE", **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = likert_view
        if scale_steps == 7:
            self.choices = {
                1: "fa-face-grin-hearts",
                2: "fa-face-grin",
                3: "fa-face-smile",
                4: "fa-face-meh",  # Undecided
                5: "fa-face-frown",
                6: "fa-face-frown-open",
                7: "fa-face-angry",
            }
            self.style = self._apply_style([ColorScheme.GRADIENT_7])


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
                question="What's your name?",
                explainer="Please enter your full name.",
            ),
            BooleanQuestion(
                key="is_student",
                question="Are you a student?",
            ),
        ])
        ```
    """

    def __init__(
        self,
        form: List[Question],
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
