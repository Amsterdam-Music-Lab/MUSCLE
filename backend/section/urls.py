from django.urls import path

from section.views import get_section, set_playlist

app_name = 'section'

urlpatterns = [
    # Section
    path("<int:section_id>/", get_section, name="section"),
    path("set_playlist/", set_playlist, name="set_playlist"),
]
