from django import forms
from .models import ThemeConfig


class ThemeConfigForm(forms.ModelForm):

    class Meta:
        model = ThemeConfig
        fields = '__all__'

    class Media:
        js = ['font_preview.js']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field.startswith('color'):
                self.fields[field].widget = forms.TextInput(attrs={'type': 'color'})

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance
