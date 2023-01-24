from django.urls import path
from django.views.generic.base import TemplateView
from .views import get_experiment

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
