from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    add_default_question_series,
    create_phase,
    get_block,
    get_experiment,
    post_feedback,
    render_markdown,
    validate_block_playlist,
)

app_name = 'experiment'

urlpatterns = [
    path('render_markdown/', render_markdown, name='render_markdown'),
    path('block/<slug:slug>/', get_block, name='block'),
    path('block/<slug:slug>/feedback/', post_feedback, name='feedback'),
    path(
        'block/<slug:slug>/default_question_series/',
        add_default_question_series,
        name="default_question_series",
    ),
    path('phase/create/', create_phase, name='create_phase'),
    path('<slug:slug>/', get_experiment, name='experiment'),
    # Robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
