from django.forms import ModelForm, TextInput

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
