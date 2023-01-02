from django.urls import path

from .views import current, link, reload, scores,share

urlpatterns = [
    # Participant
    path('participant/', current,
         name='participant_current'),
    path('participant/scores/', scores,
         name='participant_score'),
    path('participant/reload/<int:participant_id>/<slug:unique_hash>/',
         reload, name='participant_reload'),
    path('participant/link/', link,
         name='participant_link'),
    path('participant/share/', share,
         name='participant_share'),
]