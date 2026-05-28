from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from .models import Session
from experiment.models import Experiment
from experiment.serializers import serialize_actions
from participant.utils import get_participant


def next_round(request, session_id):
    """
    Fall back to continue a block is case next_round data is missing
    This data is normally provided in: result()
    """
    # Current participant
    participant = get_participant(request)

    session = get_object_or_404(Session, pk=session_id, participant__id=participant.id)

    # Get next round for given session
    actions = serialize_actions(session.block_rules().next_round(session))

    if not isinstance(actions, list):
        if actions.get("redirect"):
            return redirect(actions.get("redirect"))
        actions = [actions]

    return JsonResponse({"next_round": actions}, json_dumps_params={"indent": 4})
