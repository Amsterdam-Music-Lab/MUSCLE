from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from .models import ThemeConfig


class ThemeConfigForm(forms.ModelForm):

    class Meta:
        model = ThemeConfig
        fields = '__all__'

    class Media:
        js = ['img_preview.js', 'font_preview.js']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance
