import json

from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect

from participant.utils import get_participant
from session.models import Session
from result.models import Result
from result.utils import handle_results

@require_POST
def score(request):
    """Create a new result for the given session, and return followup action"""
    # Current participant
    participant = get_participant(request)
    # Get session for current participant
    session_id = request.POST.get("session_id")

    if not session_id:
        return HttpResponseBadRequest("session_id not defined")
    try:
        session = Session.objects.get(
            pk=session_id, participant__id=participant.id)
    except Session.DoesNotExist:
        return HttpResponseServerError("No session found")

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
        result = handle_results(result_data, session)   
        if result and result.session:
            # increment the round number if this was a session type result
            session.increment_round()
        else:
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

@require_POST
def consent(request):
    ''' Register consent: in contrast to `create`, available without sending a session_id '''
    participant = get_participant(request)
    data = json.loads(request.POST.get('json_data'))
    result = Result.objects.create(
        participant=participant,
        question_key=data.get('key'),
        given_response='agreed'
    )
    result.save()
    return JsonResponse({'status': 'ok'})


def current_profile(request):
    """Get current participant profile"""
    participant = get_participant(request)

    return JsonResponse(participant.profile_object(), json_dumps_params={'indent': 4})


def get_result(request, question):
    """Get specific answer from question from participant profile"""
    participant = get_participant(request)
    try:
        result = Result.objects.get(
            question_key=question, participant=participant)
    except Result.DoesNotExist:
        raise Http404("Not found")

    return JsonResponse({"answer": result.given_response},
                        json_dumps_params={'indent': 4})
