from io import BytesIO, StringIO
from os.path import join
from typing import Union
from zipfile import ZipFile

from django.db.models.query import QuerySet
from django.db.models import F
from django.core import serializers
from django.http import HttpResponse
from django.utils import timezone
import numpy as np
import pandas as pd
import roman


from experiment.models import Experiment, Block, Feedback
from result.models import Result
from participant.models import Participant
from section.models import Song, Section
from session.models import Session


def non_breaking_spaces(input_string: str) -> str:
    """Convert regular spaces to non breaking spacing on the given string
    Args:
        input_string: Input string

    Returns:
        String with non breaking spaces
    """

    non_breaking_space = chr(160)
    return input_string.replace(" ", non_breaking_space)


def external_url(text: str, url: str) -> str:
    """Create a HTML element for an external url

    Args:
        text: Text
        url: Url

    Returns:
        HTML element
    """

    return '<a href="{}" target="_blank" rel="noopener noreferrer" >{}</a>'.format(url, text)


def format_label(number: int, label_style: str) -> str:
    """Generate a label based on an index and a label style

    Args:
        number: index
        label_style: 'alphabetic', 'roman'

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
    """Generate path to save consent file based on experiment.identifier and language

    Args:
        instance: Experiment instance to determine folder name
        filename: Name of the consent file to be uploaded

    Returns:
        upload_to: Path for uploading the consent file

    Note:
        Used by the Block model for uploading consent file
    """

    experiment = instance.experiment
    folder_name = experiment.identifier
    language = instance.language

    join("consent", folder_name, f"{language}-{filename}")


def get_participants_of_sessions(sessions: QuerySet[Session]) -> QuerySet[Participant]:
    return Participant.objects.filter(sessions__in=sessions)


def get_results_of_sessions(sessions: QuerySet[Session]) -> QuerySet[Result]:
    return Result.objects.filter(session__in=sessions)


def get_profiles_of_participants(
    participants: QuerySet[Participant],
) -> QuerySet[Result]:
    return Result.objects.filter(participant__in=participants)


def block_generate_results_data_frame(block_identifier: str) -> pd.DataFrame:
    """export results and profiles in two csvs
    This export does not provide all data, but a selection of the variables
    expected to be of most interest for basic analyses
    """
    this_block = Block.objects.get(identifier=block_identifier)
    all_sessions = this_block.sessions.order_by("pk")
    all_results = get_results_of_sessions(all_sessions)
    result_output_keys = [
        "session__id",
        "session__final_score",
        "participant__id",
        "participant__country_code",
        "question_identifier",
        "created_at",
        "expected_response",
        "given_response",
        "score",
        "section__id",
        "section__song__name",
        "section__song__artist",
        "section__tag",
        "section__group",
    ]
    results_output = pd.DataFrame(
        list(
            all_results.annotate(participant__id=F("session__participant")).values(
                *result_output_keys
            )
        )
    )
    all_participants = get_participants_of_sessions(all_sessions)
    question_identifiers = []
    question_lists = this_block.questionlist_set.all()
    for ql in question_lists:
        question_identifiers.extend(ql.questions.values_list("identifier", flat=True))
    relevant_profiles = get_profiles_of_participants(all_participants).filter(
        question_identifier__in=question_identifiers
    )
    profile_output_keys = [
        "participant__id",
        "participant__country_code",
        "question_identifier",
        "given_response",
        "score",
    ]
    profiles_output = pd.DataFrame(list(relevant_profiles.values(*profile_output_keys)))
    if profiles_output.empty:
        return results_output
    wide_profiles = profiles_output.pivot(
        index="participant__id",
        columns="question_identifier",
        values=["given_response", "score"],
    )
    wide_profiles.columns = [
        ".".join(map(str, reversed(col)))
        for col in wide_profiles.columns.to_flat_index()
    ]
    wide_profiles = wide_profiles.reset_index()
    if results_output.empty:
        return wide_profiles
    return pd.merge(results_output, wide_profiles, on="participant__id")


def block_export_csv_results(block_identifier: str) -> StringIO:
    csv_buffer = StringIO()
    results_df = block_generate_results_data_frame(block_identifier)
    results_df.to_csv(csv_buffer)
    return csv_buffer.getvalue()


def get_block_csv_export_as_response(block_identifier: str) -> HttpResponse:
    '''Create a download response for the admin experimenter dashboard'''
    csv_string = block_export_csv_results(block_identifier)
    response = HttpResponse(csv_string)
    response["Content-Type"] = "text/csv"
    response["Content-Disposition"] = (
        'attachment; filename="'
        + block_identifier
        + "-"
        + timezone.now().isoformat()
        + '.csv"'
    )
    return response


def experiment_export_csv_results(experiment_identifier: str) -> StringIO:
    experiment = Experiment.objects.get(identifier=experiment_identifier)
    block_identifiers = experiment.associated_blocks().values_list(
        "identifier", flat=True
    )
    data_frames = [
        block_generate_results_data_frame(block_id) for block_id in block_identifiers
    ]
    combination = pd.concat(data_frames)
    if any(combination.section__id):
        # if we have section_ids defined, aggregate data by section_id
        keys_of_interest = [
            "score",
            "given_response",
            "section__id",
            "participant__id",
            "question_identifier",
        ]
        section_data = (
            (
                combination[keys_of_interest]
                .groupby(
                    ["section__id", "question_identifier", "participant__id"],
                    dropna=False,
                )
                .agg(agg_func)
            )
            .unstack("question_identifier")
            .reset_index()
        )
        section_data.columns = [
            ".".join(map(str, reversed(col))).strip(".")
            for col in section_data.columns.to_flat_index()
        ]
        profile_columns = [
            col for col in combination.columns if ".given_response" in col
        ]
        if profile_columns:
            profile_data = combination.dropna(subset=profile_columns, how="all").drop(
                [
                    "question_identifier",
                    "session__id",
                    "session__final_score",
                    "created_at",
                    "given_response",
                    "expected_response",
                    "score",
                ],
                axis=1,
            )
            output = section_data.merge(
                profile_data,
                how="inner",
                on=["participant__id", "section__id"],
            )
        else:
            output = section_data
    else:
        output = combination
    csv_buffer = StringIO()
    output.fillna(value=np.nan).drop_duplicates().to_csv(csv_buffer)
    return csv_buffer.getvalue()


def block_export_csv_results(block_identifier: str) -> StringIO:
    csv_buffer = StringIO()
    results_df = block_generate_results_data_frame(block_identifier)
    results_df.to_csv(csv_buffer)
    return csv_buffer.getvalue()


def get_experiment_csv_export_as_response(experiment_identifier: str) -> HttpResponse:
    '''Create a download response for the admin experimenter dashboard'''
    csv_string = experiment_export_csv_results(experiment_identifier)
    response = HttpResponse(csv_string)
    response["Content-Type"] = "text/csv"
    response["Content-Disposition"] = (
        'attachment; filename="'
        + experiment_identifier
        + "-"
        + timezone.now().isoformat()
        + '.csv"'
    )
    return response


def agg_func(input_value: Union[list, str, int]) -> str:
    """return the first response by a participant"""
    if type(input_value) is pd.Series:
        return input_value.values[0]
    else:
        return input_value


def get_block_csv_export_as_response(block_identifier: str) -> HttpResponse:
    '''Create a download response for the admin experimenter dashboard'''
    csv_string = block_export_csv_results(block_identifier)
    response = HttpResponse(csv_string)
    response["Content-Type"] = "text/csv"
    response["Content-Disposition"] = (
        'attachment; filename="'
        + block_identifier
        + "-"
        + timezone.now().isoformat()
        + '.csv"'
    )
    return response


def block_export_json_results(block_identifier: str) -> ZipFile:
    """Export block JSON data as zip archive"""

    this_block = Block.objects.get(identifier=block_identifier)
    all_feedback = Feedback.objects.filter(block=this_block)

    # Collect data
    all_sessions = this_block.sessions.order_by("pk")
    all_results = get_results_of_sessions(all_sessions)
    all_participants = get_participants_of_sessions(all_sessions)
    all_profiles = get_profiles_of_participants(all_participants)
    all_sections = Section.objects.filter(playlist__in=this_block.playlists.all())
    all_songs = Song.objects.filter(section__in=all_sections).distinct()

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


def get_block_json_export_as_response(block_identifier: str) -> HttpResponse:
    '''Create a download response for the admin experimenter dashboard'''
    zip_buffer = block_export_json_results(block_identifier)
    response = HttpResponse(zip_buffer.getbuffer())
    response["Content-Type"] = "application/x-zip-compressed"
    response["Content-Disposition"] = (
        'attachment; filename="'
        + block_identifier
        + "-"
        + timezone.now().isoformat()
        + '.zip"'
    )
    return response
