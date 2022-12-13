import json

from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_POST
from experiment.rules.util.score import SCORING_RULES
from experiment.models import Profile, Result, Session
from .util.participant import current_participant


def current(request):
    """Get current participant profile"""
    participant = current_participant(request)

    return JsonResponse(participant.profile_object(), json_dumps_params={'indent': 4})


def get(request, question):
    """Get specific answer from question from participant profile"""
    participant = current_participant(request)

    try:
        result = Result.objects.get(
            question_key=question, is_profile=True, session__participant=participant)
    except Result.DoesNotExist:
        raise Http404("Not found")

    return JsonResponse({"answer": result.given_response},
                        json_dumps_params={'indent': 4})


@require_POST
def create(request):
    """Store a profile question/answer to current participant"""
    # Current participant
    participant = current_participant(request)
    # Get question
    result_data = json.loads(request.POST.get("json_data"))
    # Session ID, defaults to 0
    session_id = int(request.POST.get("session_id", -1))
    try:
        session = Session.objects.get(pk=session_id, participant=participant)
    except Session.DoesNotExist:
        session = None
    if not result_data:
        return HttpResponseBadRequest("Missing required parameter: result")
    for form_element in result_data['form']:
        question = form_element['key']
        try:
            result = Result.objects.get(
                question_key=question, is_profile=True, session__participant=participant)
        except Result.DoesNotExist:
            # Create new profile value, and session not linked to an experiment
            if not session:
                session = Session(participant=participant)
                session.save()
            result = Result(session=session,
                is_profile=True,
                question_key=question)
        result.given_response = form_element['value']
        scoring_rule = SCORING_RULES.get(form_element.get('scoring_rule'))
        if scoring_rule:
            result.score = scoring_rule(form_element, None, None)
        result.save()

    return JsonResponse({
        'status': 'ok'
    }, json_dumps_params={'indent': 4})
