from django.urls import path
from .views import get_theme


app_name = 'theme'

urlpatterns = [
    path('/<int:theme_id>/', get_theme),
]
