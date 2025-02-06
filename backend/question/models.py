from django.db import models
from experiment.models import Block


class Question(models.Model):
    """A model that refers to a built-in or customized question"""

    key = models.SlugField(primary_key=True, max_length=128)
    question = models.CharField(max_length=1024)
    editable = models.BooleanField(default=True, editable=False)

    explainer=models.TextField(blank=True, default="")

    TYPES = [
        ("", "---------"),
        ("BooleanQuestion", "BooleanQuestion"),
        ("ChoiceQuestion", "ChoiceQuestion"),
        ("NumberQuestion", "NumberQuestion"),
        ("TextQuestion", "TextQuestion"),
        ("LikertQuestion", "LikertQuestion"),
        ("LikertQuestionIcon", "LikertQuestionIcon"),
        ("AutoCompleteQuestion", "AutoCompleteQuestion"),
    ]
    type = models.CharField(max_length=128, default="", choices=TYPES)

    SCALE_STEPS = [(5,5),(7,7)]
    scale_steps = models.IntegerField(choices=SCALE_STEPS, default=7)

    PROFILE_SCORING_RULES = [
        ("LIKERT", "LIKERT"),
        ("REVERSE_LIKERT", "REVERSE_LIKERT"),
        ("CATEGORIES_TO_LIKERT", "CATEGORIES_TO_LIKERT"),
    ]
    profile_scoring_rule = models.CharField(blank = True, max_length=128,  default="", choices=PROFILE_SCORING_RULES)

    # NumberQuestion
    min_value = models.FloatField(default=0)
    max_value = models.FloatField(default=120)

    # TextQuestion
    max_length = models.IntegerField(default=64)

    # ChoiceQuestion
    min_values = models.IntegerField(default=1)
    VIEWS = [
        ("BUTTON_ARRAY", "BUTTON_ARRAY"),
        ("CHECKBOXES", "CHECKBOXES"),
        ("RADIOS", "RADIOS"),
        ("DROPDOWN", "DROPDOWN"),
    ]
    view = models.CharField(max_length=128, default="", choices=VIEWS)

    is_skippable = models.BooleanField(default=False)

    def __str__(self):
        return "(" + self.key + ") " + self.question

    class Meta:
        ordering = ["key"]


class Choice(models.Model):

    key = models.SlugField(max_length=128)
    text = models.CharField()
    index = models.PositiveIntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        ordering = ["index"]


class QuestionGroup(models.Model):
    """Convenience model for groups of questions to add at once to Block QuestionSeries from admin"""

    key = models.CharField(primary_key=True, max_length=128)
    questions = models.ManyToManyField(Question)
    editable = models.BooleanField(default=True, editable=False)

    class Meta:
        ordering = ["key"]
        verbose_name_plural = "Question Groups"

    def __str__(self):
        return self.key


class QuestionSeries(models.Model):
    """Series of Questions asked in a Block"""

    name = models.CharField(default="", max_length=128)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()  # index of QuestionSeries within Block
    questions = models.ManyToManyField(Question, through="QuestionInSeries")
    randomize = models.BooleanField(default=False)  # randomize questions within QuestionSeries

    class Meta:
        ordering = ["index"]
        verbose_name_plural = "Question Series"

    def __str__(self):
        return "QuestionSeries object ({}): {} questions".format(self.id, self.questioninseries_set.count() if self.pk else 0)


class QuestionInSeries(models.Model):
    """Question with its index in QuestionSeries"""

    question_series = models.ForeignKey(QuestionSeries, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    index = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("question_series", "question")
        ordering = ["index"]
        verbose_name_plural = "Question In Series objects"
