from os.path import join

from django.http import Http404, HttpRequest, FileResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect

from .models import Playlist, Section
from rest_framework.decorators import api_view
from rest_framework.response import Response


def get_section(
    request: HttpRequest, section_id: int
) -> Section | HttpResponsePermanentRedirect | HttpResponseRedirect | FileResponse:
    """Get section by given id"""
    try:
        section = Section.objects.get(pk=section_id)

        # Section will be served, so increase play count
        # On your local development server you can receive multiple requests on
        # a single section
        section.add_play_count()
        section.save()

        # Option 1: provide a redirect to the filename
        # Could be enabled if server load is to high
        # Advantage: low server load
        # Disadvantage: exposes url

        if str(section.filename).startswith("http"):
            # external link, redirect
            return redirect(str(section.filename))

        if section.playlist.url_prefix:
            # Make link external using url_prefix
            return redirect(section.playlist.url_prefix + str(section.filename))

        # We only do this in production, as the Django dev server not correctly supports
        # The range/seeking of audio files in Chrome
        if not settings.DEBUG:
            return redirect(settings.MEDIA_URL + str(section.filename))

        # Option 2: stream file through Django
        # Advantage: keeps url secure, correct play_count value
        # Disadvantage: potential high server load
        filename = str(section.filename)
        if filename.startswith("/"):
            # remove initial slash in filename, as otherwise os.path.join considers it an absolute path
            filename = filename[1:]
        filepath = join(settings.MEDIA_ROOT, filename)

        # Uncomment to only use example file in development
        # if settings.DEBUG:
        #    filename = settings.BASE_DIR + "/upload/example.mp3"
        response = FileResponse(open(filepath, "rb"))

        # Header is required to make seeking work in Chrome
        response["Accept-Ranges"] = "bytes"

        # Response may log a ConnectionResetError on the development server
        # This has no effect on serving the file
        return response

    except Section.DoesNotExist:
        raise Http404("Section does not exist")


@api_view(["GET"])
def playlists(request):
    """Return a list of all playlists"""
    playlists = [{"id": playlist.id, "name": playlist.name} for playlist in Playlist.objects.all()]
    return Response(playlists)
