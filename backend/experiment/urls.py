from django.urls import path
from django.conf import settings
from django.views.generic.base import TemplateView
from . import api


app_name = 'experiment'

urlpatterns = [
    # Experiment
    path('id/<slug:slug>/', api.experiment.get, name='experiment'),

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
