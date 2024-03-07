from django.contrib.postgres.forms import SimpleArrayField
from django import forms
from .models import Image


class ImageAdminForm(forms.ModelForm):

    tags = SimpleArrayField(
        forms.CharField(max_length=255),
        required=False,
        delimiter=',',
    )

    class Meta:
        model = Image
        fields = '__all__'
