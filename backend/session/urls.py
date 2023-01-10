from django.urls import path
from .views import create_session, next_round, continue_session

urlpatterns = [
    path('session/create/',
        create_session, name='session_create'),
    path('session/<int:session_id>/next_round/',
        next_round, name='session_next_round'),
    path('session/continue/<int:session_id>', 
        continue_session, name='continue_session'),
]