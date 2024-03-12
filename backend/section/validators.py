from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


audio_extensions = ['wav', 'mp3', 'aiff', 'flac', 'ogg']


def audio_file_validator():
    return FileExtensionValidator(allowed_extensions=audio_extensions)


def url_prefix_validator(value):
    if value.startswith('http://'):
        pass
    elif value.startswith('https://'):
        pass
    else:
        raise ValidationError(
            ("%(value)s is not a valid URL"),
            params={"value": value},
        )
