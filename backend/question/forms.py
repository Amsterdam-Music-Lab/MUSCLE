from django.forms import ModelForm, ValidationError, ChoiceField, BaseInlineFormSet


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('instance') is None:
            
            self.fields['type'].help_text = "Click 'Save and continue editing' to customize"

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

