import json
import logging

from django.http import Http404, HttpRequest, JsonResponse
from django.utils.translation import gettext_lazy as _, get_language
from django_markup.markup import formatter
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Block, Experiment, Feedback, Session
from section.models import Playlist
from experiment.serializers import (
    serialize_block,
    serialize_experiment,
    serialize_phase,
)
from experiment.rules import BLOCK_RULES
from experiment.actions.utils import EXPERIMENT_KEY
from experiment.serializers import ExperimentSerializer

from participant.models import Participant
from participant.utils import get_participant
from theme.serializers import serialize_theme
from question.models import Question, QuestionGroup

logger = logging.getLogger(__name__)


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated]


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
        "playlists": [{"id": playlist.id, "name": playlist.name} for playlist in block.playlists.all()],
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


def add_default_question_series(request, slug):
    if request.method == "POST":
        Block.objects.get(slug=slug).add_default_question_series()
    return JsonResponse({})


def get_experiment(
    request: HttpRequest,
    slug: str,
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

    phases = list(experiment.phases.order_by("index").all())
    if not len(phases):
        return JsonResponse(
            {"error": "This experiment does not have phases and blocks configured"},
            status=500,
        )
    times_played_key = 'f"{slug}-xplayed"'
    times_played = request.session.get(times_played_key, 0)
    for phase in phases:
        serialized_phase = serialize_phase(phase, participant, times_played)
        if serialized_phase:
            return JsonResponse(
                {
                    **serialize_experiment(experiment),
                    **serialized_phase,
                }
            )
    # if no phase was found, start from scratch with the minimum session count
    request.session[times_played_key] = _get_min_session_count(experiment, participant)
    return get_experiment(request, slug)


def _get_min_session_count(experiment: Experiment, participant: Participant) -> int:
    phases = experiment.phases.all()
    session_counts = []
    for phase in phases:
        session_counts.extend(
            [
                Session.objects.exclude(finished_at__isnull=True).filter(block=block, participant=participant).count()
                for block in phase.blocks.all()
            ]
        )
    return min(session_counts)


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


@api_view(["GET"])
def block_rules(request):
    """Return a list of available block rules"""
    rules = [{"id": rule_id, "name": rule_class.__name__} for rule_id, rule_class in BLOCK_RULES.items()]
    return Response(rules)


@api_view(["GET"])
def get_available_questions(request):
    questions = Question.objects.all()
    question_groups = QuestionGroup.objects.all()

    return Response(
        {
            "questions": [{"key": q.key, "question": q.question, "type": q.type} for q in questions],
            "questionGroups": [
                {"key": g.key, "questions": [q.key for q in g.questions.all()]} for g in question_groups
            ],
        }
    )
