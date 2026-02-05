""" Types of questions to be presented to participants """
from typing import Any, List, Optional, TypedDict

from experiment.actions.base_action import BaseAction
from theme.styles import ColorScheme

class QuestionAction(BaseAction):
    """
    A base object for question actions. Do not use direcly, use subtypes instead.

    Args:
        key: a unique key with which the question is logged to the database
        result_id: the identifier of the `Result` object associated with this question
        text: the text shown to the user
        explainer: optionally, an instruction for the user of how to use the shown widget
        style: list of style classes for display in the frontend
        scoring_rule: the scoring rule with which to score the user's response
        view: the view (widget) shown to the user, set in the subclasses
    """

    def __init__(
        self,
        key: str,
        result_id: int = None,
        text: str = '',
        explainer: str = '',
        style: list[str] = [],
        view: str = '',
    ):
        self.key = key
        self.text = text
        self.result_id = result_id
        self.explainer = explainer
        self.style = self._apply_style(style)
        self.view = view


class Choice(TypedDict):
    """The structure of the dictionary for a question choice
    Note that color (optional) is only shown in ButtonArrayQuestion and IconRangeQuestion
    """

    value: str
    label: str
    color: Optional[str]


class ChoiceQuestionAction(QuestionAction):
    """An action class with choices

    Args:
        choices (dict): a dictionary of answer options
        min_values: the minimal number of options to be selected by user
    """

    def __init__(
        self,
        choices: List[Choice],
        min_values: Optional[int] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.choices = choices
        self.min_values = min_values


class OpenQuestionAction(QuestionAction):
    """A question class showing a text / number or range field

    Args:
        min_value: minimum value (for number / range questions)
        max_value: maximum value (for number / range questions)
        max_length: maximum number of characters (for text questions)
    """

    def __init__(
        self,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        max_length: Optional[int] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.max_length = max_length


class AutoCompleteQuestion(ChoiceQuestionAction):
    """A question with an autocomplete input.

    Args:
        choices (dict): dictionary of answer options
        **kwargs: additional Question arguments

    Example:
        ```python
        question = AutoCompleteQuestion(
            key="color",
            text="What's your favorite color?",
            choices=[
                {"value": "red", "label": "Red"},
                {"value": "green", "label": "Green"},
                {"value": "blue", "label": "Blue"},
            ],
        )
        ```
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(view='AUTOCOMPLETE', **kwargs)


class ButtonArrayQuestion(ChoiceQuestionAction):
    """A question showing buttons for each choice.
    If choices specify color values from the theme, buttons will be colored.
    Not practical to use for more than 5 choices.

    Args:
        choices (List[Choice]): list of dictionaries with value, label and optional color for choice
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = ButtonArrayQuestion(
            key="is_student",
            text="Are you a student?",
            choices=[
                {"value": "no", "label": _("Nope"), "color": "colorNegative"},
                {"value": "yes", "label": _("Yep"), "color": "colorPositive"}
            ],
        )
        ```
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(view="BUTTON_ARRAY", **kwargs)


class CheckBoxQuestion(ChoiceQuestionAction):
    """A question with (multiple) choice options represented as check boxes

    Args:
        choices (List[Choice]): Available options
        min_values (int): Minimum number of selections required
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = MultipleChoiceQuestion(
            key="color",
            text="What's your favorite color?",
            choices=[
                {"value": "red", "label": "Red"},
                {"value": "green", "label": "Green"},
                {"value": "blue": "label": "Blue"}
            ],
            min_values=1,
        )
        ```
    """

    def __init__(self, min_values: int = 1, **kwargs: Any) -> None:
        if min_values < 1:
            raise ValueError("min_values should be at least 1")
        super().__init__(view="CHECKBOXES", min_values=min_values, **kwargs)

    def action(self):
        return {**super().action(), 'min_values': self.min_values}


class DropdownQuestion(ChoiceQuestionAction):
    """A question with a dropdown menu.

    Args:
        choices (List[Choice]): Available options
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = DropdownQuestion(
            key="color",
            text="What's your favorite color?",
            choices=[
                {"value": "red", "label": "Red"},
                {"value": "green", "label": "Green"},
                {"value": "blue", "label": "Blue"},
            ],
        )
        ```
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(view="DROPDOWN", **kwargs)


class IconRangeQuestion(ChoiceQuestionAction):
    """A question showing a range slider with icons.

    Args:
        choices (dict): dictionary of answer options, the values identify icons

    Example:
        ```python
        question = IconRangeQuestion(
            key="satisfaction",
            text="How satisfied are you with the service?",
            choices=[
                {"value": 1, "label": "fa-face-smile"},
                {"value": 2, "label": "fa-face-meh"},
                {"value": 3, "label": "fa-face-frown"}
            [
        )
        ```
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(view="ICON_RANGE", **kwargs)
        self.style = self._apply_style([ColorScheme.GRADIENT_7])


class NumberQuestion(OpenQuestionAction):
    """A question showing numeric input.

    Args:
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        **kwargs: Additional Question arguments
    """

    def __init__(
        self,
        min_value: int = 0,
        max_value: int = 120,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            min_value=min_value, max_value=max_value, view="NUMBER", **kwargs
        )


class RadiosQuestion(ChoiceQuestionAction):
    """A question with radio buttons.

    Args:
        choices (List[Choice]): Available options
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = RadiosQuestion(
            key="color",
            text="What's your favorite color?",
            choices=[
                {"value": "red", "label": "Red"},
                {"value": "green", "label": "Green"},
                {"value": "blue", "label": "Blue"},
            ],
        )
        ```
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(view = "RADIOS", **kwargs)


class RangeQuestion(OpenQuestionAction):
    """A question with a range slider.

    Args:
        min_value: Minimum value
        max_value: Maximum value
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = RangeQuestion(
            key="age",
            text="How old are you?",
            min_value=18,
            max_value=120,
        )
        ```
    """

    def __init__(self, min_value: int = 0, max_value: int = 0, **kwargs: Any) -> None:
        super().__init__(
            min_value=min_value, max_value=max_value, view='RANGE', **kwargs
        )


class TextRangeQuestion(ChoiceQuestionAction):
    """A question with a slider, usually used for a Likert scale.

    Args:
        choices (List[Choice]): list of answer options
        **kwargs: Additional Question arguments

    Example:
        ```python
        question = TextRangeQuestion(
            key="satisfaction",
            text="How satisfied are you with MUSCLE?",
            explainer="Please rate your satisfaction.",
            choices=[
                {"value": 1, "label": _("Very satisfied")},
                {"value": 2, "label": _("Satisfied")},
                {"value": 3, "label": _("Neutral")},
                {"value": 4, "label": _("Disappointed")},
                {"value": 5, "label": _("Very disappointed)}
            ]
        )
        ```
    """

    def __init__(self, **kwargs: Any):
        super().__init__(view='TEXT_RANGE', **kwargs)


class TextQuestion(OpenQuestionAction):
    """A question that accepts text input.

    Args:
        max_length: Maximum character length
        **kwargs: Additional Question arguments
    """

    def __init__(self, max_length: int = 64, **kwargs: Any) -> None:
        super().__init__(max_length=max_length, view="STRING", **kwargs)
