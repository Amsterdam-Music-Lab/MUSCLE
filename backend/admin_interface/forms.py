
from django import forms
from .models import AdminInterfaceConfiguration


class AdminInterfaceConfigurationForm(forms.ModelForm):

    class Meta:
        model = AdminInterfaceConfiguration
        fields = '__all__'


class AdminInterfaceThemeConfigurationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget = forms.TextInput(attrs={'type': 'color'})