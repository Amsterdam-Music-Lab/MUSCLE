from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from .validators import validate_image_file

TARGET_CHOICES = (
    ("_self", "Self"),
    ("_blank", "Blank"),
    ("_parent", "Parent"),
    ("_top", "Top"),
)


class SVGAndImageFieldFile(ImageFieldFile):
    """
    Custom file field to handle SVG and standard image files that inherit from Django's ImageFieldFile.
    """

    def save(self, name, content, save=True):
        if isinstance(content, UploadedFile) and (content.content_type == "image/svg+xml" or name.endswith(".svg")):
            name = default_storage.save(name, content)
            self.name = name
            self._committed = True
        else:
            super().save(name, content, save)


class SVGAndImageField(models.ImageField):
    """
    Custom ImageField that uses SVGAndImageFieldFile that inherits from Django's ImageField.
    """

    attr_class = SVGAndImageFieldFile


class Image(models.Model):
    """
    Model representing an image with various attributes.

    Args:
        file (SVGAndImageField): The uploaded image file.
        title (str): The title of the image.
        description (str): A description of the image.
        alt (str): Alternative text for the image. Used for accessibility (e.g., screen readers).
        href (str): Optional URL that the image links to. If provided, the image will be wrapped in an anchor tag in the frontend.
        rel (str): Relationship attribute for the link. Used to specify the relationship between the current document and the linked document.
        target (str): Specifies where to open the linked document. Most common values are "_self" (open in the same frame) and "_blank" (open in a new window).
        tags (List[str]): Tags associated with the image.
        created_at (datetime): Timestamp when the image was created. Automatically set when the image is created.
        updated_at (datetime): Timestamp when the image was last updated. Automatically set when the image is updated.

    Example:
        ```python
        image = Image(
            file=uploaded_file,
            title="Sample Image",
            description="A sample image description.",
            alt="Alt text for sample image",
            href="https://example.com",
            rel="noopener",
            target="_blank",
            tags=["sample", "image"],
        )
    """

    file = SVGAndImageField(upload_to="%Y/%m/%d/", validators=[validate_image_file], help_text="Uploaded image file.")
    title = models.CharField(max_length=255, help_text="Title of the image.")
    description = models.TextField(blank=True, default="", help_text="Description of the image.")
    alt = models.CharField(max_length=255, blank=True, default="", help_text="Alternative text for the image.")
    href = models.URLField(blank=True, default="", help_text="URL that the image links to.")
    rel = models.CharField(max_length=255, blank=True, default="", help_text="Relationship attribute for the link.")
    target = models.CharField(
        max_length=255,
        blank=True,
        choices=TARGET_CHOICES,
        default=TARGET_CHOICES[0],
        help_text="Specifies where to open the linked document.",
    )
    tags = ArrayField(
        models.CharField(max_length=255), blank=True, default=list, help_text="Tags associated with the image."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the image was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the image was last updated.")

    def __str__(self):
        return self.title or self.file.name or self.alt or "Image"
