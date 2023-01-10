from django.urls import path
from django.conf import settings
from django.views.generic.base import TemplateView
from .views import get_experiment
from .api import dev


app_name = 'experiment'

urlpatterns = [
    # Experiment
    path('<slug:slug>/', get_experiment, name='experiment'),

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
             dev.fake_playlist, name='fake_playlist'),
        path('fake_sessions/<int:experiment_id>/',
             dev.fake_sessions, name='fake_sessions'),
        path('test_forms/',
             dev.test_sessions, name='test_forms')
    ]
