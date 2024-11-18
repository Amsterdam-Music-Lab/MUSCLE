import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput
from django.contrib.postgres.forms import SimpleArrayField
from .models import Image, TARGET_CHOICES


class SVGAndImageFormField(forms.FileField):
    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return None

        # Check for valid image extensions including SVG and WEBP
        valid_image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"]
        ext = os.path.splitext(f.name)[1].lower()

        if ext not in valid_image_extensions:
            raise ValidationError(f"Unsupported file extension: {ext}. Please upload a valid image file.")

        return f


class SVGAndImageInput(ClearableFileInput):
    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if isinstance(upload, list):
            upload = upload[0]
        return upload


class ImageAdminForm(forms.ModelForm):
    file = SVGAndImageFormField(
        widget=SVGAndImageInput, help_text="Upload an image file (supported formats: JPG, JPEG, PNG, GIF, SVG, WEBP)"
    )

    title = forms.CharField(
        max_length=255, help_text="A descriptive title for the image that will be used for administrative purposes"
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text="A detailed description of the image content - useful for content management",
    )

    alt = forms.CharField(
        max_length=255,
        required=False,
        help_text="Alternative text that describes the image - important for accessibility and SEO. "
        "This text is displayed if the image fails to load and is read by screen readers.",
    )

    href = forms.URLField(
        required=False,
        help_text="The URL where the image should link to when clicked. "
        "Leave empty if the image should not be clickable.",
    )

    rel = forms.CharField(
        max_length=255,
        required=False,
        help_text='The relationship attribute for the link (e.g., "nofollow" for SEO, '
        '"noopener noreferrer" for security when linking to external sites)',
    )

    target = forms.ChoiceField(
        choices=TARGET_CHOICES,
        required=False,
        help_text="Specifies where to open the linked URL:\n"
        "- Self: Opens in the same window/tab\n"
        "- Blank: Opens in a new window/tab\n"
        "- Parent: Opens in the parent frame\n"
        "- Top: Opens in the full body of the window",
    )

    tags = SimpleArrayField(
        forms.CharField(max_length=255),
        required=False,
        delimiter=",",
        help_text='Comma-separated tags to categorize and filter images (e.g., "header,banner,promotional")',
    )

    class Meta:
        model = Image
        fields = "__all__"
