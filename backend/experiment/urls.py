from django.urls import path
from django.views.generic.base import TemplateView
from .views import get_experiment, get_experiment_collection, post_feedback, default_questions, render_markdown

app_name = 'experiment'

urlpatterns = [
    # Experiment
    path('render_markdown/', render_markdown, name='render_markdown'),
    path('<slug:slug>/', get_experiment, name='experiment'),
    path('<slug:slug>/feedback/', post_feedback, name='feedback'),
    path('collection/<slug:slug>/', get_experiment_collection,
         name='experiment_collection'),
    path('default_questions/<str:rules>/', default_questions, name='default_questions'),

    # Robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    )
]
