from django.urls import path
from .views import question_groups

app_name = 'question'

urlpatterns = [
    path('question_groups/', question_groups, name='question_groups'),
]
