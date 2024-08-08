from urllib.parse import urljoin
from django.conf import settings

from .models import Image


def serialize_image(image: Image) -> dict:   
    return {
        'file': urljoin(settings.BASE_URL, image.file.url),
        'href': image.href,
        'alt': image.alt,
        'rel': image.rel,
        'target': image.target,
        'tags': image.tags,
        'title': image.title,
        'description': image.description,
    }
