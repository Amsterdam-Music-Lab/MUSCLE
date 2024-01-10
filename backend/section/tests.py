from django.test import Client, TestCase
from django.contrib.admin.sites import AdminSite
from section.admin import PlaylistAdmin
from section.models import Playlist, Section, Song


class PlaylistModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Playlist.objects.create(name='TestPlaylist')

    def test_update_sections_csv_empty(self):
        playlist = Playlist.objects.get(name='TestPlaylist')
        playlist.csv = ''
        s = playlist.update_sections()
        self.assertFalse(playlist.section_set.all())
        self.assertEqual(s['status'], playlist.CSV_OK)

    def test_update_sections_invalid_row_length(self):
        playlist = Playlist.objects.get(name='TestPlaylist')
        # Third row invalid, len < 8
        playlist.csv = ("Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0,0\n"
                        "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,0,0\n"
                        "Netta,Toy,0.0,10.0,0,0,0\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0,0\n")
        s = playlist.update_sections()
        self.assertEqual(s['status'], playlist.CSV_ERROR)

    def test_update_sections_not_number(self):
        playlist = Playlist.objects.get(name='TestPlaylist')
        # Third row string is not a number 
        playlist.csv = ("Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0,0\n"
                        "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,0,0\n"
                        "Netta,Toy,string,string,bat/netta.mp3,string,tag,group\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0,0\n")
        s = playlist.update_sections()
        self.assertEqual(s['status'], playlist.CSV_ERROR)
    
    def test_get_section(self):
        playlist = Playlist.objects.get(name='TestPlaylist')
        playlist.csv = (
                        "Weird Al,Eat It,0.0,10.0,some/file.mp3,0,tag1,0\n"
                        "Weird Al,Eat It,10.0,20.0,some/file.mp3,0,tag2,0\n"
                        "Weird Al,Like a Surgeon,0.0,10.0,some/otherfile.mp3,0,tag1,0\n"
                        "Weird Al,Like a Surgeon,10.0,20.0,some/otherfile.mp3,0,tag2,0\n"
                        )
        playlist.update_sections()
        assert Song.objects.count() == 2
        song1 = Song.objects.get(name='Eat It')
        section = playlist.get_section(song_ids=[song1.id])
        assert section.song.id == song1.id
        section = playlist.get_section(filter_by={'tag': 'tag1'})
        assert section.tag == 'tag1'
        song2 = Song.objects.get(name='Like a Surgeon')
        section = playlist.get_section(filter_by={'tag': 'tag2'}, song_ids=[song2.id])
        assert section.tag == 'tag2' and section.song.id == song2.id

    def test_valid_csv(self):
        playlist = Playlist.objects.get(name='TestPlaylist')    
        playlist.csv = ("Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0,0\n"
                        "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,1,2\n"
                        "Netta,Toy,0.0,10.0,bat/netta.mp3,1,tag,group\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,1,0,0\n")
        s = playlist.update_sections()
        self.assertEqual(s['status'], playlist.CSV_OK)
        sections = playlist.section_set.all()
        self.assertEqual(len(sections), 4)

        self.assertEqual(sections[2].song.artist, "Netta")
        self.assertEqual(sections[2].song.name, "Toy")
        self.assertEqual(sections[2].start_time, 0.0)
        self.assertEqual(sections[2].duration, 10.0)
        self.assertEqual(sections[2].filename,"bat/netta.mp3")
        self.assertEqual(sections[2].song.restricted, [{"restricted": "nl"}])
        self.assertEqual(sections[2].tag, "tag")
        self.assertEqual(sections[2].group, "group")

        self.assertEqual(sections[3].song.artist, "Salvador Sobral")
        self.assertEqual(sections[3].song.name, "Amar pelos dois")
        self.assertEqual(sections[3].start_time, 0.0)
        self.assertEqual(sections[3].duration, 10.0)
        self.assertEqual(sections[3].filename,"bat/sobral.mp3")
        self.assertEqual(sections[3].song.restricted, [{"restricted": "nl"}])
        self.assertEqual(sections[3].tag, "0")
        self.assertEqual(sections[3].group, '0')
       
        
class MockRequest:
    pass


this_playlist_admin = PlaylistAdmin(
    model=Playlist, admin_site=AdminSite)
    

class TestAmdinEditSection(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.create()
        cls.song = Song.objects.create(artist='default',
                            name='default',
                            restricted= [{"restricted": "nl"}])
        Section.objects.create(playlist=cls.playlist,
                               song=cls.song)

    def test_edit_sections(self):
        request = MockRequest()
        this_section = Section.objects.first()
        pre_fix = str(this_section.id)
        request.POST = {'_update': '',
                        pre_fix + '_artist': 'edited',
                        pre_fix + '_name': 'edited',
                        pre_fix + '_start_time': '1.1',
                        pre_fix + '_duration': '1.1',
                        pre_fix + '_tag': 'edited',
                        pre_fix + '_group': 'edited',
                        pre_fix + '_restricted': '0'}
        this_playlist = Playlist.objects.first()            
        response = this_playlist_admin.edit_sections(request, this_playlist)
        edit_section = Section.objects.first()
        self.assertEqual(edit_section.song.artist, 'edited')
        self.assertEqual(edit_section.song.name, 'edited')
        self.assertEqual(edit_section.start_time, 1.1)
        self.assertEqual(edit_section.duration, 1.1)
        self.assertEqual(edit_section.tag, 'edited')
        self.assertEqual(edit_section.group, 'edited')
        self.assertEqual(edit_section.song.restricted, [])
        self.assertEqual(response.status_code, 302)
 