from typing import List, Tuple
import roman
from django.utils.html import format_html
from django.db.models.query import QuerySet
from experiment.models import Experiment, Phase, Block, BlockTranslatedContent


def slugify(text):
    """Create a slug from given string"""
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


def non_breaking_spaces(s):
    # Convert regular spaces to non breaking spacing
    # on the given string
    non_breaking_space = chr(160)
    return s.replace(" ", non_breaking_space)


def external_url(text, url):
    # Create a HTML element for an external url
    return '<a href="{}" target="_blank" rel="noopener noreferrer" >{}</a>'.format(url, text)


def create_player_labels(num_labels, label_style="number"):
    return [format_label(i, label_style) for i in range(num_labels)]


def format_label(number, label_style):
    if label_style == "alphabetic":
        return chr(number + 65)
    elif label_style == "roman":
        return roman.toRoman(number + 1)
    else:
        return str(number + 1)


def get_flag_emoji(country_code):
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

        if missing_languages:
            missing_content_blocks.append((block, missing_languages))

    return missing_content_blocks


def check_missing_translations(experiment: Experiment) -> str:
    warnings = []

    missing_content_blocks = get_missing_content_blocks(experiment)
    for block, missing_languages in missing_content_blocks:
        missing_language_flags = [get_flag_emoji(language) for language in missing_languages]
        warnings.append(f"Block {block.name} does not have content in {', '.join(missing_language_flags)}")

    warnings_text = "\n".join(warnings)

    print(warnings_text)

    return warnings_text
