from django.urls import path
from django.views.generic.base import TemplateView
from .views import get_experiment, get_experiment_collection, post_feedback, question_groups, add_default_question_series

app_name = 'experiment'

urlpatterns = [
    path('question_groups/', question_groups, name='question_groups'),
    path('add_default_question_series/<int:id>/', add_default_question_series, name='add_default_question_series'),
    # Experiment
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
