import json
import logging
from typing import Union

from django.views.decorators.http import require_POST
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseServerError,
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)

from participant.utils import get_participant
from session.models import Session
from result.models import Result
from result.utils import handle_results

logger = logging.getLogger(__name__)

@require_POST
def score(
    request: HttpRequest,
) -> Union[JsonResponse, HttpResponseBadRequest, HttpResponseServerError]:
    """Attempt to create a new result for the given session, and return a success or error response

    Args:
        request: the request coming in from the frontend

    Returns:
        a JsonResponse with `{'succcess': True}`,
        a HttpResponseBadRequest if the request.POST data does not contain `json_data`, or
        a HttpResponseServerError: if no result can be retrieved or created based on the session / participant / request data
    """
    session = verify_session(request)
    if isinstance(session, HttpResponse):
        return session

    # Create result based on POST data
    json_data = request.POST.get("json_data")
    if not json_data:
        return HttpResponseBadRequest("json_data not defined")

    try:
        result_data = json.loads(json_data)
        # Create a result from the data
        handle_results(result_data, session)
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError("Invalid data")
    return JsonResponse({'success': True})


@require_POST
def intermediate_score(
    request: HttpRequest,
) -> Union[JsonResponse, HttpResponseBadRequest]:
    """Calculate and return a score based on frontend data
    Args:
        request: the request from the frontend

    Returns:
        a JsonResponse with the score, or a HttpResponseBadRequest if the request.POST data does not contain `json_data`
    """
    session = verify_session(request)
    if isinstance(session, HttpResponse):
        return session
    result = request.POST.get("json_data")
    if not result:
        return HttpResponseBadRequest("json_data not defined")
    score = session.block_rules().calculate_intermediate_score(session, result)
    return JsonResponse({'score': score})


@require_POST
def consent(request: HttpRequest) -> JsonResponse:
    '''Register consent: in contrast to `score`, available without sending a session_id

    Args:
        request: the request from the frontend

    Returns:
        a JsonResponse with {'status': 'ok'}
    '''
    participant = get_participant(request)
    data = json.loads(request.POST.get('json_data'))
    result = Result.objects.create(
        participant=participant,
        question_key=data.get('key'),
        given_response='agreed'
    )
    result.save()
    return JsonResponse({'status': 'ok'})


def current_profile(request: HttpRequest) -> JsonResponse:
    """Get current participant profile (i.e., all results tied to the participant)

    Args:
        request: frontend request

    Returns:
        JsonResponse with serialized result objects
    """
    participant = get_participant(request)
    return JsonResponse(participant.profile_object(), json_dumps_params={'indent': 4})


def get_result(
    request: HttpRequest, question_key: str
) -> Union[JsonResponse, HttpResponse]:
    """Get data of a specific result from participant profile

    Args:
        request: frontend request
        question_key: the `question_key` of the result

    Returns:
        a JsonResponse with the answer, or a `No Content` HttpResponse
    """
    participant = get_participant(request)
    try:
        result = Result.objects.get(question_key=question_key, participant=participant)
    except Result.DoesNotExist:
        return HttpResponse(status=204)

    return JsonResponse({"answer": result.given_response},
                        json_dumps_params={'indent': 4})


def verify_session(
    request: HttpRequest,
) -> Union[Session, HttpResponseBadRequest, HttpResponseServerError]:
    """Given the frontend request, make sure a valid session for the current participant exists
    Args:
        request: the frontend request

    Returns:
        a `Session` object, or a HttpResponse with details about the failure
    """
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
        return HttpResponseNotFound("No session found")

    # Prevent creating results when session is finished
    if session._is_finished():
        return HttpResponseServerError("Session has already finished")

    return session
