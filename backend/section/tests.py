from django.test import TestCase

from section.models import Playlist


class PlaylistModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Playlist.objects.create()

    def test_update_sections_csv_empty(self):
        playlist = Playlist.objects.get(id = 1)
        playlist.csv = ''
        s = playlist.update_sections()
        self.assertFalse(playlist.section_set.all())
        self.assertEqual(s['status'], playlist.CSV_OK)

    def test_update_sections_invalid_row_length(self):
        playlist = Playlist.objects.get(id = 1)
        # Third row invalid, len < 8
        playlist.csv = ("Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0,0\n"
                        "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,0,0\n"
                        "Netta,Toy,0.0,10.0,0,0,0\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0,0\n")
        s = playlist.update_sections()
        self.assertEqual(s['status'], playlist.CSV_ERROR)

    def test_update_sections_not_number(self):
        playlist = Playlist.objects.get(id = 1)
        # Third row string is not a number 
        playlist.csv = ("Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0,0\n"
                        "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,0,0\n"
                        "Netta,Toy,string,string,bat/netta.mp3,string,tag,group\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0,0\n")
        s = playlist.update_sections()
        self.assertEqual(s['status'], playlist.CSV_ERROR)

    def test_valid_csv(self):
        playlist = Playlist.objects.get(id = 1)    
        playlist.csv = ("Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0,0\n"
                        "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,1,2\n"
                        "Netta,Toy,0.0,10.0,bat/netta.mp3,1,tag,group\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,1,0,0\n")
        s = playlist.update_sections()
        self.assertEqual(s['status'], playlist.CSV_OK)
        sections = playlist.section_set.all()
        self.assertEqual(len(sections), 4)

        self.assertEqual(sections[2].artist, "Netta")
        self.assertEqual(sections[2].name, "Toy")
        self.assertEqual(sections[2].start_time, 0.0)
        self.assertEqual(sections[2].duration, 10.0)
        self.assertEqual(sections[2].filename,"bat/netta.mp3")
        self.assertEqual(sections[2].restrict_to_nl, 1)
        self.assertEqual(sections[2].tag, "tag")
        self.assertEqual(sections[2].group, "group")

        self.assertEqual(sections[3].artist, "Salvador Sobral")
        self.assertEqual(sections[3].name, "Amar pelos dois")
        self.assertEqual(sections[3].start_time, 0.0)
        self.assertEqual(sections[3].duration, 10.0)
        self.assertEqual(sections[3].filename,"bat/sobral.mp3")
        self.assertEqual(sections[3].restrict_to_nl, 1)
        self.assertEqual(sections[3].tag, "0")
        self.assertEqual(sections[3].group, '0')
        
