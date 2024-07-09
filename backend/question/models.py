from django.db import models
from experiment.models import Block


class Question(models.Model):
    """A model that (currently) refers to a built-in question"""

    key = models.CharField(primary_key=True, max_length=128)
    question = models.CharField(max_length=1024)
    editable = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return "("+self.key+") "+ self.question

    class Meta:
        ordering = ["key"]


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
    """Series of Questions asked in an Block"""

    name = models.CharField(default='', max_length=128)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    index = models.PositiveIntegerField() # index of QuestionSeries within Block
    questions = models.ManyToManyField(Question, through='QuestionInSeries')
    randomize = models.BooleanField(default=False) # randomize questions within QuestionSeries

    class Meta:
        ordering = ["index"]
        verbose_name_plural = "Question Series"

    def __str__(self):
        return "QuestionSeries object ({}): {} questions".format(self.id, self.questioninseries_set.count())


class QuestionInSeries(models.Model):
    """Question with its index in QuestionSeries"""

    question_series = models.ForeignKey(QuestionSeries, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    class Meta:
        unique_together = ('question_series', 'question')
        ordering = ["index"]
        verbose_name_plural = "Question In Series objects"
