from os.path import join

from django.conf import settings

from .models import Image


def serialize_image(image: Image) -> dict:
    """serialize an Image object

    Args:
        image: the image to serialize
    """
    return {
        'file': f'{settings.BASE_URL.strip("/")}/{settings.MEDIA_URL.strip("/")}/{image.file}',
        'href': image.href,
        'alt': image.alt,
        'rel': image.rel,
        'target': image.target,
        'tags': image.tags,
        'title': image.title,
        'description': image.description,
    }
