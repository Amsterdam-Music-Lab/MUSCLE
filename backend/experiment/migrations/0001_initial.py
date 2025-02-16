# Generated by Django 3.2.8 on 2021-10-12 11:25
import random

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="Experiment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=64)),
                ("slug", models.CharField(max_length=64, unique=True)),
                ("active", models.BooleanField(default=True)),
                ("rounds", models.PositiveIntegerField(default=10)),
                ("bonus_points", models.PositiveIntegerField(default=0)),
                ("rules", models.CharField(default="", max_length=64)),
                (
                    "language",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Unset"),
                            ("aa", "Afar"),
                            ("af", "Afrikaans"),
                            ("ak", "Akan"),
                            ("sq", "Albanian"),
                            ("am", "Amharic"),
                            ("ar", "Arabic"),
                            ("an", "Aragonese"),
                            ("hy", "Armenian"),
                            ("as", "Assamese"),
                            ("av", "Avaric"),
                            ("ae", "Avestan"),
                            ("ay", "Aymara"),
                            ("az", "Azerbaijani"),
                            ("bm", "Bambara"),
                            ("ba", "Bashkir"),
                            ("eu", "Basque"),
                            ("be", "Belarusian"),
                            ("bn", "Bengali"),
                            ("bh", "Bihari languages"),
                            ("bi", "Bislama"),
                            ("nb", "Bokmål, Norwegian; Norwegian Bokmål"),
                            ("bs", "Bosnian"),
                            ("br", "Breton"),
                            ("bg", "Bulgarian"),
                            ("my", "Burmese"),
                            ("ca", "Catalan; Valencian"),
                            ("km", "Central Khmer"),
                            ("ch", "Chamorro"),
                            ("ce", "Chechen"),
                            ("ny", "Chichewa; Chewa; Nyanja"),
                            ("zh", "Chinese"),
                            (
                                "cu",
                                "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic",
                            ),
                            ("cv", "Chuvash"),
                            ("kw", "Cornish"),
                            ("co", "Corsican"),
                            ("cr", "Cree"),
                            ("hr", "Croatian"),
                            ("cs", "Czech"),
                            ("da", "Danish"),
                            ("dv", "Divehi; Dhivehi; Maldivian"),
                            ("nl", "Dutch; Flemish"),
                            ("dz", "Dzongkha"),
                            ("en", "English"),
                            ("eo", "Esperanto"),
                            ("et", "Estonian"),
                            ("ee", "Ewe"),
                            ("fo", "Faroese"),
                            ("fj", "Fijian"),
                            ("fi", "Finnish"),
                            ("fr", "French"),
                            ("ff", "Fulah"),
                            ("gd", "Gaelic; Scottish Gaelic"),
                            ("gl", "Galician"),
                            ("lg", "Ganda"),
                            ("ka", "Georgian"),
                            ("de", "German"),
                            ("el", "Greek, Modern (1453-)"),
                            ("gn", "Guarani"),
                            ("gu", "Gujarati"),
                            ("ht", "Haitian; Haitian Creole"),
                            ("ha", "Hausa"),
                            ("he", "Hebrew"),
                            ("hz", "Herero"),
                            ("hi", "Hindi"),
                            ("ho", "Hiri Motu"),
                            ("hu", "Hungarian"),
                            ("is", "Icelandic"),
                            ("io", "Ido"),
                            ("ig", "Igbo"),
                            ("id", "Indonesian"),
                            (
                                "ia",
                                "Interlingua (International Auxiliary Language Association)",
                            ),
                            ("ie", "Interlingue; Occidental"),
                            ("iu", "Inuktitut"),
                            ("ik", "Inupiaq"),
                            ("ga", "Irish"),
                            ("it", "Italian"),
                            ("ja", "Japanese"),
                            ("jv", "Javanese"),
                            ("kl", "Kalaallisut; Greenlandic"),
                            ("kn", "Kannada"),
                            ("kr", "Kanuri"),
                            ("ks", "Kashmiri"),
                            ("kk", "Kazakh"),
                            ("ki", "Kikuyu; Gikuyu"),
                            ("rw", "Kinyarwanda"),
                            ("ky", "Kirghiz; Kyrgyz"),
                            ("kv", "Komi"),
                            ("kg", "Kongo"),
                            ("ko", "Korean"),
                            ("kj", "Kuanyama; Kwanyama"),
                            ("ku", "Kurdish"),
                            ("lo", "Lao"),
                            ("la", "Latin"),
                            ("lv", "Latvian"),
                            ("li", "Limburgan; Limburger; Limburgish"),
                            ("ln", "Lingala"),
                            ("lt", "Lithuanian"),
                            ("lu", "Luba-Katanga"),
                            ("lb", "Luxembourgish; Letzeburgesch"),
                            ("mk", "Macedonian"),
                            ("mg", "Malagasy"),
                            ("ms", "Malay"),
                            ("ml", "Malayalam"),
                            ("mt", "Maltese"),
                            ("gv", "Manx"),
                            ("mi", "Maori"),
                            ("mr", "Marathi"),
                            ("mh", "Marshallese"),
                            ("mn", "Mongolian"),
                            ("na", "Nauru"),
                            ("nv", "Navajo; Navaho"),
                            ("nd", "Ndebele, North; North Ndebele"),
                            ("nr", "Ndebele, South; South Ndebele"),
                            ("ng", "Ndonga"),
                            ("ne", "Nepali"),
                            ("se", "Northern Sami"),
                            ("no", "Norwegian"),
                            ("nn", "Norwegian Nynorsk; Nynorsk, Norwegian"),
                            ("oc", "Occitan (post 1500)"),
                            ("oj", "Ojibwa"),
                            ("or", "Oriya"),
                            ("om", "Oromo"),
                            ("os", "Ossetian; Ossetic"),
                            ("pi", "Pali"),
                            ("pa", "Panjabi; Punjabi"),
                            ("fa", "Persian"),
                            ("pl", "Polish"),
                            ("pt", "Portuguese"),
                            ("ps", "Pushto; Pashto"),
                            ("qu", "Quechua"),
                            ("ro", "Romanian; Moldavian; Moldovan"),
                            ("rm", "Romansh"),
                            ("rn", "Rundi"),
                            ("ru", "Russian"),
                            ("sm", "Samoan"),
                            ("sg", "Sango"),
                            ("sa", "Sanskrit"),
                            ("sc", "Sardinian"),
                            ("sr", "Serbian"),
                            ("sn", "Shona"),
                            ("ii", "Sichuan Yi; Nuosu"),
                            ("sd", "Sindhi"),
                            ("si", "Sinhala; Sinhalese"),
                            ("sk", "Slovak"),
                            ("sl", "Slovenian"),
                            ("so", "Somali"),
                            ("st", "Sotho, Southern"),
                            ("es", "Spanish; Castilian"),
                            ("su", "Sundanese"),
                            ("sw", "Swahili"),
                            ("ss", "Swati"),
                            ("sv", "Swedish"),
                            ("tl", "Tagalog"),
                            ("ty", "Tahitian"),
                            ("tg", "Tajik"),
                            ("ta", "Tamil"),
                            ("tt", "Tatar"),
                            ("te", "Telugu"),
                            ("th", "Thai"),
                            ("bo", "Tibetan"),
                            ("ti", "Tigrinya"),
                            ("to", "Tonga (Tonga Islands)"),
                            ("ts", "Tsonga"),
                            ("tn", "Tswana"),
                            ("tr", "Turkish"),
                            ("tk", "Turkmen"),
                            ("tw", "Twi"),
                            ("ug", "Uighur; Uyghur"),
                            ("uk", "Ukrainian"),
                            ("ur", "Urdu"),
                            ("uz", "Uzbek"),
                            ("ve", "Venda"),
                            ("vi", "Vietnamese"),
                            ("vo", "Volapük"),
                            ("wa", "Walloon"),
                            ("cy", "Welsh"),
                            ("fy", "Western Frisian"),
                            ("wo", "Wolof"),
                            ("xh", "Xhosa"),
                            ("yi", "Yiddish"),
                            ("yo", "Yoruba"),
                            ("za", "Zhuang; Chuang"),
                            ("zu", "Zulu"),
                        ],
                        default="",
                        max_length=2,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Participant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unique_hash",
                    models.CharField(default=uuid.uuid4, max_length=64, unique=True),
                ),
                ("country_code", models.CharField(default="", max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name="Playlist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=64)),
                (
                    "process_csv",
                    models.BooleanField(
                        default=False,
                        help_text="Warning: Processing a live playlist may affect the result data",
                    ),
                ),
                (
                    "csv",
                    models.TextField(
                        blank=True,
                        help_text='CSV Format: artist_name [string],        song_name [string],start_position [float],duration [float],        "path/filename.mp3" [string], restricted_to_nl [int 0=False 1=True], tag_id [int], group_id [int]',
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "started_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "finished_at",
                    models.DateTimeField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                ("json_data", models.TextField(blank=True)),
                ("final_score", models.FloatField(db_index=True, default=0.0)),
                (
                    "experiment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="experiment.experiment",
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="experiment.participant",
                    ),
                ),
                (
                    "playlist",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="experiment.playlist",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("artist", models.CharField(db_index=True, max_length=128)),
                ("name", models.CharField(db_index=True, max_length=128)),
                ("start_time", models.FloatField(db_index=True, default=0.0)),
                ("duration", models.FloatField(default=0.0)),
                ("filename", models.CharField(max_length=128)),
                ("restrict_to_nl", models.BooleanField(default=False)),
                ("play_count", models.PositiveIntegerField(default=0)),
                (
                    "code",
                    models.PositiveIntegerField(default=random.randint(10000, 99999)),
                ),
                ("tag_id", models.PositiveIntegerField(default=0)),
                ("group_id", models.PositiveIntegerField(default=0)),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="experiment.playlist",
                    ),
                ),
            ],
            options={
                "ordering": ["artist", "name", "start_time"],
            },
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("expected_response", models.CharField(blank=True, max_length=100)),
                ("given_response", models.CharField(blank=True, max_length=100)),
                ("score", models.FloatField(default=0)),
                ("json_data", models.TextField(blank=True)),
                (
                    "section",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="experiment.section",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="experiment.session",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("question", models.CharField(max_length=64)),
                ("answer", models.CharField(default="", max_length=512)),
                ("session_id", models.PositiveIntegerField(default=0)),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="experiment.participant",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="experiment",
            name="playlists",
            field=models.ManyToManyField(to="experiment.Playlist"),
        ),
        migrations.AddIndex(
            model_name="profile",
            index=models.Index(
                fields=["participant", "answer"], name="experiment__partici_969242_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="profile",
            index=models.Index(
                fields=["session_id", "answer"], name="experiment__session_b36855_idx"
            ),
        ),
    ]
