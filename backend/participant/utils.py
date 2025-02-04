import logging
import urllib
import urllib.request
from django.conf import settings
from django.http import HttpRequest


from .models import Participant
PARTICIPANT_KEY = 'participant_id'

logger = logging.getLogger(__name__)


def located_in_nl(request: HttpRequest) -> bool:
    """Return True if the requesting IP-address is located in NL

    Args:
        request: Http request object

    Returns:
        Whether a participant is located in the Netherlands or not.

    Example:
        Check if the participant is located in the Netherlands
        ```python
        if located_in_nl(request):
            # block of code to be executed if the condition is true
        ```
    """
    return country(request) == 'nl'


def country(request: HttpRequest) -> str:
    """Get the country code of the current participant

    Args:
        request: Http request object

    Returns:
        Country code from: `experiment.standards.iso_countries.ISO_COUNTRIES`

    Example:
        Get country code from the request
        ```python
        country_code = country(request)
        ```
    """

    country_code = ""
    key = 'country_code'

    # Get country_code from session
    country_code = request.session.get(key)

    # If country code is missing, guess country by ip address
    if not country_code:
        ip_address = visitor_ip_address(request)

        if settings.DEBUG:
            # On development, always fake netherlands
            country_code = "nl"
        else:
            country_code = get_country_code(ip_address)
            if country_code is None:
                country_code = ""

        request.session[key] = country_code

    return country_code


def get_country_code(ip_address: str) -> str:
    """Get the country code from a given ip address

    Args:
        ip_address (str): The ip address of the participant

    Returns:
        Country code from: `experiment.standards.iso_countries.ISO_COUNTRIES`

    Example:
        Get the country code from an ip address
        ```python
        country_code = get_country_code("192.168.2.1")
        ```
    """

    # Check if location provided is configured
    if not settings.LOCATION_PROVIDER:
        return None

    # Prepare url
    ip_address = urllib.parse.quote(ip_address)
    location_url = settings.LOCATION_PROVIDER.format(ip_address)

    # Request location data
    with urllib.request.urlopen(location_url) as url:
        try:
            return url.read().decode()
        except:
            return None


def visitor_ip_address(request: HttpRequest) -> str:
    """Get the visitor's ip address from the request

    Args:
        request: Http request object

    Returns:
        ip address of the participant

    Example:
        Get ip address from the request
        ```python
        ip_address = visitor_ip_address(request)
        ```
    """

    # You may want to change the header based on your production settings
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]

    return request.META.get('REMOTE_ADDR')


def get_participant(request: HttpRequest) -> Participant:
    """Get participant object from the session

    Args:
        request: Http request object

    Returns:
        Participant object linked to the session

    Example:
        Get current participant from the request
        ```python
        participant = get_participant(request)
        ```
    """
    # get participant from session
    participant_id = request.session.get(PARTICIPANT_KEY, -1)

    if not participant_id or participant_id == -1:
        raise Participant.DoesNotExist("No participant in session")

    try:
        return Participant.objects.get(
                pk=int(participant_id))
    except Participant.DoesNotExist:
        raise


def get_or_create_participant(request:HttpRequest) -> Participant:
    """Get a participant from URL, the session, or create/add a new one

    Args:
        request: Http request object

    Returns:
        Participant object from the `participant_url_id`, the active session, \
        or from a newly created object if none of the previous methods were successful

    Example:
        Get or create participant from the request
        ```python
        participant = get_or_create_participant(request)
        ```
    """
    # check if query string contains  participant
    participant_id_url = request.GET.get("participant_id")  # can be None
    try:
        if participant_id_url:
            # get participant from query string
            participant = Participant.objects.get(participant_id_url = participant_id_url)
            set_participant(request, participant)
            return participant
        else:
            # Get participant from session
            participant = get_participant(request)

    except Participant.DoesNotExist:
        # create new participant
        country_code = country(request)
        access_info = request.META.get('HTTP_USER_AGENT')

        # Create a new Participant, store the country code once
        participant = Participant(country_code=country_code, access_info=access_info, participant_id_url=participant_id_url)
        participant.save()
        set_participant(request, participant)
    return participant


def set_participant(request: HttpRequest, participant: Participant):
    """Set a participant to the current session

    Args:
        request: Http request object
        participant: Participant instance

    Example:
        Set a participant to the current session
        ```python
        set_participant(request, participant)
        ```
    """
    if participant:
        request.session[PARTICIPANT_KEY] = participant.id
    else:
        del request.session[PARTICIPANT_KEY]
