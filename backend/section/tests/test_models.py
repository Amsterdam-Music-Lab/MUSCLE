from django.test import override_settings, TestCase

from section.models import Playlist, Section, Song


class PlaylistModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Playlist.objects.create(name="TestPlaylist")

    def test_update_sections_csv_empty(self):
        playlist = Playlist.objects.get(name="TestPlaylist")
        playlist.csv = ""
        s = playlist._update_sections()
        self.assertFalse(playlist.section_set.all())
        self.assertEqual(s["status"], playlist.CSV_OK)

    def test_update_sections_invalid_row_length(self):
        playlist = Playlist.objects.get(name="TestPlaylist")
        # Third row invalid, len < 8
        playlist.csv = (
            "Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0\n"
            "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,0\n"
            "Netta,Toy,0.0,10.0,0,0\n"
            "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0\n"
        )
        s = playlist._update_sections()
        self.assertEqual(s["status"], playlist.CSV_ERROR)

    def test_update_sections_not_number(self):
        playlist = Playlist.objects.get(name="TestPlaylist")
        # Third row string is not a number
        playlist.csv = (
            "Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0\n"
            "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,0,0\n"
            "Netta,Toy,string,string,bat/netta.mp3,string,tag,group\n"
            "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0\n"
        )
        s = playlist._update_sections()
        self.assertEqual(s["status"], playlist.CSV_ERROR)

    def test_get_section(self):
        playlist = Playlist.objects.get(name="TestPlaylist")
        playlist.csv = (
            "Weird Al,Eat It,0.0,10.0,some/file.mp3,tag1,0\n"
            "Weird Al,Eat It,10.0,20.0,some/file.mp3,tag2,0\n"
            "Weird Al,Like a Surgeon,0.0,10.0,some/otherfile.mp3,tag1,0\n"
            "Weird Al,Like a Surgeon,10.0,20.0,some/otherfile.mp3,tag2,0\n"
        )
        playlist._update_sections()
        assert Song.objects.count() == 2
        song1 = Song.objects.get(name="Eat It")
        section = playlist.get_section(song_ids=[song1.id])
        assert section.song.id == song1.id
        section = playlist.get_section(filter_by={"tag": "tag1"})
        assert section.tag == "tag1"
        song2 = Song.objects.get(name="Like a Surgeon")
        section = playlist.get_section(filter_by={"tag": "tag2"}, song_ids=[song2.id])
        assert section.tag == "tag2" and section.song.id == song2.id
        with self.assertRaises(Section.DoesNotExist):
            playlist.get_section(filter_by={"tag": "non-existing tag"})

    def test_valid_csv(self):
        playlist = Playlist.objects.get(name="TestPlaylist")
        playlist.csv = (
            "Måneskin,Zitti e buoni,0.0,10.0,bat/maneskin.mp3,0,0\n"
            "Duncan Laurence,Arcade,0.0,10.0,bat/laurence.mp3,1,2\n"
            "Netta,Toy,0.0,10.0,bat/netta.mp3,tag,group\n"
            "Salvador Sobral,Amar pelos dois,0.0,10.0,bat/sobral.mp3,0,0\n"
        )
        s = playlist._update_sections()
        self.assertEqual(s["status"], playlist.CSV_OK)
        sections = playlist.section_set.all()
        self.assertEqual(len(sections), 4)

        self.assertEqual(sections[2].artist_name(), "Netta")
        self.assertEqual(sections[2].song_name(), "Toy")
        self.assertEqual(sections[2].start_time, 0.0)
        self.assertEqual(sections[2].duration, 10.0)
        self.assertEqual(sections[2].filename, "bat/netta.mp3")
        self.assertEqual(sections[2].tag, "tag")
        self.assertEqual(sections[2].group, "group")

        self.assertEqual(sections[3].artist_name(), "Salvador Sobral")
        self.assertEqual(sections[3].song_name(), "Amar pelos dois")
        self.assertEqual(sections[3].start_time, 0.0)
        self.assertEqual(sections[3].duration, 10.0)
        self.assertEqual(sections[3].filename, "bat/sobral.mp3")
        self.assertEqual(sections[3].tag, "0")
        self.assertEqual(sections[3].group, "0")

    def test_url_prefix_add_slash(self):
        playlist = Playlist.objects.get(name="TestPlaylist")
        playlist.url_prefix = "https://test.com"
        playlist.save()
        self.assertEqual(playlist.url_prefix, "https://test.com/")


class SectionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        playlist = Playlist.objects.create(name="TestPlaylist")
        song = Song.objects.create(name="São Paolo", artist="Guillemots")
        cls.section_with_song = Section.objects.create(
            playlist=playlist,
            song=song,
            start_time=0,
            duration=4.2,
            filename="/some/fantasy/path.mp3",
            tag="",
            group="",
        )
        cls.section_without_song = Section.objects.create(
            playlist=playlist,
            start_time=4,
            duration=0.2,
            filename="/another/fantasy/path.mp3",
            tag="",
            group="",
        )

    def test_artist_name(self):
        self.assertEqual(self.section_with_song.artist_name(), "Guillemots")
        self.assertEqual(self.section_without_song.artist_name(), "")
        self.assertEqual(self.section_without_song.artist_name("unknown"), "unknown")

    def test_song_name(self):
        self.assertEqual(self.section_with_song.song_name(), "São Paolo")
        self.assertEqual(self.section_without_song.song_name(), "")
        self.assertEqual(self.section_without_song.song_name("unknown"), "unknown")

    def test_song_label(self):
        self.assertEqual(self.section_with_song.song_label(), "Guillemots - São Paolo")
        self.assertEqual(self.section_without_song.song_label(), "")

    def test_start_time_str(self):
        self.assertEqual(self.section_with_song.start_time_str(), "00:00.000")
        self.assertEqual(self.section_without_song.start_time_str(), "00:04.000")

    def test_end_time_str(self):
        self.assertEqual(self.section_with_song.end_time_str(), "00:04.200")
        self.assertEqual(self.section_without_song.end_time_str(), "00:04.200")

    def test_string_method(self):
        self.assertEqual(
            str(self.section_with_song), "Guillemots - São Paolo (00:00.000-00:04.200)"
        )
        self.assertEqual(str(self.section_without_song), " (00:04.000-00:04.200)")

    def test_add_playcount(self):
        self.section_with_song.add_play_count()
        self.section_without_song.add_play_count()
        self.section_without_song.add_play_count()
        self.assertEqual(self.section_with_song.play_count, 1)
        self.assertEqual(self.section_without_song.play_count, 2)

    @override_settings(BASE_URL="TestingBase")
    def test_absolute_url_no_trailing_slash(self):
        assert self.section_with_song.absolute_url().startswith("TestingBase/section")

    @override_settings(BASE_URL="TestingBase//")
    def test_absolute_url_trailing_slashes(self):
        assert self.section_with_song.absolute_url().startswith("TestingBase/section")
