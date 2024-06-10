from os.path import join

from django.conf import settings

from .models import Image


def serialize_image(image: Image) -> dict:
    return {
        'file': join(settings.MEDIA_URL, str(image.file)),
        'href': image.href,
        'alt': image.alt,
    }
