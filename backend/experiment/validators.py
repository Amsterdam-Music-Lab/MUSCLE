from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

valid_extensions = ['md', 'html']


def consent_file_validator():
    return FileExtensionValidator(allowed_extensions=valid_extensions)


def experiment_slug_validator(value):
    
    disallowed_slugs = [
        'admin',
        'server',
        'experiment',
        'participant',
        'result',
        'section',
        'session',
        'static',
    ]

    # Slugs must not be in the disallowed list
    if value in disallowed_slugs:
        raise ValidationError(f'The slug "{value}" is not allowed.')

    # Slugs must be lowercase    
    if value.lower() != value:
        raise ValidationError('Slugs must be lowercase.')
