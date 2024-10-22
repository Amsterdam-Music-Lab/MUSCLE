from django.urls import path

from .views import get_section

app_name = 'section'

urlpatterns = [
    # Section
    path("<int:section_id>/", get_section, name="section"),
]
