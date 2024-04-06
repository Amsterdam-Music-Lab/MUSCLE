from django.urls import path

from .views import get_section, validate_csv

app_name = 'section'

urlpatterns = [
    # Section
    path('<int:section_id>/<int:code>/',
        get_section, name='section'),
    path('validate_csv/', validate_csv, name='validate_csv'),
]
