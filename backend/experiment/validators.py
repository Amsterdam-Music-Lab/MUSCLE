from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

valid_extensions = ['md', 'html']


def markdown_html_validator():
    return FileExtensionValidator(allowed_extensions=valid_extensions)


def block_slug_validator(value):

    disallowed_slugs = [
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

    # Slug cannot start with a disallowed slug
    for slug in disallowed_slugs:
        if value.lower().startswith(slug):
            raise ValidationError(f'The slug cannot start with "{slug}".')

    # Slugs must be lowercase
    if value.lower() != value:
        raise ValidationError('Slugs must be lowercase.')


# This is the validator that is used in the migration file
experiment_slug_validator = block_slug_validator
