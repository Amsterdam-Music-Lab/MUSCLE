from os.path import join

from django.conf import settings

from .models import Image


def serialize_image(image: Image) -> dict:
    return {
        'file': join(settings.MEDIA_URL, settings.SUBPATH, str(image.file)),
        'href': image.href,
        'alt': image.alt,
    }
