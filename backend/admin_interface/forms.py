
from django import forms
from .models import AdminInterfaceConfiguration


class AdminInterfaceConfigurationForm(forms.ModelForm):

    class Meta:
        model = AdminInterfaceConfiguration
        fields = '__all__'

