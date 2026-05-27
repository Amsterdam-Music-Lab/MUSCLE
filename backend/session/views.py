from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from .models import Session
from experiment.models import Experiment
from experiment.serializers import serialize_actions
from experiment.actions.utils import EXPERIMENT_KEY
from participant.utils import get_participant


def next_round(request, session_id):
    """
    Fall back to continue a block is case next_round data is missing
    This data is normally provided in: result()
    """
    # Current participant
    participant = get_participant(request)

    session = get_object_or_404(Session, pk=session_id, participant__id=participant.id)

    # check if this block is part of an Experiment
    experiment_slug = request.session.get(EXPERIMENT_KEY)
    if experiment_slug:
        # check that current session does not have the experiment information saved yet
        if not session.json_data.get(EXPERIMENT_KEY):
            # set information of the Experiment to the session
            experiment = Experiment.objects.get(slug=experiment_slug)
            if experiment and session.block in experiment.associated_blocks():
                session.save_json_data({EXPERIMENT_KEY: experiment_slug})

    # Get next round for given session
    actions = serialize_actions(session.block_rules().next_round(session))

    if not isinstance(actions, list):
        if actions.get("redirect"):
            return redirect(actions.get("redirect"))
        actions = [actions]

    return JsonResponse({"next_round": actions}, json_dumps_params={"indent": 4})
