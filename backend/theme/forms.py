from django import forms
from .models import ThemeConfig
from experiment.forms import MarkdownPreviewTextInput


class ThemeConfigForm(forms.ModelForm):

    class Meta:
        model = ThemeConfig
        fields = '__all__'

    class Media:
        js = ['font_preview.js']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance

