from django.core.validators import FileExtensionValidator

valid_extensions = ['md', 'html']


def consent_file_validator():
    return FileExtensionValidator(allowed_extensions=valid_extensions)
