from django.test import TestCase

from experiment.models.playlist import Playlist


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
                        "Netta,Toy,string,string,bat/netta.mp3,string,string,string\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0,0\n")
        s = playlist.update_sections()
        self.assertEqual(s['status'], playlist.CSV_ERROR)

    def test_valid_csv(self):
        playlist = Playlist.objects.get(id = 1)    
        playlist.csv = ("Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0,0\n"
                        "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,0,0\n"
                        "Netta,Toy,0.0,10.0,bat/netta.mp3,1,2,3\n"
                        "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0,0\n")
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
        self.assertEqual(sections[2].tag_id, 2)
        self.assertEqual(sections[2].group_id, 3)
        
