from django.db import models
from django.conf import settings
from django.utils.translation import activate, gettext_lazy as _

from experiment.actions import question
from experiment.actions.question import QuestionAction

class Question(models.Model):
    """Model for question asked during experiment

    Attributes:
        key (slug): Unique identifier
        question (str): Question text
        editable (bool): False for built-in questions. Key and type of a built-in question cannot be changed.
        explainer (str): Question explainer text
        type (str): Question type {"BooleanQuestion", "ChoiceQuestion", "NumberQuestion", "TextQuestion", "LikertQuestion", "LikertQuestionIcon", "AutoCompleteQuestion"}
        scale_steps (int): Number of scale steps {5, 7} (applies to LikertQuestion, LikertQuestionIcon)
        profile_scoring_rule (str): Profile scoring rule {"", "LIKERT", "REVERSE_LIKERT", "CATEGORIES_TO_LIKERT"} (ChoiceQuestion, LikertQuestion)
        min_value (float): Minimal value (NumberQuestion)
        max_value (float): Maximal value (NumberQuestion)
        max_length (int): Maximal length (TextQuestion)
        min_values (int): Minimum number of values to choose (ChoiceQuestion)
        view (int): Question view {"BUTTON_ARRAY", "CHECKBOXES", "RADIOS", "DROPDOWN"} (ChoiceQuestion)
        is_skippable (bool): If question can be skipped during experiment

    """

    class QuestionTypes(models.TextChoices):
        AUTOCOMPLETE = "AutoCompleteQuestion", _(
            "Autocomplete: Present choices as a dropdown with autocomplete function"
        )
        BUTTON_ARRAY = "ButtonArrayQuestion", _(
            "Button Array: Present choices as a row of buttons"
        )
        CHECKBOXES = "CheckboxQuestion", _(
            "Checkboxes: Present choices as checkboxes (multiple options)"
        )
        DROPDOWN = "DropdownQuestion", _("Dropdown: Present choices in a dropdown menu")
        ICON_RANGE = "IconRangeQuestion", _(
            "Icon Range: Present choices as a range slider with icons"
        )
        RADIOS = "RadiosQuestion", _("Radios: Present choices as radio buttons")
        RANGE = "RangeQuestion", _("Range: Present a range slider to select a number")
        NUMBER = "NumberQuestion", _(
            "Number: Present a number field to select a number"
        )
        STRING = "TextQuestion", _("Text: Present a text field to enter free text")
        TEXT_RANGE = "TextRangeQuestion", _(
            "Text Range: Present choices as a range slider with text"
        )

    key = models.SlugField(primary_key=True, max_length=128)
    text = models.CharField(max_length=1024)
    explainer = models.TextField(blank=True, default="")
    from_python = models.BooleanField(default=False, editable=False)

    type = models.CharField(max_length=32, default="", choices=QuestionTypes.choices)

    PROFILE_SCORING_RULES = [
        ("LIKERT", "LIKERT"),
        ("REVERSE_LIKERT", "REVERSE_LIKERT"),
        ("CATEGORIES_TO_LIKERT", "CATEGORIES_TO_LIKERT"),
    ]
    profile_scoring_rule = models.CharField(
        blank=True, max_length=128, default="", choices=PROFILE_SCORING_RULES
    )

    # only applicable for Number/RangeQuestion
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)

    # only applicable for TextQuestion: maximal length of text
    max_length = models.IntegerField(blank=True, null=True)

    # ChoiceQuestion
    choices = models.ForeignKey(
        'question.ChoiceSet', null=True, on_delete=models.SET_NULL
    )
    # only applicable for CheckBoxQuestion
    min_values = models.IntegerField(blank=True, null=True)

    is_skippable = models.BooleanField(default=False)

    def __str__(self):
        return "(" + self.key + ") " + self.question

    def populate_translated_fields(self, field_name: str):
        _populate_translated_fields(self, field_name)

    def convert_to_action(self) -> QuestionAction:
        question_type = getattr(question, self.type)
        if self.choices:
            choices = self.choices.to_dict()
            question_action = question_type(
                key=self.key, text=self.question, choices=choices
            )
        else:
            question_action = question_type(key=self.key, text=self.question)
        optional_fields = [
            'min_value',
            'max_value',
            'max_length',
            'min_values',
            'is_skippable',
        ]
        [self.set_optional_fields(field, question_action) for field in optional_fields]
        return question_action

    def set_optional_fields(self, field, question_action: QuestionAction):
        if getattr(self, field):
            setattr(question_action, field, getattr(self, field))

    class Meta:
        ordering = ["key"]


class ChoiceSet(models.Model):
    """A collection of choices for a question"""

    key = models.SlugField(max_length=64, primary_key=True)
    from_python = models.BooleanField(default=False, editable=False)

    def to_dict(self):
        return {choice.key: choice.text for choice in self.choices.all()}


class Choice(models.Model):
    """ Choice model for Question with choices

    Attributes:
        key (slug): Unique identifier
        text (str): Choice text
        index (int): Index of choice within Question
        question (Question): Question that contains the Choice

    """

    key = models.SlugField(max_length=128)
    text = models.CharField()
    index = models.PositiveIntegerField(default=0)
    set = models.ForeignKey(
        ChoiceSet,
        on_delete=models.CASCADE,
        related_name='choices',
    )

    class Meta:
        ordering = ["index"]
        unique_together = ["key", "set"]


class QuestionSeries(models.Model):
    """Series of Questions asked in a Block

    Attributes:
        name (str): Name of the QuestionSeries
        block (Block): Block that contains QuestionSeries
        index (int):  Index of QuestionSeries within Block
        questions (Queryset[Question]): ManyToManyField to Questions that the QuestionSeries contains
        randomize (bool): Randomize questions within QuestionSeries
    """

    name = models.CharField(default="", max_length=128)
    block = models.ForeignKey('experiment.Block', on_delete=models.CASCADE)
    index = models.PositiveIntegerField()  # index of QuestionSeries within Block
    questions = models.ManyToManyField(Question, through="QuestionInSeries")
    randomize = models.BooleanField(default=False)  # randomize questions within QuestionSeries

    class Meta:
        ordering = ["index"]
        unique_together = ["name", "block"]
        verbose_name_plural = "Question Series"

    def __str__(self):
        return _(
            "QuestionSeries %(qs_name)s of block with slug %(block_slug)s: %(n_questions)i questions"
        ) % {
            'qs_name': self.name,
            'block_slug': self.block.slug,
            'n_questions': self.questioninseries_set.count() if self.pk else 0,
        }


class QuestionInSeries(models.Model):
    """Question with its index in QuestionSeries

    Attributes:
        question_series (QuestionSeries): QuestionSeries that contains the Question
        question (Question): Question linked to question_series
        index (int): Index of Question within QuestionSeries
    """

    question_series = models.ForeignKey(QuestionSeries, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    index = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("question_series", "question")
        ordering = ["index"]
        verbose_name_plural = "Question In Series objects"


def _populate_translated_fields(obj: models.Model, field_name: str):
    """Check if there are Python-defined translations and fill fields of a Question or Choice object
    Args:
        obj: the Question / Choice object whose fields to set
        field_name: the name of the field (registered in `question.translations`)
    """
    for lang in reversed(settings.MODELTRANSLATION_LANGUAGES):
        lang_field = lang.replace("-", "_")
        activate(lang)
        input_string = getattr(obj, field_name)
        setattr(
            obj,
            f"{field_name}_{lang_field}",
            str(input_string),
        )
