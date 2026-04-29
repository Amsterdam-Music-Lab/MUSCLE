from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    FeedbackListView,
    get_block,
    get_experiment,
    post_feedback,
    render_markdown,
    validate_block_playlist,
)

app_name = 'experiment'

urlpatterns = [
    path('render_markdown/', render_markdown, name='render_markdown'),
    path(
        'validate_playlist/<str:rules_id>',
        validate_block_playlist,
        name='validate_block_playlist',
    ),
    path(
        'feedback_list/<int:block_id>', FeedbackListView.as_view(), name='feedback_list'
    ),
    path('<slug:slug>/', get_experiment, name='experiment'),
    path('<slug:experiment_slug>/block/<slug:slug>/', get_block, name='block'),
    path(
        '<slug:experiment_slug>/block/<slug:slug>/feedback/',
        post_feedback,
        name='feedback',
    ),
    # Robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
