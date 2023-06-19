import json

from django.conf import settings
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Session
from experiment.models import Experiment
from section.models import Playlist
from participant.utils import get_participant


@require_POST
def create_session(request):
    """Create new session for given experiment for current participant"""

    # Current participant
    participant = get_participant(request)

    # Get experiment
    experiment_id = request.POST.get("experiment_id")
    if not experiment_id:
        return HttpResponseBadRequest("experiment_id not defined")
    try:
        experiment = Experiment.objects.get(pk=experiment_id, active=True)
    except Experiment.DoesNotExist:
        raise Http404("Experiment does not exist")

    # Create new session
    session = Session(experiment=experiment, participant=participant)

    # Get playlist
    if experiment.playlists.count() == 1:
        # Skip if there is only one playlist
        session.playlist = experiment.playlists.first()
    else:
        # load playlist from request
        playlist_id = request.POST.get("playlist_id")

        if not playlist_id:
            return HttpResponseBadRequest("playlist_id not defined")

        try:
            playlist = Playlist.objects.get(
                pk=playlist_id, experiment__id=experiment.id)
            session.playlist = playlist
        except Playlist.DoesNotExist:
            raise Http404("Playlist does not exist")

    # Get json_data
    data = request.POST.get("data")
    if data:
        try:
            json.loads(data)
            session.json_data = data
        except ValueError:
            return HttpResponseBadRequest("Invalid data")

    # Save session
    session.save()

    return JsonResponse({'session': {'id': session.id}})


def continue_session(request, session_id):
    """ given a session_id, continue where we left off """
    
    session = get_object_or_404(Session, pk=session_id)

    # Get next round for given session
    action = session.experiment_rules().next_round(session)
    return JsonResponse(action, json_dumps_params={'indent': 4})


def next_round(request, session_id):
    """
    Fall back to continue an experiment is case next_round data is missing
    This data is normally provided in: result()
    """
    # Current participant
    participant = get_participant(request)

    session = get_object_or_404(Session, 
            pk=session_id, participant__id=participant.id)

    # Get next round for given session
    if request.session.get('experiment_series'):
        # we are in the middle of an experiment series - need to pass in request.session object
        actions = session.experiment_rules().next_round(session, request.session)
    else:
        # Get next round for given session
        actions = session.experiment_rules().next_round(session)
    
    if not isinstance(actions,  list):
        if actions.get('redirect'):
            return redirect(actions.get('redirect'))
        actions = [actions]

    return JsonResponse({'next_round': actions}, json_dumps_params={'indent': 4})

def finalize_session(request, session_id):
    # Get session
    participant = get_participant(request)
    session = get_object_or_404(Session, pk=session_id, participant__id=participant.id)
    session.finish()
    session.save()
    return redirect(settings.HOMEPAGE)
