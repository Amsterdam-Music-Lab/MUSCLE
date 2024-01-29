from django.urls import path
from .views import create_session, continue_session, next_round, finalize_session, register_playlist

app_name='session'

urlpatterns = [
    path('create/',
        create_session, name='session_create'),
    path('<int:session_id>/next_round/',
        next_round, name='session_next_round'),
    path('<int:session_id>/register_playlist/',
         register_playlist, name='register_playlist'),
    path('continue/<int:session_id>', 
        continue_session, name='continue_session'),
    path('<int:session_id>/finalize/', finalize_session)
]
