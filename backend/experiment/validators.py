from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

valid_extensions = ['md', 'html']


def markdown_html_validator():
    return FileExtensionValidator(allowed_extensions=valid_extensions)


def identifier_validator(value):

    disallowed_identifiers = [
        'admin',
        'server',
        'experiment',
        'participant',
        'result',
        'section',
        'session',
        'static',
        'block',
    ]

    # Identifier cannot start with a disallowed identifier
    for identifier in disallowed_identifiers:
        if value.lower().startswith(identifier):
            raise ValidationError(f'The identifier cannot start with "{identifier}".')

    # Identifiers must be lowercase
    if value.lower() != value:
        raise ValidationError('Identifiers must be lowercase.')
