from typing import List, Tuple
import roman
from os.path import join

from experiment.models import Experiment, Phase, Block, BlockTranslatedContent


def slugify(text: str) -> str:
    """Create a slug from given string

    Args:
        text: Input text (str)

    Returns:
        slug
    """

    non_url_safe = [
        '"',
        "#",
        "$",
        "%",
        "&",
        "+",
        ",",
        "/",
        ":",
        ";",
        "=",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "`",
        "{",
        "|",
        "}",
        "~",
        "'",
    ]
    translate_table = {ord(char): "" for char in non_url_safe}
    text = text.translate(translate_table)
    text = "_".join(text.split())
    return text.lower()


def non_breaking_spaces(input_string: str) -> str:
    """Convert regular spaces to non breaking spacing on the given string
    Args:
        input_string: Input string

    Returns:
        String with non breaking spaces
    """

    non_breaking_space = chr(160)
    return input_string.replace(" ", non_breaking_space)


def external_url(text: str, url) -> str:
    """Create a HTML element for an external url

    Args:
        text: Text
        url: Url

    Returns:
        HTML element
    """

    return '<a href="{}" target="_blank" rel="noopener noreferrer" >{}</a>'.format(url, text)


def create_player_labels(num_labels: int, label_style: str = "number") -> list[str]:
    """Create player labels

    Args:
        num_labels: Number of labels
        label_style: 'number', 'alphabetic', 'roman'

    Returns:
        Player label
    """

    return [format_label(i, label_style) for i in range(num_labels)]


def format_label(number: int, label_style: str) -> str:
    """Generate player_label for create_player_label()

    Args:
        number: index
        label_style: 'number', 'alphabetic', 'roman'

    Returns:
        Player label
    """

    if label_style == "alphabetic":
        return chr(number + 65)
    elif label_style == "roman":
        return roman.toRoman(number + 1)
    else:
        return str(number + 1)


def get_flag_emoji(country_code):
    # If the country code is not provided or is empty, return "Unknown"
    if not country_code:
        return "🏳️"

    # Convert the country code to uppercase
    country_code = country_code.upper()

    # Calculate the Unicode code points for the flag emoji
    flag_emoji = "".join([chr(127397 + ord(char)) for char in country_code])

    return flag_emoji


def get_missing_content_block(block: Block) -> List[str]:
    block_experiment = block.phase.experiment

    languages = block_experiment.translated_content.values_list("language", flat=True)

    missing_languages = []

    for language in languages:
        block_content = BlockTranslatedContent.objects.filter(block=block, language=language)
        if not block_content:
            missing_languages.append(language)

    return missing_languages


# Returns a list of a tuple containing the Block and a list of missing languages
def get_missing_content_blocks(experiment: Experiment) -> List[Tuple[Block, List[str]]]:
    languages = experiment.translated_content.values_list("language", flat=True)

    associated_phases = Phase.objects.filter(experiment=experiment)
    associated_blocks = Block.objects.filter(phase__in=associated_phases)

    missing_content_blocks = []

    for block in associated_blocks:
        missing_languages = []
        for language in languages:
            block_content = BlockTranslatedContent.objects.filter(block=block, language=language)
            if not block_content:
                missing_languages.append(language)

        if len(missing_languages) > 0:
            missing_content_blocks.append((block, missing_languages))

    return missing_content_blocks


def check_missing_translations(experiment: Experiment) -> str:
    warnings = []

    missing_content_blocks = get_missing_content_blocks(experiment)

    for block, missing_languages in missing_content_blocks:
        missing_language_flags = [get_flag_emoji(language) for language in missing_languages]
        warnings.append(f"Block {block.slug} does not have content in {', '.join(missing_language_flags)}")

    warnings_text = "\n".join(warnings)

    return warnings_text


def consent_upload_path(instance: Experiment, filename: str) -> str:
    """Generate path to save consent file based on experiment.slug and language

    Args:
        instance: Experiment instance to determine folder name
        filename: Name of the consent file to be uploaded

    Returns:
        upload_to: Path for uploading the consent file

    Note:
        Used by the Block model for uploading consent file
    """
    experiment = instance.experiment
    folder_name = experiment.slug
    language = instance.language

    join("consent", folder_name, f"{language}-{filename}")
