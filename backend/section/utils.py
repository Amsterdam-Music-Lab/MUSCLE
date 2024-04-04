class CsvStringBuilder(object):
    def __init__(self):
        self.csv_string = []

    def write(self, row):
        self.csv_string.append(row)


def get_or_create_song(artist='', name=''):
    """Retrieve an extisting song or create a new one"""
    from .models import Song
    song, created = Song.objects.get_or_create(
        artist=artist,
        name=name)
    return song
