from django.forms import ModelForm, ValidationError, ChoiceField


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('instance') is None:
            
            self.fields['type'].help_text = "Click 'Save and view' to customize"

        else:
            type = self.fields.get("type", None)
            if type:
                self.fields["type"].disabled = True

    def clean_choices(self):

        choices = self.cleaned_data['choices']

        if choices:
            for line in choices.split('\n'):
                if len(line.split(":")) != 2:
                    raise ValidationError("Enter each choice on a separate line as key:text")

        if self.instance.type in ("ChoiceQuestion","AutoCompleteQuestion") and not choices:
            raise ValidationError("Choices cannot be empty")

        return choices

    class Meta:
        help_texts = {
            "choices" : "Enter each choice on a separate line as key:text",
            "scale_steps" : "Non-empty choices field overrides this value",
            "min_values" : "Only affects CHECKBOXES view"
        }
   
