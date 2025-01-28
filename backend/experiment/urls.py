from django.urls import path, include
from rest_framework import routers
from django.views.generic.base import TemplateView
from .views import (
    ExperimentViewSet,
    get_block,
    get_experiment,
    post_feedback,
    render_markdown,
    add_default_question_series,
    validate_block_playlist,
    block_rules,
    get_available_questions,
)

app_name = "experiment"

router = routers.DefaultRouter()
router.register(r"experiments", ExperimentViewSet, basename="experiment")

urlpatterns = [
    # Experiment API
    path("api/", include(router.urls)),
    # Experiment
    path("render_markdown/", render_markdown, name="render_markdown"),
    path(
        "validate_playlist/<str:rules_id>",
        validate_block_playlist,
        name="validate_block_playlist",
    ),
    path("block/<slug:slug>/", get_block, name="block"),
    path("block/<slug:slug>/feedback/", post_feedback, name="feedback"),
    path(
        "block/<slug:slug>/default_question_series/",
        add_default_question_series,
        name="default_question_series",
    ),
    path("<slug:slug>/", get_experiment, name="experiment"),
    # Robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("api/block-rules/", block_rules, name="block-rules"),
    path("api/questions/", get_available_questions, name="get_available_questions"),
]
