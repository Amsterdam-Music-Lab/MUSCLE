from django.urls import path
from .views import create_session, next_round, finalize_session


app_name = 'session'

urlpatterns = [
    path("create/", create_session, name="session_create"),
    path("<int:session_id>/next_round/", next_round, name="session_next_round"),
    path("<int:session_id>/finalize/", finalize_session),
]
