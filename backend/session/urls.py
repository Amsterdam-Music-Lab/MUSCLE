from django.urls import path
from .views import create_session, next_round, continue_session, finalize_session

app_name='session'

urlpatterns = [
    path('create/',
        create_session, name='session_create'),
    path('<int:session_id>/next_round/',
        next_round, name='session_next_round'),
    path('continue/<int:session_id>', 
        continue_session, name='continue_session'),
    path('<int:session_id>/finalize/', finalize_session)
]