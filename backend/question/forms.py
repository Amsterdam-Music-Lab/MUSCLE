from django.forms import ChoiceField, ModelForm, TextInput

from question.models import Question, QuestionInList, QuestionList
from question.banks import PRESET_BANKS

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

QUESTION_BANK_CHOICES = [(None, '-----')] + [(key, key) for key in PRESET_BANKS.keys()]


class QuestionListForm(ModelForm):
    questions_from_bank = ChoiceField(
        choices=QUESTION_BANK_CHOICES,
        initial=None,
        required=False,
        label="Add all questions from a question bank",
    )

    class Meta:
        model = QuestionList
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=commit)
        bank_key = self.cleaned_data.get('questions_from_bank')
        if bank_key:
            instance.save()
            self.add_questions_from_bank(instance, bank_key)
        return instance

    def add_questions_from_bank(self, instance, bank_key: str):
        '''Add all questions from the given bank'''
        n_questions_in_list = QuestionInList.objects.filter(
            questionlist=instance
        ).count()
        for index, key in enumerate(PRESET_BANKS.get(bank_key)):
            question_obj = Question.objects.get(key=key)
            QuestionInList.objects.bulk_create(
                [
                    QuestionInList(
                        questionlist=instance,
                        question=question_obj,
                        index=index + n_questions_in_list,
                    )
                ],
                ignore_conflicts=True,
            )
