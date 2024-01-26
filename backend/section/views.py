from django.http import Http404, FileResponse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import redirect

from .models import Section
from participant.utils import located_in_nl


def get_section(request, section_id, code):
    """Get section by given id, check location restrictions"""
    try:
        section = Section.objects.get(pk=section_id, code=code)

        # Section will be served, so increase play count
        # On your local development server you can receive multiple requests on
        # a single section
        section.add_play_count()
        section.save()

        # Option 1: provide a redirect to the filename
        # Could be enabled if server load is to high
        # Advantage: low server load
        # Disadvantage: exposes url

        if str(section.filename).startswith('http'):
            # external link, redirect
            return redirect(str(section.filename))

        # We only do this in production, as the Django dev server not correctly supports
        # The range/seeking of audio files in Chrome
        if not settings.DEBUG:
            return redirect(settings.MEDIA_URL + str(section.filename))

        # Option 2: stream file through Django
        # Advantage: keeps url secure, correct play_count value
        # Disadvantage: potential high server load

        filename = settings.BASE_DIR + settings.MEDIA_URL + str(section.filename)

        # Uncomment to only use example file in development
        # if settings.DEBUG:
        #    filename = settings.BASE_DIR + "/upload/example.mp3"

        response = FileResponse(open(filename, 'rb'))

        # Header is required to make seeking work in Chrome
        response['Accept-Ranges'] = 'bytes'

        # Response may log a ConnectionResetError on the development server
        # This has no effect on serving the file
        return response

    except Section.DoesNotExist:
        raise Http404("Section does not exist")
