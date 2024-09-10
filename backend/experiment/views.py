import json
import logging

from django.http import Http404, HttpRequest, JsonResponse
from django.conf import settings
from django.utils.translation import activate, gettext_lazy as _, get_language
from django_markup.markup import formatter

from .models import Block, Experiment, Phase, Feedback, Session
from section.models import Playlist
from experiment.serializers import (
    serialize_block,
    serialize_experiment,
    serialize_phase,
)
from experiment.rules import BLOCK_RULES
from experiment.actions.utils import EXPERIMENT_KEY
from image.serializers import serialize_image
from participant.utils import get_participant
from theme.serializers import serialize_theme

logger = logging.getLogger(__name__)


def get_block(request: HttpRequest, slug: str) -> JsonResponse:
    """Get block data from active block with given :slug
    DO NOT modify session data here, it will break participant_id system
       (/participant and /block/<slug> are called at the same time by the frontend)"""
    block = block_or_404(slug)
    class_name = ""
    active_language = get_language()

    if active_language.startswith("zh"):
        class_name = "chinese"

    participant = get_participant(request)
    session = Session(block=block, participant=participant)

    playlist = block.playlists.first()
    if playlist:
        session.playlist = playlist

    session.save()

    # create data
    block_data = {
        **serialize_block(block),
        "theme": serialize_theme(block.theme_config) if block.theme_config else None,
        "class_name": class_name,  # can be used to override style
        "rounds": block.rounds,
        "bonus_points": block.bonus_points,
        "playlists": [
            {"id": playlist.id, "name": playlist.name}
            for playlist in block.playlists.all()
        ],
        "feedback_info": block.get_rules().feedback_info(),
        "loading_text": _("Loading"),
        "session_id": session.id,
    }

    response = JsonResponse(block_data, json_dumps_params={"indent": 4})

    return response


def post_feedback(request, slug):
    text = request.POST.get("feedback")
    block = block_or_404(slug)
    feedback = Feedback(text=text, block=block)
    feedback.save()
    return JsonResponse({"status": "ok"})


def block_or_404(slug):
    # get block
    try:
        return Block.objects.get(slug=slug)
    except Block.DoesNotExist:
        raise Http404("Block does not exist")


def add_default_question_series(request, id):
    if request.method == "POST":
        Block.objects.get(pk=id).add_default_question_series()
    return JsonResponse({})


def get_experiment(
    request: HttpRequest,
    slug: str,
    phase_index: int = 0,
) -> JsonResponse:
    """
    check which `Phase` objects are related to the `Experiment` with the given slug
    retrieve the phase with the lowest order (= current_phase)
    return the next block from the current_phase without a finished session
    except if Phase.dashboard = True,
    then all blocks of the current_phase will be returned as an array (also those with finished session)
    """

    try:
        experiment = Experiment.objects.get(slug=slug, active=True)
    except Experiment.DoesNotExist:
        raise Http404("Experiment does not exist or is not active")
    except Exception as e:
        logger.error(e)
        return JsonResponse(
            {"error": "Something went wrong while fetching the experiment. Please try again later."},
            status=500,
        )

    request.session[EXPERIMENT_KEY] = slug
    participant = get_participant(request)
    language_code = get_language()[0:2]

    translated_content = experiment.get_translated_content(language_code)

    if not translated_content:
        raise ValueError("No translated content found for this experiment")

    experiment_language = translated_content.language
    activate(experiment_language)

    phases = list(Phase.objects.filter(experiment=experiment.id).order_by("index"))
    try:
        current_phase = phases[phase_index]
        serialized_phase = serialize_phase(current_phase, participant)
        if not serialized_phase:
            # if the current phase is not a dashboard and has no unfinished blocks, it will return None
            # set it to finished and continue to next phase
            phase_index += 1
            return get_experiment(request, slug, phase_index=phase_index)
    except IndexError:
        serialized_phase = {"dashboard": [], "next_block": None}

    response = JsonResponse({**serialize_experiment(experiment, language_code), **serialized_phase})

    return response


def get_associated_blocks(pk_list):
    """get all the experiment objects registered in an Experiment field"""
    return [Block.objects.get(pk=pk) for pk in pk_list]


def render_markdown(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"})

    if not request.body:
        return JsonResponse({"status": "error", "message": "No body found in request"})

    if request.content_type != "application/json":
        return JsonResponse({"status": "error", "message": "Only application/json content type is allowed"})

    data = json.loads(request.body)
    markdown = data["markdown"]

    if markdown:
        return JsonResponse({"html": formatter(markdown, filter_name="markdown")})

    return JsonResponse({"html": ""})


def validate_block_playlist(request: HttpRequest, rules_id: str) -> JsonResponse:
    """
    Validate the playlist of an experiment based on the used rules
    """

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"})

    if not request.body:
        return JsonResponse({"status": "error", "message": "No body found in request"})

    if request.content_type != "application/json":
        return JsonResponse({"status": "error", "message": "Only application/json content type is allowed"})

    json_body = json.loads(request.body)
    playlist_ids = json_body.get("playlists", [])
    playlists = Playlist.objects.filter(id__in=playlist_ids)

    if not playlists:
        return JsonResponse({"status": "error", "message": "The block must have a playlist."})

    rules = BLOCK_RULES[rules_id]()

    if not rules.validate_playlist:
        return JsonResponse({"status": "warn", "message": "This rulesset does not have a playlist validation."})

    playlist_errors = []

    for playlist in playlists:
        errors = rules.validate_playlist(playlist)
        if errors:
            playlist_errors.append({"playlist": playlist.name, "errors": errors})

    if playlist_errors:
        return JsonResponse(
            {"status": "error", "message": "There are errors in the playlist.", "errors": playlist_errors}
        )

    return JsonResponse({"status": "ok", "message": "The playlist is valid."})
