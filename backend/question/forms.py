from django.forms import ModelForm, ValidationError, ChoiceField, BaseInlineFormSet


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            type_choices = [('', '---')] + self.fields['type'].choices
            self.fields['type'].choices = type_choices

    class Meta:
        help_texts = {
            "min_value": "The minimum number allowed in the Number / Range question",
            "max_value": "The maximum number allowed in the Number / Range question",
            "min_values": "How many options should be selected by participant in the Checkbox question",
            "max_length": "The maximum number of characters allowed in the Text question",
        }
