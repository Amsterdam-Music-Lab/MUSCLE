from django.test import TestCase

from section.models import Playlist

from experiment.rules.toontjehogerkids_5_tempo import ToontjeHogerKids5Tempo


class ToontjeHogerKids5TempoTest(TestCase):

    # Toontje Hoger Kids 5 Tempo does not have the strict tag validation
    # that Toontje Hoger 5 Tempo has. Therefore, we must ensure that
    # the validate_playlist method does not raise any errors for tags
    # that would be considered invalid in Toontje Hoger 5 Tempo.
    def test_validate_playlist_valid(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C3_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C5_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C5_P2_CH,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P1_CH,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C3_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,F4_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P9_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P2_ZR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C6_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C1_P3_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C1_P1_OZ,ch\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist.update_sections()

        toontje_hoger_5_tempo_rules = ToontjeHogerKids5Tempo()
        self.assertEqual(
            toontje_hoger_5_tempo_rules.validate_playlist(playlist), []
        )
