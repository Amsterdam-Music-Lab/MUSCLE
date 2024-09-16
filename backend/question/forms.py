from django.forms import ModelForm, ValidationError, ChoiceField, BaseInlineFormSet


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('instance') is None:
            
            self.fields['type'].help_text = "Click 'Save and view' to customize"

        else:

            if not kwargs.get('instance').editable:
                self.fields["key"].disabled = True

            type = self.fields.get("type", None)
            if type:
                self.fields["type"].disabled = True

    class Meta:
        help_texts = {
            "scale_steps" : "Non-empty choices field overrides this value",
            "min_values" : "Only affects CHECKBOXES view"
        }
   

class ChoiceInlineFormset(BaseInlineFormSet):

    def clean(self):

        choices_n = len(self.cleaned_data)
        deletes_n = 0

        for choice in self.cleaned_data:
            if choice['DELETE']:
                deletes_n += 1

        if choices_n == 0 or (choices_n == deletes_n):
            raise ValidationError('Choices cannot be empty!')
