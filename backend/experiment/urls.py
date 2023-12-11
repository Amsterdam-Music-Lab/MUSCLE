from django.urls import path
from django.views.generic.base import TemplateView
from .views import get_experiment, post_feedback, default_questions

app_name = 'experiment'

urlpatterns = [
    # Experiment
    path('<slug:slug>/', get_experiment, name='experiment'),
    path('<slug:slug>/feedback/', post_feedback, name='feedback'),
    path('default_questions/<str:rules>/', default_questions, name='default_questions'),

    # Robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    )
]
