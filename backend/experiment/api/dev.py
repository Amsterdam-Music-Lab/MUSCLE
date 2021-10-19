import random
import csv
import json
from django.shortcuts import render
from django.http import HttpResponse, Http404
from experiment.models import Experiment, Session, Result, Participant
from .util import slugify
from .util.participant import current_participant


def test_sessions(request):
    """Show a test page for manual form actions"""
    experiment = Experiment.objects.filter(pk=1, active=True).first()
    return render(request, 'dev/test_forms.html', {
        'experiment': experiment,
        'section_id': experiment.playlists.first().section_set.all().first().id,
        'participant': current_participant(request)
    })


def fake_playlist(request, rows):
    """Create a csv section list with fake data"""

    # Fake data
    artist = ['The Beatles', 'The Rolling Stones', 'Queen', 'Neil Young',
              'Abba', 'Bon Jovi', 'Elton John', 'The Beachboys', 'Michael Jackson', 'U2']
    word_frags = ['my', 'your', 'from', 'me', 'to', 'you', 'after', 'sun', 'rock',
                  'midnight', 'desert', 'love', 'forever',
                  'last', 'great', 'power', 'day', 'bright']

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="random_section_data.csv"'

    writer = csv.writer(response, quoting=csv.QUOTE_NONNUMERIC)

    current_sections = 0
    current_artist = ""
    current_song = ""
    current_slug = ""
    current_restricted = False
    rows_added = 0
    while rows_added < rows:
        if current_sections > 0:
            # fill sections

            # realistic filenames
            # writer.writerow([song_id, current_artist, current_song,
            #                  current_sections * 30.1, 20.2, '/sections/eurovision/' +
            #                  current_slug + str(current_sections) + ".mp3",
            #                  current_restricted])

            # fake data with /example.mp3
            writer.writerow([current_artist, current_song,
                             current_sections * 30.1, 20.2, '/example.mp3',
                             current_restricted, 0, 0])

            rows_added += 1
            current_sections -= 1
        else:
            # new song
            current_artist = random.choice(artist)
            current_song = random.choice(word_frags).capitalize() + " " + \
                random.choice(word_frags) + " " + random.choice(word_frags)
            current_slug = slugify(current_artist + "-" + current_song)
            current_restricted = 1 if random.randint(0, 6) == 0 else 0
            current_sections = random.randint(1, 6)

    return response


def fake_sessions(request, experiment_id):
    """Add 100 fake sessions to given Experiment"""
    try:
        experiment = Experiment.objects.get(pk=experiment_id, active=True)
    except Experiment.DoesNotExist:
        raise Http404("Experiment does not exist")

    playlists = experiment.playlists.all()
    sessions = []
    results = []
    for _ in range(0, 100):
        # session
        participant = Participant()
        participant.save()
        playlist = random.choice(playlists)
        session = Session(playlist=playlist, participant=participant,
                          experiment=experiment, json_data='{"comment":"auto generated"}')
        session.save()
        sessions.append(session)

    # sections available from playlist
    sections = session.playlist.section_set.all()

    for session in sessions:
        # 20 results
        for _ in range(0, 20):
            results.append(Result(session=session,
                                  section=random.choice(sections),
                                  score=1.0,
                                  json_data=json.dumps({
                                      'recognition_time': 2,
                                      'recognition_assertion': random.randint(0, 1) == 0,
                                      'continuation_correctness': random.randint(0, 1) == 0,
                                      'verification_length': 2,
                                      'verification_correctness': random.randint(0, 1) == 0
                                  }, indent=4)))

    Result.objects.bulk_create(results)

    return HttpResponse("Added 100 sessions to experiment " + experiment.name)
