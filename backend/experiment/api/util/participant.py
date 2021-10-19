from experiment.models import Participant
from .location import country

SESSION_KEY = 'participant_id'


def current_participant(request):
    """Get a participant from the session, or create/add a new one"""
    participant = None

    # get participant from session
    if SESSION_KEY in request.session:
        try:
            participant = Participant.objects.get(
                pk=int(request.session[SESSION_KEY]))
        except Participant.DoesNotExist:
            participant = None

    if not participant:
        country_code = country(request)

        # Create a new Participant, store the country code once
        participant = Participant(country_code=country_code)
        participant.save()
        set_participant(request, participant)

    return participant


def set_participant(request, participant):
    """Set a participant to the session"""
    if participant:
        request.session[SESSION_KEY] = participant.id
    else:
        del request.session[SESSION_KEY]
