import json
import urllib
import urllib.request
from django.conf import settings


def located_in_nl(request):
    """Return True if the requesting IP-address is located in NL"""
    return country(request) == 'nl'


def country(request):
    """Get country code of requesting ip"""

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


def get_country_code(ip_address):
    """Get country code from given ip address"""

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
            # Old format?
            # data = json.loads(url.read().decode())
            # if data.get('status') == 'ok':
            #     return data.get('country')
            # else:
            #     return None
        except:
            return None


def visitor_ip_address(request):
    """Get visitor ip address from request"""

    # You may want to change the header based on your production settings
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]

    return request.META.get('REMOTE_ADDR')
