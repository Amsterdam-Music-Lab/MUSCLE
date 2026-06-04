from django.urls import path
from .views import next_round

app_name = 'session'

urlpatterns = [
    path("<int:session_id>/next_round/", next_round, name="session_next_round"),
]
