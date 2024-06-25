from django.urls import path
from django.views.generic.base import TemplateView
from .views import get_experiment, get_experiment_collection, post_feedback, render_markdown, add_default_question_series, validate_experiment_playlist

app_name = 'experiment'

urlpatterns = [
    path('add_default_question_series/<int:id>/', add_default_question_series, name='add_default_question_series'),
    # Experiment
    path('render_markdown/', render_markdown, name='render_markdown'),
    path('validate_playlist/<str:rules_id>', validate_experiment_playlist, name='validate_experiment_playlist'),
    path('<slug:slug>/', get_experiment, name='experiment'),
    path('<slug:slug>/feedback/', post_feedback, name='feedback'),
    path('collection/<slug:slug>/', get_experiment_collection,
         name='experiment_collection'),

    # Robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    )
]
