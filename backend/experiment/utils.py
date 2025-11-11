from io import BytesIO
from os.path import join
import roman
from zipfile import ZipFile

from django.db.models.query import QuerySet
from django.core import serializers
from django.http import HttpResponse
from django.utils import timezone

from experiment.models import Experiment, Block, Feedback
from result.models import Result
from participant.models import Participant
from section.models import Song, Section
from session.models import Session

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


def get_participants_of_sessions(sessions: QuerySet[Session]) -> QuerySet[Participant]:
    return Participant.objects.filter(session__in=sessions)


def get_results_of_sessions(sessions: QuerySet[Session]) -> QuerySet[Result]:
    return Result.objects.filter(session__in=sessions)


def get_profiles_of_participants(
    participants: QuerySet[Participant],
) -> QuerySet[Result]:
    return Result.objects.filter(participant__in=participants)


def block_export_json_results(block_slug: str) -> ZipFile:
    """Export block JSON data as zip archive"""

    this_block = Block.objects.get(slug=block_slug)
    all_feedback = Feedback.objects.filter(block=this_block)

    # Collect data
    all_sessions = this_block.associated_sessions().order_by("pk")
    all_results = get_results_of_sessions(all_sessions)
    all_participants = get_participants_of_sessions(all_sessions)
    all_profiles = get_profiles_of_participants(all_participants)
    all_sections = Section.objects.filter(playlist__in=this_block.playlists.all())
    all_songs = Song.objects.filter(section__in=all_sections)

    # create empty zip file in memory
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as new_zip:
        # serialize data to new json files within the zip file
        new_zip.writestr(
            "sessions.json", data=str(serializers.serialize("json", all_sessions))
        )
        new_zip.writestr(
            "participants.json",
            data=str(serializers.serialize("json", all_participants)),
        )
        new_zip.writestr(
            "profiles.json",
            data=str(
                serializers.serialize(
                    "json", all_profiles.order_by("participant", "pk")
                )
            ),
        )
        new_zip.writestr(
            "results.json",
            data=str(serializers.serialize("json", all_results.order_by("session"))),
        )
        new_zip.writestr(
            "sections.json",
            data=str(
                serializers.serialize("json", all_sections.order_by("playlist", "pk"))
            ),
        )
        new_zip.writestr(
            "songs.json",
            data=str(serializers.serialize("json", all_songs.order_by("pk"))),
        )
        new_zip.writestr(
            "feedback.json",
            data=str(serializers.serialize("json", all_feedback.order_by("pk"))),
        )
    return zip_buffer


def get_block_json_export_as_repsonse(block_slug: str):
    '''Create a download response for the admin experimenter dashboard'''
    zip_buffer = block_export_json_results(block_slug)
    response = HttpResponse(zip_buffer.getbuffer())
    response["Content-Type"] = "application/x-zip-compressed"
    response["Content-Disposition"] = (
        'attachment; filename="'
        + block_slug
        + "-"
        + timezone.now().isoformat()
        + '.zip"'
    )
    return response
