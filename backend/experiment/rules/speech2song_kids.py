import random

from django.utils.translation import gettext as _
from django.conf import settings

from experiment.actions.info import Info
from experiment.actions.html import HTML
from experiment.actions.playback import Autoplay, ImagePlaybackSection
from experiment.actions.form import Form
from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.trial import Trial
from image.models import Image
from result.utils import prepare_result
from session.models import Session
from .base import BaseRules

class Speech2SongKids(BaseRules):
    """ Rules for a speech-to-song experiment """
    ID = 'SPEECH_TO_SONG_KIDS'
    available_images = [str(item + 1) for item in range(20)]

    def get_intro_explainer(self, session: Session):
        video = "https://player.vimeo.com/video/1012736887?h=bac11b4075"
        body = f'<div style="padding:56.25% 0 0 0;position:relative;margin-bottom:2vh;"><iframe src="{video}" frameborder="0" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="Hoe werkt een spectrogram?"></iframe></div><script src=https://player.vimeo.com/api/player.js></script>'
        session.save_json_data({"has_seen_intro": True})
        return Info(
            body=body
        )

    def next_round(self, session: Session):
        if not session.json_data.get("has_seen_intro"):
            return self.get_intro_explainer(session)
        else:
            previous_section = session.last_section()
            if previous_section and previous_section.tag == "single":
                section = session.playlist.get_section({"song": previous_section.song, "tag": "repeated"})
                this_image = session.json_data.get("current_image")
                image = Image.objects.get(tags__contains=[this_image, "long"])
            else:
                section = session.playlist.get_section(
                    {"song__id__in": session.get_unused_song_ids(), "tag": "single"}
                )
                available_images = session.json_data.get("available_images", [])
                if not len(available_images):
                    available_images = self.available_images
                random.shuffle(available_images)
                this_image = available_images.pop()
                image = Image.objects.get(tags__contains=[this_image, 'short'])
                session.save_json_data(
                    {"available_images": available_images, "current_image": this_image}
                )
            identifier = "speech_or_song"
            result_id = prepare_result(identifier, session=session, section=section)
            return Trial(
                html=HTML(
                    body='<div style="display: flex; flex-direction: row; justify-content: center;"><img src="http://localhost:8000/upload/2026/06/02/Melodieplaneet.png" style="width:80%"><img src="http://localhost:8000/upload/2026/06/02/Spraakplaneet.png" style="width:80%"></div>'
                ),
                playback=Autoplay(
                    sections=[
                        ImagePlaybackSection(
                            section=section,
                            image={
                                "link": f"{settings.BASE_URL}{settings.MEDIA_URL}{str(image.file)}",
                                "label": image.title,
                            },
                        )
                    ],
                    show_animation=False,
                ),
                feedback_form=Form(
                    form=[
                        ButtonArrayQuestion(
                            identifier=identifier,
                            choices=[
                                {
                                    "value": "music",
                                    "label": "🎵",
                                    "color": "colorNeutral1",
                                },
                                {
                                    "value": "speech",
                                    "label": "💬",
                                    "color": "colorNeutral2",
                                },
                            ],
                            result_id=result_id,
                        )
                    ]
                ),
                response_time=section.duration,
                listen_first=True,
            )
