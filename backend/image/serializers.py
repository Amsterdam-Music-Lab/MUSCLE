from os.path import join

from django.conf import settings

from .models import Image


def serialize_image(image: Image) -> dict:
    return {
        'file': f'{settings.BASE_URL.strip("/")}/{settings.MEDIA_URL.strip("/")}/{image.file}',
        'href': image.href,
        'alt': image.alt,
    }
