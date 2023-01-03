import json

from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponseServerError, JsonResponse, HttpResponseBadRequest

from participant.utils import current_participant
from session.models import Session

@require_POST
def result(request):
    """Create a new result for the given session, and return followup action"""
    # Current participant
    participant = current_participant(request)
    # Get session for current participant
    session_id = request.POST.get("session_id")

    if not session_id:
        return HttpResponseBadRequest("session_id not defined")
    try:
        session = Session.objects.get(
            pk=session_id, participant__id=participant.id)
    except Session.DoesNotExist:
        raise Http404("Session does not exist")

    # Prevent creating results when session is finished
    if session.is_finished():
        return HttpResponseServerError("Session has already finished")

    # Create result based on POST data
    json_data = request.POST.get("json_data")
    if not json_data:
        return HttpResponseBadRequest("json_data not defined")

    try:
        result_data = json.loads(json_data)
        # Create a result from the data
        if 'form' in result_data:
            result = session.experiment_rules().handle_results(session, result_data)
        else:
            result = session.experiment_rules().handle_result(session, result_data)
            
        if not result:
            return HttpResponseServerError("Could not create result from data")

    except ValueError:
        return HttpResponseServerError("Invalid data")

    # Get next round for given session
    if request.session.get('experiment_series'):
        # we are in the middle of an experiment series - need to pass in request.session object
        action = session.experiment_rules().next_round(session, request.session)
    else:
        action = session.experiment_rules().next_round(session)
    return JsonResponse(action, json_dumps_params={'indent': 4})
