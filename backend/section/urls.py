from django.urls import path
from .views import get_section, playlists

app_name = "section"

urlpatterns = [
    path("<int:section_id>/", get_section, name="section"),
    path("api/playlists/", playlists, name="playlists"),
]
