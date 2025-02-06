# Exporting result data

## Export raw result data in JSON format

Using the admin interface you can export all relevant result data from the sessions of a specific block of an experiment.

To do so, navigate to [localhost:8000/admin/experiment/](http://localhost:8000/admin/experiment/) and click the `Experimenter Dashboard` button next to the experiment for which you want to export data.

Then, click "Export JSON" in the "Export Results" column.

After downloading and extracting the zip file you will have 7 JSON files containing the raw data as it is stored in the database by Django :

- [`sessions.json`](#sessionsjson) - All sessions that were logged by running this block.
- [`participants.json`](#participantsjson) - All participants that started a `Session` with this block.
- [`profiles.json`](#profilesjson) - All profile questions answered by the participants.
- [`results.json`](#resultsjson) - All results from the trials of this block.
- [`sections.json`](#sectionsjson) - All sections (sounds, images, stimuli, etc.) used in this block.
- [`songs.json`](#songsjson) - All `Song` objects that belong to the sections that were used in this block.
- [`feedback.json`](#feedbackjson) - All `Feedback` objects that belong to this block.

### Format of the exported data

Each file contains a list of objects, which are instances of a specific Django [model](https://docs.djangoproject.com/en/4.2/topics/db/models/#module-django.db.models), containing the data.

To link these objects together we use a field with a [Foreign key](https://docs.djangoproject.com/en/4.2/topics/db/models/#relationships) which relates to the [Primary Key](https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.primary_key) of the linked object.

The `Result` model is used twice, for different purposes:
- In `profiles.json`, which contains the profile (or `Participant`) questions. Recognizable by:
    - A foreign key value on the `Participant` field.
    - A `null` value on the `Session` field.
- In `results.json`, which contains the trial (or `Session`) results. Recognizable by:
    - A foreign key value on the `Session` field.
    - A `null` value on the `Participant` field.

***
#### sessions.json

Contains a list of all the sessions that were logged by running this block.
###### Example of an object of the `Session` model:

```
    {
        "model": "session.session",
        "pk": 2173,
        "fields": {
            "block": 1,
            "participant": 425,
            "playlist": 2,
            "started_at": "2024-07-22T10:26:50.911Z",
            "finished_at": "2024-07-22T10:31:53.955Z",
            "json_data": {
                "group": "S1",
                "phase": "FINISHED",
                "choices": {
                    "A": "___",
                    "B": "___"
                },
                "sequence": [4, 57, 51, 57, 12, 40, 35, 51, 57,  57, 35, 40, 33, 33, 37, 51, 13, 37, 29, 44, 37, 29, 4, 51, 57, 45, 45,
                            44, 12, 29, 57, 51, 35, 33, 51, 40, 44, 57, 4, 51, 37, 57, 57, 33, 40, 13, 13, 51, 29, 44, 57, 12, 51, 40,
                            12, 51, 37, 57, 33, 45, 12, 35, 45, 45, 44, 51, 13, 51, 51, 51, 35, 51, 4, 57, 57, 4, 13, 29, 57, 57
                ],
                "stimuli_a": "ORANGE",
                "experiment": "my_experiment",
                "pair_colors": "A = Orange, B = Blue",
                "button_order": "neutral",
                "button_colors": "Blue left, Orange right",
                "assigned_group": "Same direction, Pair 1",
                "training_rounds": 20,
                "feedback_sequence": [
                    10, 43, 51, 42, 9, 74, 75, 2, 31, 58, 68, 16, 8, 56, 69, 72, 70, 40, 35, 24
                ]
            },
            "final_score": 78.0,
            "current_round": 101
        }
    }
```

- `model`: Name of the django app followed by the name of the model (or database table).
- `pk`: The Primary Key of this session.
- `fields`:
    - `Block`: Foreign key `fk` relates to the `Block` object. (`block.pk`)
    - `Participant`: Foreign key `fk` relates to the `Participant` object. (`participant.pk`)
    - `playlist`: Foreign key `fk` relates to the `playlist` object. (`playlist.pk`)
    - `started_at`: Timestamp logged on creation of this `Session` object. (Set in the timezone of the server)
    - `finished_at`: Timestamp logged on finishing the `Session`. (Set in the timezone of the server)
    This will be set to `null` if the `Participant` hasn't completed the `Session`.
    - `json_data`:
        - `experiment`: Slug of the experiment that this block is a part of.
        - The rest of the data varies per `Block` type and generally contains configuration data sent by the backend, that is used while running this `Block` of the experiment. During the `Session` this data can be changed by the backend to log information on the progress of this `Block` and/or the user's actions. This data can then be used to dynamically alter the course of the `Session`.
    *e.g., The user can only continue to a next stage, when certain training trials have been completed successfully.*
    - `final_score`: The final score calculated upon completion of the `Session`. Unfinished sessions will have a value of `0,0`

***
#### participants.json

Contains a list of all the participants that started a `Session` with this block.
###### Example of an object of the `Participant` model:
```
    {
        "model": "participant.participant",
        "pk": 425,
        "fields": {
            "unique_hash": "8ebd4a37-e969-4e29-a535-482dfe1dedc4",
            "country_code": "nl",
            "access_info": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "participant_id_url": "test_user"
        }
    }
```

- `model`: Name of the django app followed by the name of the model (or database table).
- `pk`: Primary Key of this `Participant` object.
- `fields`:
    - `unique_hash`: The unique hash code, for this `Participant`.
    - `country_code`: The participant's country code derived from the ip address.
    - `access_info`: The participant's browser and operating system info, as provided by the [`User-Agent`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) request header, which is logged upon creation of this object.
    - `participant_id_url`: An optional custom identifier for this `Participant`, which is set through the URL of the experiment:
    *e.g., `localhost:3000/my_experiment?participant_id=<custom_id>`*

***
#### profiles.json

A list of `Result` objects containing the participant's anwers to the profile questions in this `Session`.
###### Example of an object of the `Result` model:
```
    {
        "model": "result.result",
        "pk": 7983,
        "fields": {
            "session": null,
            "participant": 425,
            "section": null,
            "created_at": "2024-07-20T14:28:13.227Z",
            "question_key": "dgf_generation",
            "expected_response": null,
            "given_response": "gen_x",
            "comment": "",
            "score": null,
            "scoring_rule": "",
            "json_data": {
                "key": "dgf_generation",
                "view": "RADIOS",
                "style": "neutral",
                "value": "gen_x",
                "config": {
                    "auto_advance": false,
                    "listen_first": false,
                    "response_time": 5,
                    "continue_label": "Continue",
                    "show_continue_button": true
                },
                "choices": {
                    "gen_x": "1965-1980",
                    "gen_z": "1997 or later",
                    "boomer": "1946–1964",
                    "silent": "1945 or earlier",
                    "millenial": "1981–1996"
                },
                "submits": false,
                "question": "When were you born?",
                "explainer": "",
                "result_id": 7983,
                "min_values": 1,
                "is_skippable": false,
                "decision_time": 4.958999872207642
            }
        }
    }
```

- `model`: Name of the django app followed by the name of the model (or database table).
- `pk`: Primary Key of this `Result` object.
- `fields`:
    - `Session`: Not used for profile (`Participant`) results.
    - `participant`: Foreign key `fk` relates to the `Participant` object. (`participant.pk`)
    - `Section`: Not used for profile (`Participant`) results.
    - `created_at`: Timestamp logged on creation of this `Result` object. (Set in the timezone of the server)
    - `question_key`: Unique identifier for this question.
    - `expected_response`: Not used for profile (`Participant`) results.
    - `given_response`: Participant's response to the question.
    - `comment`: Optional comment, sent by the backend.
    - `score`: Not used for profile (`Participant`) results.
    - `score`: The scoring rule used to calculate the score for this `Result`.
    - `json_data`:
        - `decision_time`: Logged time in seconds. Measured from presenting the question until the participant's response.
        - The rest of the data varies per `Question` type and generally contains configuration data sent by the backend to render a `Question` on the frontend.

***
#### results.json

A list of session `Result` objects containing the participant's responses to the trials in this `Session`.
###### Example of an object of the `Result` model:

```
{
        "model": "result.result",
        "pk": 8051,
        "fields": {
            "session": 2173,
            "participant": null,
            "section": 44,
            "created_at": "2024-07-22T10:29:57.720Z",
            "question_key": "choice",
            "expected_response": "B",
            "given_response": "B",
            "comment": "testing",
            "score": 1.0,
            "scoring_rule": "CORRECTNESS",
            "json_data": {
                "key": "choice",
                "view": "BUTTON_ARRAY",
                "style": {
                    "neutral": true,
                    "invisible-text": true,
                    "buttons-large-gap": true,
                    "buttons-large-text": true
                },
                "value": "B",
                "config": {
                    "auto_advance": true,
                    "listen_first": true,
                    "response_time": 5,
                    "continue_label": "Verder",
                    "time_pass_break": false,
                    "auto_advance_timer": 2500,
                    "show_continue_button": true
                },
                "choices": {
                    "A": "___",
                    "B": "___"
                },
                "submits": true,
                "question": "",
                "explainer": "",
                "result_id": 8051,
                "min_values": 1,
                "is_skippable": false,
                "decision_time": 0.31099987030029297,
                "expected_response": "B"
            }
        }
    }
```

- `model`: Name of the django app followed by the name of the model (or database table).
- `pk`: Primary Key of this `Result` object.
- `fields`:
    - `Session`: Foreign key `fk` relates to the `Session` object. (`session.pk`)
    - `Participant`: Not used for trial `Session` results.
    - `section`: Foreign key `fk` relates to the `Section` object used for this trial. (`Section.pk`)
    - `created_at`: Timestamp logged on creation of this `Result` object.
    - `question_key`: Unique identifier for the `Question` type in this trial.
    - `expected_response`: The expected/correct response to this trial.
    - `given_response`: Participant's response to this trial.
    - `comment`: Optional comment, sent by the backend.
    - `score`: The participant's score for this trial.
    - `scoring_rule`: The scoring rule used to calculate the score for this trial `Result`.
    - `json_data`:
        - `decision_time`: Logged response time in seconds. The start time can either be set the moment the trial has been loaded, or set after the sound has stopped playing. In this example `listen_first` is set in the `config` of the widget, so the time is measured from the moment the sound stopped playing until the response of the `Participant`.
        - The rest of the data varies per trial and widget type and generally contains configuration data sent by the backend to render a trial on the frontend.

***
#### sections.json

A list of `Section` objects used in the trials of this `Session`.
###### Example of an object of the `Section` model:
```
  {
        "model": "section.section",
        "pk": 21,
        "fields": {
            "playlist": 2,
            "song": 22,
            "start_time": 0.0,
            "duration": 1.25,
            "filename": "CAT/C3FcP1A.wav",
            "play_count": 31,
            "tag": "1A",
            "group": "CROSSED"
        }
    }
```

- `model`: Name of the django app followed by the name of the model (or database table).
- `pk`: Primary Key of this `Section` object.
- `fields`:
    - `playlist`: Foreign key `fk` relates to the `Playlist` object used for this trial. (`playlist.pk`)
    The `Playlist` object is not included in this export, as it's merely used to create a collection of sections and in itself doesn't provide additional data.
    -  `song`: Foreign key `fk` relates to the `Song` object of this `Section`. (`song.pk`)
    A `Song` object for a section is only created if an artist or name is provided upon creation of the `Section` object.
    - `start_time`: The offset time in seconds from the beginning of the audio file at which the player starts to play this `Section`.
    - `duration`: The duration in seconds of this section.
    The duration of a `Section` is calculated when a playlist is compiled with the [compileplaylist](https://github.com/Amsterdam-Music-Lab/MUSCLE/wiki/04.-Creating-playlists#manually-uploading-sound-files) command, or when the `Section` is uploaded via the [admin interface](https://github.com/Amsterdam-Music-Lab/MUSCLE/wiki/04.-Creating-playlists#uploading-sound-files-through-the-admin-interface).
    - `filename`: The actual folder and filename, relative to the `backend/upload` folder, where the audio file for this `Section` is stored.
    - `play_count`: How many times this `Section` has been played.
    - `tag`: A tag that can be used by the backend to identify sections for different purposes.
    *e.g., This section is the right or wrong response to a certain trial.*
    - `group`: A tag that can be used by the backend to group `Section`s for different purposes.
    *e.g., This `Section` belongs to the group of deprecated sections.*

***
#### songs.json

A list of `Song` objects that belong to the sections of the trials used for this `Session`.
###### Example of an object of the `Section` model:
```
{
        "model": "section.song",
        "pk": 52,
        "fields": {
            "artist": "P1 Training B-150Hz(4.6k)-220Hz(4.1k)-290Hz(3.6k)-360Hz(3.1k)-430Hz(2.6k).wav",
            "name": "C0T1B"
        }
    }
```

- `model`: Name of the django app followed by the name of the model (or database table).
- `pk`: Primary Key of this `Song` object.
- `fields`:
    - `artist`: The artist's name of this `Song`.
    - `name`: The name of this `Song`.

***
#### feedback.json

A list of `Feedback` objects that belong to this `Block`.
###### Example of an object of the `Feedback` model:
```
{
        "model": "experiment.feedback",
        "pk": 1,
        "fields": {
            "text": "Lorem.",
            "block": 3
        }
    }
```

- `model`: Name of the django app followed by the name of the model (or database table).
- `pk`: Primary Key of this `Feedback` object.
- `fields`:
    - `text`: The feedback on this block given by an anonymous participant.
    - `block`: Foreign key `fk` relates to the `Block` object.

## Export selected result data in CSV format


Using the admin interface you can export selected result data from the sessions from a specific block of an experiment as a `CSV` file.

To do so, navigate to [localhost:8000/admin/experiment/block](http://localhost:8000/admin/experiment/block) and click the `Export CSV` button next to the block that you want to export.

You will be presented with a screen that lets you choose the fields that you want to export, as well as the lay-out for the data in the CSV file:

![export-csv](https://github.com/user-attachments/assets/d2f603ca-b55d-4911-9de0-11ef6a69b326)

1. Choose the [`Session`](#sessionsjson) and related [`Participant`](#participantsjson) fields that you want to export.
    - [Click here](#sessionsjson) for a description of the raw `Session` data.
    - [Click here](#participantsjson) for a description of the raw `Participant` data.
2. Choose which fields of the `Result` object you want to export.
    - [Click here](#profilesjson) for a description of the raw profile `Result` data.
    - [Click here](#resultsjson) for a description of the raw trial `Result` data.
3. Select options to adjust the format of the exported CSV file.
4. Select to include the session's [`json_data`](#sessionsjson) field.
5. Select to convert the session's [`json_data`](#sessionsjson) field to seperate columns. The data in this field will vary in size per block type. Therefore converting this data to columns can in some situations cause the CSV file to become unreadable.
6. Select to include the trial result's [`json_data`](#resultsjson) field.
7. Select to convert the trial result's [`json_data`](#resultsjson) field to seperate columns. The data in this field will vary in size per trial type. Therefore converting this data to columns can in some situations cause the CSV file to become unreadable.
8. Choose a format for the CSV file:
    - Long format: (*default*)
        - Each result is a row.
    - Wide format:
        - Each session is a row, each result is a column.
9. Select a settings template here.
    - We have included a few templates of export settings for typical scenarios.
10. Click to load the selected template. The selected options on the left will change. You can still select or deselect options before you hit the export button. (11)
11. The export button! Click this button to download the CSV file from the server.
12. Go back to the `Block` overview page.

## The database structure
[![muscle_db_visualized](https://github.com/user-attachments/assets/f0d97029-ec49-4bcc-8c84-8ed35b0937c0)](https://github.com/user-attachments/assets/f0d97029-ec49-4bcc-8c84-8ed35b0937c0)
[*click to open the image to enable zoom functionality*](https://github.com/user-attachments/assets/f0d97029-ec49-4bcc-8c84-8ed35b0937c0)

## Note on Timestamps

All timestamps in JSON exports are in UTC time. This ensures consistency across different systems and time zones. Please also note that the timezone for this application is configurable via the `AML_TIME_ZONE` environment variable and defaults to "Europe/Amsterdam". To use a different timezone, update the `AML_TIME_ZONE` variable in your environment or in the .env file.

Look for the following lines in the base_settings.py file in the backend/aml directory:
```python
USE_TZ = True
TIME_ZONE = os.getenv("AML_TIME_ZONE", "Europe/Amsterdam")
```
