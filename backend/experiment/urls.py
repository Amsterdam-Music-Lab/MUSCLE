from django.urls import path
from django.conf import settings
from django.views.generic.base import TemplateView
from . import api


app_name = 'experiment'

urlpatterns = [
    # Experiment
    path('id/<slug:slug>/', api.experiment.get, name='experiment'),
    path('continue/<int:session_id>', api.experiment.continue_experiment, name='continue_experiment'),

    # Section
    path('section/<int:section_id>/<int:code>/',
         api.section.get, name='section'),

    # Session
    path('session/create/',
         api.session.create, name='session_create'),
    path('session/result/',
         api.session.result, name='session_result'),
    path('session/<int:session_id>/next_round/',
         api.next_round, name='session_next_round'),

    # Participant
    path('participant/', api.participant.current,
         name='participant_current'),
    path('participant/scores/', api.participant.scores,
         name='participant_score'),
    path('participant/reload/<int:participant_id>/<slug:unique_hash>/',
         api.participant.reload, name='participant_reload'),
    path('participant/link/', api.participant.link,
         name='participant_link'),
    path('participant/share/', api.participant.share,
         name='participant_share'),

    # Profile
    path('profile/', api.profile.current,
         name='profile_current'),
    path('profile/create/', api.profile.create,
         name='profile_create'),
    path('profile/<slug:question>/', api.profile.get,
         name='profile_get'),

    # Robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    )
]

if settings.DEBUG:
    urlpatterns += [
        path('fake_playlist/<int:rows>/',
             api.dev.fake_playlist, name='fake_playlist'),
        path('fake_sessions/<int:experiment_id>/',
             api.dev.fake_sessions, name='fake_sessions'),
        path('test_forms/',
             api.dev.test_sessions, name='test_forms')
    ]
