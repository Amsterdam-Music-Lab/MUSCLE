from django import forms
from modeltranslation.forms import TranslationModelForm
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


class FooterConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disclaimer'].widget = MarkdownPreviewTextInput()
        self.fields['privacy'].widget = MarkdownPreviewTextInput()
