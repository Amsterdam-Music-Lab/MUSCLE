import json

from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponseForbidden
from django.views.decorators.http import require_POST
from experiment.models import Profile, Session
from .util.participant import current_participant


def current(request):
    """Get current participant profile"""
    participant = current_participant(request)

    return JsonResponse(participant.profile_object(), json_dumps_params={'indent': 4})


def get(request, question):
    """Get specific answer from question from participant profile"""
    participant = current_participant(request)

    try:
        profile = Profile.objects.get(
            question=question, participant=participant)
    except Profile.DoesNotExist:
        raise Http404("Not found")

    return JsonResponse({"answer": profile.answer},
                        json_dumps_params={'indent': 4})


@require_POST
def create(request):
    """Store a profile question/answer to current participant"""
    # Current participant
    participant = current_participant(request)
    # Get question
    result = json.loads(request.POST.get("json_data")).get('result')

    if not result:
        return HttpResponseBadRequest("Missing required parameter: result")

    for form_element in result['form']:
        question = form_element['question'] 
        try:
            profile = Profile.objects.get(
                participant=participant, question=question)
            # Existing profile value

        except Profile.DoesNotExist:
            # Create new profile value
            profile = Profile(participant=participant,
                              question=question)
        profile.answer = form_element['value']
        profile.save()

        # Session ID, defaults to 0
        session_id = int(request.POST.get("session_id", 0))

        if session_id > 0:
            try:
                # Validate the session belongs to current participant
                session = Session.objects.get(
                    participant=participant, pk=session_id)
                profile.session_id = session.id

            except Session.DoesNotExist:
                return HttpResponseForbidden("No access to given session")

        profile.save()

    return JsonResponse({
        'status': 'ok'
    }, json_dumps_params={'indent': 4})
