import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput
from django.contrib.postgres.forms import SimpleArrayField
from .models import Image


class SVGAndImageFormField(forms.FileField):
    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return None

        # Check for valid image extensions including SVG and WEBP
        valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']
        ext = os.path.splitext(f.name)[1].lower()

        if ext not in valid_image_extensions:
            raise ValidationError(f'Unsupported file extension: {ext}. Please upload a valid image file.')

        return f


class SVGAndImageInput(ClearableFileInput):
    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if isinstance(upload, list):
            upload = upload[0]
        return upload


class ImageAdminForm(forms.ModelForm):
    file = SVGAndImageFormField(widget=SVGAndImageInput)

    tags = SimpleArrayField(
        forms.CharField(max_length=255),
        required=False,
        delimiter=',',
    )

    class Meta:
        model = Image
        fields = '__all__'
