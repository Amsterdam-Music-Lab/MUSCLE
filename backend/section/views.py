import json
import csv
from http import HTTPStatus
import os
from django.http import Http404, FileResponse, JsonResponse
from django.conf import settings
from django.shortcuts import redirect

from .models import Section


def get_section(request, section_id, code):
    """Get section by given id"""
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


def validate_csv(request):
    """Validate the csv file"""

    json_body = json.loads(request.body)
    csv_data = json_body['csv']

    # Add new sections from csv
    try:
        reader = csv.DictReader(csv_data.splitlines(), fieldnames=(
            'artist', 'name', 'start_time', 'duration', 'filename', 'tag', 'group'))
    except csv.Error:
        return {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'message': "Error: could not initialize csv.DictReader"
        }

    validation_warnings = []
    validation_errors = []
    lines_count = 0
    parsed_csv_data = []

    for row in reader:
        lines_count += 1

        if None in row.values():
            validation_errors.append(
                f"Error: Missing value in row {lines_count}")
            continue

        if not row['filename'].endswith(('.mp3', '.wav', '.ogg')):
            validation_errors.append(
                f"Error: Invalid file extension in row {lines_count}")
            continue

        if not row['start_time'].replace('.', '', 1).isdigit():
            validation_errors.append(
                f"Error: Invalid start_time in row {lines_count}")
            continue

        if not row['duration'].replace('.', '', 1).isdigit():
            validation_errors.append(
                f"Error: Invalid duration in row {lines_count}")
            continue

        # check if file exists
        filename = row['filename']
        if not filename.startswith('http'):
            full_file_path = f'./upload/{filename}'
            if not os.path.isfile(full_file_path):
                validation_errors.append(f"Error: File '{filename}' cannot be found in row {lines_count}.")

        for key, value in row.items():
            if value != value.strip():
                validation_warnings.append(
                    f"Warning: Whitespace in column '{key}' with value '{value}' in row {lines_count}")

        parsed_csv_data.append(row)

    if validation_errors:

        message = f"Error: CSV contains {len(validation_errors)} errors"

        if validation_warnings:
            message += f" and {len(validation_warnings)} warnings"

        return JsonResponse({
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'message': message,
            'warnings': validation_warnings,
            'errors': validation_errors
        }, status=HTTPStatus.UNPROCESSABLE_ENTITY)

    message = f"CSV with {lines_count} rows parsed successfully"

    if validation_warnings:
        message += f" with {len(validation_warnings)} warnings"

    return JsonResponse({
        'status': HTTPStatus.OK,
        'message': message,
        'lines': lines_count,
        'warnings': validation_warnings,
        'data': parsed_csv_data
    }, status=HTTPStatus.OK)
