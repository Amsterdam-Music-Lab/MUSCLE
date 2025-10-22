from django.forms import ChoiceField, ModelForm, TextInput

from question.models import Question, QuestionInSeries, QuestionSeries
from question.preset_catalogues import PRESET_CATALOGUES

class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            type_choices = [('', '---')] + self.fields['type'].choices
            self.fields['type'].choices = type_choices
        else:
            if self.instance.from_python:
                [
                    setattr(self.fields[field_name], 'disabled', True)
                    for field_name in self.fields.keys()
                ]

    class Meta:
        help_texts = {
            "min_value": "The minimum number allowed in the Number / Range question",
            "max_value": "The maximum number allowed in the Number / Range question",
            "min_values": "How many options should be selected by participant in the Checkbox question",
            "max_length": "The maximum number of characters allowed in the Text question",
        }
        widgets = {'text': TextInput(attrs={'size': '100%'})}

QUESTION_CATALOGUE_CHOICES = [(None, '-----')] + [
    (key, key) for key in PRESET_CATALOGUES.keys()
]

class QuestionSeriesForm(ModelForm):
    questions_from_catalogue = ChoiceField(
        choices=QUESTION_CATALOGUE_CHOICES,
        initial=None,
        required=False,
        label="Add all questions from catalogue",
    )

    class Meta:
        model = QuestionSeries
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=commit)
        catalogue_key = self.cleaned_data.get('questions_from_catalogue')
        if catalogue_key:
            instance.save()
            self.add_questions_from_catalogue(instance, catalogue_key)
        return instance

    def add_questions_from_catalogue(self, instance, catalogue_key):
        '''Add all questions from the given catalogue'''
        n_questions_in_series = QuestionInSeries.objects.filter(
            question_series=instance
        ).count()
        for index, key in enumerate(PRESET_CATALOGUES.get(catalogue_key)):
            question_obj = Question.objects.get(key=key)
            QuestionInSeries.objects.bulk_create(
                [
                    QuestionInSeries(
                        question_series=instance,
                        question=question_obj,
                        index=index + n_questions_in_series,
                    )
                ],
                ignore_conflicts=True,
            )
