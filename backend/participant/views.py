import logging

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, Http404, HttpResponseServerError, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
from django.utils.translation import ngettext_lazy as ngettext
from django.utils.translation import gettext_lazy as _

from .models import Participant
from .utils import get_participant, get_or_create_participant, set_participant

logger = logging.getLogger(__name__)


def current(request):
    """Current participant data from session"""
    participant = get_or_create_participant(request)
    response = JsonResponse({
        'id': participant.id,
        'hash': participant.unique_hash,
        'csrf_token': get_token(request),
        'participant_id_url': participant.participant_id_url,
        'country': participant.country_code
    }, json_dumps_params={'indent': 4})
    return response


def scores(request):
    """Current participant scores"""
    participant = get_participant(request)
    scores = participant.scores_per_experiment()

    return JsonResponse({
        'messages': {
            'title': _('My profile'),
            'summary': ngettext(
            'You have participated in %(count)d Amsterdam Music Lab experiment. Your best score is:',
            'You have partcipated in %(count)d Amsterdam Music Lab experiments. Your best scores are:',
                len(scores)) % {'count': len(scores)},
            'points': _('points'),
            'continue': _('Use the following link to continue with your profile at another moment or on another device.'),
        },
        'scores': scores
    }, json_dumps_params={'indent': 4})


def reload(request, participant_id, unique_hash):
    """Reloads participant from DB, based on id and hash"""
    try:
        participant = Participant.objects.get(
            pk=participant_id, unique_hash=unique_hash)
    except Participant.DoesNotExist:
        raise Http404("Participant not found")

    set_participant(request, participant)
    return redirect(settings.RELOAD_PARTICIPANT_TARGET)


def link(request):
    """Get the participant reload url"""

    # Current participant
    participant = get_participant(request)

    # Build url (hard coded server url)
    url = 'https://app.amsterdammusiclab.nl/experiment/participant/reload/{}/{}/'.format(
        participant.id, participant.unique_hash)

    # This is the original solution, but doesn't work with Nginx in production
    # As it requires the original server host to be passed through, which isn't the case
    # request.build_absolute_uri(reverse('experiment:participant_reload', args=(participant.id, participant.unique_hash)))

    return JsonResponse({
        'url': url,
        'copy_message': _('copy')
    }, json_dumps_params={'indent': 4})


@require_POST
def share(request):
    """Shares the participant reload url by email"""

    # Current participant
    participant = get_participant(request)

    # Get email address
    email = request.POST.get("email")

    try:
        validate_email(email)
        valid_email = True
    except ValidationError:
        valid_email = False

    if not email or not valid_email:
        return HttpResponseBadRequest("email not defined or invalid")

    # Email parameters
    url = request.build_absolute_uri(
        reverse('experiment:participant_reload', args=(participant.id, participant.unique_hash)))

    # Send mail
    try:
        send_mail(
            'Your experiment session',
            'Hi!\nYou can restore your experiment sessions in the future by using the following url:\n{}\n\nThank you for your participating in our experiments!'.format(
                url),
            'Amsterdam Music Lab <{}>'.format(settings.FROM_MAIL),
            [email],
            fail_silently=False,
        )
    except:
        return HttpResponseServerError("An error occured while sending the email")

    return JsonResponse({
        'status': 'ok',
    }, json_dumps_params={'indent': 4})
