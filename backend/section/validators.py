from django.core.validators import FileExtensionValidator

audio_extensions = ['wav', 'mp3', 'aiff', 'flac', 'ogg']


def audio_file_validator():
    return FileExtensionValidator(allowed_extensions=audio_extensions)
