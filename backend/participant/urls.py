from django.urls import path

from .views import current, link, reload, scores,share

app_name = 'participant'

urlpatterns = [
    # Participant
    path('', current,
         name='participant_current'),
    path('scores/', scores,
         name='participant_score'),
    path('reload/<int:participant_id>/<slug:unique_hash>/',
         reload, name='participant_reload'),
    path('link/', link,
         name='participant_link'),
    path('share/', share,
         name='participant_share'),
]